"""
Root ingestion script entrypoint for Incredible Journeys: Discover India with AI.
Idempotent and resumable.
"""

import sys
from pathlib import Path

# Ensure root is in path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.rag.ingest import run_ingestion

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Incredible Journeys Ingestion CLI")
    parser.add_argument("--force", action="store_true", help="Force re-indexing of ChromaDB")
    parser.add_argument("--dry-run", action="store_true", help="Audit without updating database")
    args = parser.parse_args()

    run_ingestion(force=args.force, dry_run=args.dry_run)
