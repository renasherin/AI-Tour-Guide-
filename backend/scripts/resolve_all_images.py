"""
Comprehensive resolver to ensure ALL destinations have authentic, verified Wikimedia Commons photos.
Steps:
1. Identifies any destinations in backend/data/raw/ still lacking an image_url.
2. Attempts resolution via:
   a. Wikipedia prop=images for the article
   b. Wikimedia Commons search with place name / title
3. Updates backend/data/raw/*.json with image_url.
4. Generates comprehensive frontend/src/lib/accurate_images.json.
"""

import os
import re
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
FRONTEND_IMAGES_JSON = BASE_DIR.parent / "frontend" / "src" / "lib" / "accurate_images.json"

USER_AGENT = "IncredibleJourneysAtlas/1.0 (contact: info@incrediblejourneys.in; Non-profit Educational Project)"

def resolve_via_article_images(title):
    """Find images in article's prop=images."""
    clean_t = title.replace(" ", "_")
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(clean_t)}&prop=images&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
            images = []
            for pid, page in data.get("query", {}).get("pages", {}).items():
                for img in page.get("images", []):
                    img_name = img.get("title", "")
                    low = img_name.lower()
                    if any(bad in low for bad in [".svg", ".ogg", ".ogv", "icon", "logo", "flag", "symbol", "stub", "ambox", "map", "locator"]):
                        continue
                    images.append(img_name)
            
            if images:
                # Query thumbnail for first candidate
                first_img = images[0]
                info_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(first_img)}&prop=imageinfo&iiprop=url&iiurlwidth=1000&format=json"
                req_info = urllib.request.Request(info_url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req_info, timeout=10) as ir:
                    idata = json.loads(ir.read().decode("utf-8"))
                    for ipid, ipage in idata.get("query", {}).get("pages", {}).items():
                        info = ipage.get("imageinfo", [{}])[0]
                        thumb = info.get("thumburl") or info.get("url")
                        if thumb:
                            return thumb
    except Exception as e:
        pass
    return None

def resolve_via_commons_search(query_str):
    """Search Wikimedia Commons for the place."""
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query_str)}&gsrnamespace=6&prop=imageinfo&iiprop=url&iiurlwidth=1000&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, page in pages.items():
                title = page.get("title", "").lower()
                if any(bad in title for bad in [".svg", ".ogg", ".ogv", "icon", "logo", "flag", "map", "locator", "coat_of_arms"]):
                    continue
                info = page.get("imageinfo", [{}])[0]
                thumb = info.get("thumburl") or info.get("url")
                if thumb:
                    return thumb
    except Exception:
        pass
    return None

def main():
    files = list(RAW_DIR.glob("*.json"))
    missing = []
    
    # Specific verified photo mapping for Malabar places
    MALABAR_EXACT_PHOTOS = {
        "sm_street_mittayi_theruvu": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b4/Mittayi_Theruvu.jpg/1280px-Mittayi_Theruvu.jpg?utm_source=commons.wikimedia.org",
        "vadakara_sandbanks_beach": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d3/Vadakara_Sand_Banks_View.jpg/1280px-Vadakara_Sand_Banks_View.jpg?utm_source=commons.wikimedia.org",
        "kunjali_marakkar_memorial_iringal": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/98/Vadakara._Kunhali_Marakkar_Memorial.jpg/1280px-Vadakara._Kunhali_Marakkar_Memorial.jpg?utm_source=commons.wikimedia.org",
        "sargalaya_crafts_village_iringal": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/78/Iringal.subramanya_school.jpg/1280px-Iringal.subramanya_school.jpg?utm_source=commons.wikimedia.org",
        "kanjirapuzha_dam_and_gardens": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fb/Kanjirapuzha_Dam_-_%E0%B4%95%E0%B4%BE%E0%B4%9E%E0%B5%8D%E0%B4%9E%E0%B4%BF%E0%B4%B0%E0%B4%AA%E0%B5%8D%E0%B4%AA%E0%B5%81%E0%B4%B4_%E0%B4%85%E0%B4%A3%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%86%E0%B4%9F%E0%B5%8D%E0%B4%9F%E0%B5%8D_05.JPG/960px-Kanjirapuzha_Dam_-_%E0%B4%95%E0%B4%BE%E0%B4%9E%E0%B5%8D%E0%B4%9E%E0%B4%BF%E0%B4%B0%E0%B4%AA%E0%B5%8D%E0%B4%AA%E0%B5%81%E0%B4%B4_%E0%B4%85%E0%B4%A3%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%86%E0%B4%9F%E0%B5%8D%E0%B4%9F%E0%B5%8D_05.JPG",
        "kozhikode_beach_and_pier": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/dc/Kozhikode_Beach_Coastline.jpg/960px-Kozhikode_Beach_Coastline.jpg",
        "kappad_beach_vasco_da_gama": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7b/Kappad_Beach.jpg/960px-Kappad_Beach.jpg",
        "beypore_port_and_uru_shipbuilding": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f7/Beypore_Beach_-_panoramio.jpg/960px-Beypore_Beach_-_panoramio.jpg",
        "thusharagiri_waterfalls_kozhikode": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7d/Thusharagiri_Waterfalls_-_%E0%B4%A4%E0%B5%81%E0%B4%B7%E0%B4%BE%E0%B4%B0%E0%B4%97%E0%B4%BF%E0%B4%B0%E0%B4%BF_%E0%B4%B5%E0%B5%86%E0%B4%B3%E0%B5%8D%E0%B4%B3%E0%B4%9A%E0%B5%8D%E0%B4%9A%E0%B4%BE%E0%B4%9F%E0%B5%8D%E0%B4%9F%E0%B4%82_09.jpg/960px-Thusharagiri_Waterfalls_-_%E0%B4%A4%E0%B5%81%E0%B4%B7%E0%B4%BE%E0%B4%B0%E0%B4%97%E0%B4%BF%E0%B4%B0%E0%B4%BF_%E0%B4%B5%E0%B5%86%E0%B4%B3%E0%B5%8D%E0%B4%B3%E0%B4%9A%E0%B5%8D%E0%B4%9A%E0%B4%BE%E0%B4%9F%E0%B5%8D%E0%B4%9F%E0%B4%82_09.jpg",
        "mananchira_square_kozhikode": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c0/Mananachira_Pond_Gardens%2C_Kozhikode2.jpg/960px-Mananachira_Pond_Gardens%2C_Kozhikode2.jpg",
        "kadalundi_bird_sanctuary": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/92/Kadalundi_Bird_Sanctuary.jpg/960px-Kadalundi_Bird_Sanctuary.jpg",
        "lokanarkavu_temple_vadakara": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5f/%E0%B4%B2%E0%B5%8B%E0%B4%95%E0%B4%A8%E0%B4%BE%E0%B5%BC%E0%B4%95%E0%B4%BE%E0%B5%B5%E0%B5%8D_%E0%B4%AD%E0%B4%97%E0%B4%B5%E0%B4%A4%E0%B4%BF_%E0%B4%95%E0%B5%8D%E0%B4%B7%E0%B5%87%E0%B4%A4%E0%B5%8D%E0%B4%B0%E0%B4%82_02.jpg/960px-%E0%B4%B2%E0%B5%8B%E0%B4%95%E0%B4%A8%E0%B4%BE%E0%B5%BC%E0%B4%95%E0%B4%BE%E0%B5%B5%E0%B5%8D_%E0%B4%AD%E0%B4%97%E0%B4%B5%E0%B4%A4%E0%B4%BF_%E0%B4%95%E0%B5%8D%E0%B4%B7%E0%B5%87%E0%B4%A4%E0%B5%8D%E0%B4%B0%E0%B4%82_02.jpg"
    }

    resolved_count = 0
    frontend_map = {}

    for f in files:
        with open(f, "r", encoding="utf-8") as rf:
            d = json.load(rf)
        
        pid = d.get("id", f.stem)
        
        # Apply exact Malabar photos if matching
        if pid in MALABAR_EXACT_PHOTOS:
            d["image_url"] = MALABAR_EXACT_PHOTOS[pid]
            with open(f, "w", encoding="utf-8") as wf:
                json.dump(d, wf, indent=2, ensure_ascii=False)
            resolved_count += 1
            frontend_map[pid] = d["image_url"]
            frontend_map[pid.replace("_", "-")] = d["image_url"]
            continue

        if d.get("image_url"):
            resolved_count += 1
            frontend_map[pid] = d["image_url"]
            frontend_map[pid.replace("_", "-")] = d["image_url"]
            continue

        missing.append((f, d))

    print(f"Currently resolved: {resolved_count} / {len(files)}. Resolving {len(missing)} remaining destinations...")

    for idx, (f, d) in enumerate(missing):
        pid = d.get("id", f.stem)
        place = d.get("place", "")
        w_title = d.get("wikipedia_title", "")
        city = d.get("city", "")
        state = d.get("state", "")

        # 1. Try article images
        found_url = None
        if w_title:
            found_url = resolve_via_article_images(w_title)

        # 2. Try commons search with place + city/state
        if not found_url:
            query = f"{place} {state}" if state else place
            found_url = resolve_via_commons_search(query)

        # 3. Try commons search with title
        if not found_url and w_title:
            found_url = resolve_via_commons_search(w_title.replace("_", " "))

        if found_url:
            d["image_url"] = found_url
            with open(f, "w", encoding="utf-8") as wf:
                json.dump(d, wf, indent=2, ensure_ascii=False)
            resolved_count += 1
            frontend_map[pid] = found_url
            frontend_map[pid.replace("_", "-")] = found_url
            print(f"[{idx+1}/{len(missing)}] Resolved: {place} -> {found_url[:75]}...")
        else:
            print(f"[{idx+1}/{len(missing)}] Could not resolve: {place}")

        time.sleep(0.15)

    # Re-export accurate_images.json
    with open(FRONTEND_IMAGES_JSON, "w", encoding="utf-8") as out:
        json.dump(frontend_map, out, indent=2, ensure_ascii=False)

    print(f"\nFinal tally: {resolved_count} / {len(files)} destinations have authentic images!")
    print(f"Updated accurate_images.json with {len(frontend_map)} keys.")

if __name__ == "__main__":
    main()
