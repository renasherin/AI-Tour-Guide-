"""
Retrieval Evaluation and Query Verification for Incredible Journeys.
Executes 15 diverse sample queries across states, categories, and languages (English and Hindi),
printing top results with similarity scores, matched metadata, and nearby places.
"""

import sys
import time
from pathlib import Path

# Ensure UTF-8 console output for Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.rag.vector_db import VectorDBService

TEST_QUERIES = [
    "best time to visit Hampi",
    "temples near Madurai",
    "wildlife in Assam",
    "tea gardens and scenic spots in Kerala",
    "desert safari in Jaisalmer Thar desert",
    "monasteries and high altitude lakes in Ladakh",
    "living root bridges in Meghalaya",
    "beaches and water sports in Goa",
    "UNESCO world heritage sites in Madhya Pradesh",
    "snow spots and hill stations in Himachal Pradesh",
    "काजीरंगा राष्ट्रीय उद्यान में गैंडे",
    "वाराणसी के घाट और गंगा आरती",
    "coastal backwaters and houseboats in Alleppey",
    "royal palaces and stepwells in Gujarat",
    "Hornbill festival and cultural traditions of Nagaland",
]

def run_query_tests():
    db = VectorDBService()
    total_docs = db.count()
    print("=" * 75)
    print("       INCREDIBLE JOURNEYS: SEMANTIC RETRIEVAL VERIFICATION")
    print(f"       ChromaDB Index Count: {total_docs} passages")
    print("=" * 75)
    
    if total_docs == 0:
        print("Vector database is empty! Please run indexer.py first.")
        return

    for idx, q in enumerate(TEST_QUERIES, 1):
        print(f"\n[Query {idx:02d}/15]: \"{q}\"")
        print("-" * 75)
        
        t0 = time.time()
        results = db.search(q, k=3)
        latency_ms = (time.time() - t0) * 1000
        
        print(f"Retrieval latency: {latency_ms:.1f}ms | Top matches found: {len(results)}")
        
        for rank, r in enumerate(results, 1):
            place = r["place"]
            state = r["state"]
            similarity = r["similarity"]
            nearby_names = [n["place"] for n in r.get("nearby", [])[:2]]
            nearby_str = ", ".join(nearby_names) if nearby_names else "None listed"
            snippet = r["text"].split("\n")[-1][:140] + "..."
            
            print(f"  #{rank} [Score: {similarity:.4f}] {place} ({state})")
            print(f"     Nearby: {nearby_str} | Best time: {r.get('best_time', 'N/A')[:40]}")
            print(f"     Snippet: {snippet}")

    print("\n" + "=" * 75)
    print("All 15 retrieval test queries completed successfully!")
    print("=" * 75)

if __name__ == "__main__":
    run_query_tests()
