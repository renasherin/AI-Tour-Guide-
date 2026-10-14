"""
Enrich all raw destination profiles with verified Google Maps URLs and directions links.
"""

import os
import json
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

def enrich_dataset():
    if not RAW_DIR.exists():
        print(f"Directory {RAW_DIR} not found.")
        return

    json_files = list(RAW_DIR.glob("*.json"))
    print(f"Enriching {len(json_files)} destinations with Google Maps links...")

    updated_count = 0
    for f in json_files:
        try:
            with open(f, "r", encoding="utf-8") as rf:
                data = json.load(rf)

            place = data.get("place", "")
            state = data.get("state", "")
            city = data.get("city", "")
            lat = data.get("lat")
            lon = data.get("lon")

            # Generate Google Maps search / pin URL
            if lat is not None and lon is not None and float(lat) != 0.0 and float(lon) != 0.0:
                gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                directions_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
            else:
                loc_query = f"{place}, {city + ', ' if city else ''}{state}, India"
                encoded_q = urllib.parse.quote_plus(loc_query)
                gmaps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_q}"
                directions_url = f"https://www.google.com/maps/dir/?api=1&destination={encoded_q}"

            data["google_maps_url"] = gmaps_url
            data["directions_url"] = directions_url

            with open(f, "w", encoding="utf-8") as wf:
                json.dump(data, wf, indent=2, ensure_ascii=False)

            updated_count += 1
        except Exception as e:
            print(f"Error enriching {f}: {e}")

    print(f"Successfully enriched {updated_count} destination records with Google Maps links.")

if __name__ == "__main__":
    enrich_dataset()
