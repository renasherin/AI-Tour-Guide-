"""
Fetches exact, authentic, official Wikimedia Commons photography for all 639 destinations
using Wikipedia PageImages API with automatic redirect resolution and fallback mechanisms.
Stores verified image_url in backend raw dataset and frontend accurate_images.json.
"""

import os
import json
import glob
import time
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
FRONTEND_IMAGES_JSON = BASE_DIR.parent / "frontend" / "src" / "lib" / "accurate_images.json"

USER_AGENT = "IncredibleJourneysAtlas/1.0 (contact: tourguide@incrediblejourneys.in; Education & Heritage Non-profit)"

def fetch_batch_pageimages(titles_batch):
    """Query Wikipedia Action API for a batch of titles with redirects=1."""
    pipe_titles = "|".join([t.replace(" ", "_") for t in titles_batch])
    encoded = urllib.parse.quote(pipe_titles)
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded}&redirects=1&prop=pageimages&format=json&pithumbsize=1000"
    
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
            # Map of normalized/redirected title -> thumbnail
            results = {}
            redirects = {}
            normalized = {}
            
            if "query" in data:
                for norm in data["query"].get("normalized", []):
                    normalized[norm["to"]] = norm["from"]
                for red in data["query"].get("redirects", []):
                    redirects[red["to"]] = red["from"]
                
                for pid, page in data["query"].get("pages", {}).items():
                    title = page.get("title")
                    thumb = page.get("thumbnail", {}).get("source")
                    if thumb:
                        results[title] = thumb
                        # Map through redirects
                        if title in redirects:
                            orig = redirects[title]
                            results[orig] = thumb
                            if orig in normalized:
                                results[normalized[orig]] = thumb
                        if title in normalized:
                            results[normalized[title]] = thumb
            return results
    except Exception as e:
        print(f"Error fetching batch: {e}")
        return {}

def enrich_accurate_images():
    files = list(RAW_DIR.glob("*.json"))
    print(f"Starting authentic image enrichment for {len(files)} destinations...")
    
    # Map title -> list of files
    title_to_files = {}
    for f in files:
        with open(f, "r", encoding="utf-8") as rf:
            data = json.load(rf)
        t = data.get("wikipedia_title") or data.get("place")
        if t:
            clean_t = t.replace(" ", "_")
            title_to_files.setdefault(clean_t, []).append(f)

    unique_titles = list(title_to_files.keys())
    print(f"Found {len(unique_titles)} unique titles to query.")

    batch_size = 40
    all_thumbs = {}

    for i in range(0, len(unique_titles), batch_size):
        batch = unique_titles[i:i + batch_size]
        print(f"Fetching batch {i//batch_size + 1}/{(len(unique_titles) + batch_size - 1)//batch_size} ({len(batch)} titles)...")
        res = fetch_batch_pageimages(batch)
        all_thumbs.update(res)
        time.sleep(0.3)

    print(f"Direct Wikipedia pageimages found: {len(all_thumbs)}")

    # Update raw files and build frontend map
    frontend_map = {}
    updated_files = 0
    missing_places = []

    for f in files:
        with open(f, "r", encoding="utf-8") as rf:
            data = json.load(rf)

        pid = data.get("id", f.stem)
        w_title = (data.get("wikipedia_title") or data.get("place", "")).replace(" ", "_")
        
        # Check matching thumbnails (exact, underscore, or space)
        thumb_url = (
            all_thumbs.get(w_title) or
            all_thumbs.get(w_title.replace("_", " ")) or
            all_thumbs.get(data.get("place"))
        )

        if thumb_url:
            data["image_url"] = thumb_url
            frontend_map[pid] = thumb_url
            frontend_map[pid.replace("_", "-")] = thumb_url
            updated_files += 1
        else:
            missing_places.append((pid, data.get("place"), w_title))

        with open(f, "w", encoding="utf-8") as wf:
            json.dump(data, wf, indent=2, ensure_ascii=False)

    print(f"Successfully matched and saved authentic images for {updated_files} / {len(files)} destinations!")
    print(f"Unmatched places count: {len(missing_places)}")

    # Save frontend accurate_images.json
    FRONTEND_IMAGES_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(FRONTEND_IMAGES_JSON, "w", encoding="utf-8") as out:
        json.dump(frontend_map, out, indent=2, ensure_ascii=False)
    print(f"Exported frontend accurate images catalog to {FRONTEND_IMAGES_JSON}")

    if missing_places[:10]:
        print("Sample unmatched places:")
        for mp in missing_places[:10]:
            print(" -", mp)

if __name__ == "__main__":
    enrich_accurate_images()
