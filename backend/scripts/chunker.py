"""
Cleaning and Chunking Pipeline for Incredible Journeys: AI Tour Guide for India.
Cleans raw text, segments into 150-250 word passages with 30-word overlap,
computes 3 closest places by Haversine distance, and outputs data/processed/chunks.jsonl.
"""

import os
import re
import json
import math
from pathlib import Path
from typing import List, Dict, Any, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_FILE = PROCESSED_DIR / "chunks.jsonl"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points in kilometers."""
    R = 6371.0 # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 1)

def clean_text(text: str) -> str:
    """Clean markup, citations, reference sections, and noise from text."""
    if not text:
        return ""
        
    # Cut off references and external link sections
    for marker in ["== References ==", "== External links ==", "== See also ==", "== Further reading =="]:
        if marker in text:
            text = text.split(marker)[0]
            
    # Remove bracketed citations like [1], [23], [citation needed]
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\[edit\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[citation needed\]", "", text, flags=re.IGNORECASE)
    
    # Remove excessive wiki headers
    text = re.sub(r"={2,}\s*(.*?)\s*={2,}", r"\1. ", text)
    
    # Remove multiple spaces/newlines
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def chunk_words(text: str, target_size: int = 200, overlap: int = 30) -> List[str]:
    """Split text into 150-250 word chunks with specified overlap."""
    words = text.split()
    if not words:
        return []
    if len(words) <= target_size + 30:
        return [" ".join(words)]
        
    chunks = []
    step = target_size - overlap
    i = 0
    while i < len(words):
        chunk = words[i:i + target_size]
        if chunk:
            chunks.append(" ".join(chunk))
        if i + target_size >= len(words):
            break
        i += step
    return chunks

def build_proximity_graph(places: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Calculate the 3 closest places for each destination using Haversine distance."""
    proximity_map = {}
    
    # Collect places with coordinates
    with_coords = [p for p in places if p.get("lat") is not None and p.get("lon") is not None]
    
    for p in places:
        pid = p["id"]
        plat, plon = p.get("lat"), p.get("lon")
        
        candidates = []
        if plat is not None and plon is not None:
            for other in with_coords:
                if other["id"] == pid:
                    continue
                dist = haversine(plat, plon, other["lat"], other["lon"])
                candidates.append({
                    "place": other["place"],
                    "state": other["state"],
                    "distance_km": dist
                })
            candidates.sort(key=lambda x: x["distance_km"])
            proximity_map[pid] = candidates[:3]
        else:
            # Fallback: select other places from the same state
            same_state = [
                {"place": other["place"], "state": other["state"], "distance_km": 50.0}
                for other in places if other["id"] != pid and other["state"] == p["state"]
            ]
            proximity_map[pid] = same_state[:3]
            
    return proximity_map

def process_and_chunk():
    """Main pipeline for cleaning, proximity mapping, and chunk generation."""
    raw_files = list(RAW_DIR.glob("*.json"))
    if not raw_files:
        print(f"No raw JSON files found in {RAW_DIR}. Run collector.py first!")
        return

    places = []
    for f in raw_files:
        try:
            with open(f, "r", encoding="utf-8") as rf:
                data = json.load(rf)
                places.append(data)
        except Exception as e:
            print(f"Error reading {f}: {e}")

    print(f"Loaded {len(places)} raw place documents.")

    # Build proximity graph
    proximity_graph = build_proximity_graph(places)

    total_chunks = 0
    state_counts = {}
    chunks_records = []

    for p in places:
        pid = p["id"]
        place_name = p["place"]
        state = p["state"]
        city = p["city"]
        categories = p["category"]
        lat = p.get("lat")
        lon = p.get("lon")
        best_time = p.get("best_time", "")
        image_url = p.get("image_url", "")
        source = p.get("source", "Wikipedia & Wikivoyage (CC BY-SA 4.0)")
        source_url = p.get("source_url", "")
        google_maps_url = p.get("google_maps_url", "")
        directions_url = p.get("directions_url", "")
        nearby = proximity_graph.get(pid, [])
        
        state_counts[state] = state_counts.get(state, 0) + 1
        
        cleaned = clean_text(p.get("text", ""))
        word_chunks = chunk_words(cleaned, target_size=200, overlap=30)
        
        for c_idx, chunk_text in enumerate(word_chunks):
            chunk_id = f"{pid}_c{c_idx+1}"
            
            # Grounding context prefix for semantic retrieval accuracy
            categories_str = ", ".join(categories) if isinstance(categories, list) else str(categories)
            enriched_text = f"[{place_name}, {city}, {state} - Categories: {categories_str}]\n{chunk_text}"
            
            chunk_record = {
                "id": chunk_id,
                "place_id": pid,
                "place": place_name,
                "state": state,
                "city": city,
                "category": categories if isinstance(categories, list) else [categories],
                "lat": lat,
                "lon": lon,
                "best_time": best_time,
                "image_url": image_url,
                "source": source,
                "source_url": source_url,
                "google_maps_url": google_maps_url,
                "directions_url": directions_url,
                "nearby": nearby,
                "text": enriched_text,
                "raw_passage": chunk_text,
                "chunk_index": c_idx + 1,
                "total_chunks": len(word_chunks)
            }
            chunks_records.append(chunk_record)
            total_chunks += 1

    # Write output JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for cr in chunks_records:
            out.write(json.dumps(cr, ensure_ascii=False) + "\n")

    # Print comprehensive statistics
    print("\n" + "="*50)
    print("      DATASET CHUNKING & PROXIMITY STATISTICS")
    print("="*50)
    print(f"Total Places Processed:   {len(places)}")
    print(f"Total Chunks Generated:   {total_chunks}")
    print(f"Total States/UTs Covered: {len(state_counts)} (out of 36)")
    print(f"Average Chunks per Place: {total_chunks / len(places):.2f}")
    print(f"Destination Output Path:  {OUTPUT_FILE}")
    print("\nPlaces per State/UT:")
    print("-" * 50)
    for st, count in sorted(state_counts.items(), key=lambda x: x[0]):
        print(f"  {st:<42}: {count:>3} places")
    print("="*50 + "\n")

if __name__ == "__main__":
    process_and_chunk()
