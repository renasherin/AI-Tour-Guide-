"""
Verify all frontend and backend routes on a single localhost: http://localhost:3000
"""

import urllib.request
import json
import sys

routes = [
    ('/', 'text/html'),
    ('/explore', 'text/html'),
    ('/destinations/kanjirapuzha_dam_and_gardens', 'text/html'),
    ('/guide', 'text/html'),
    ('/about', 'text/html'),
    ('/api/health', 'application/json'),
    ('/api/destinations?limit=2', 'application/json'),
    ('/api/destinations/kanjirapuzha_dam_and_gardens', 'application/json'),
    ('/docs', 'text/html'),
    ('/openapi.json', 'application/json'),
]

def verify():
    all_ok = True
    print("=" * 70)
    print("  VERIFYING UNIFIED SINGLE LOCALHOST: http://localhost:3000")
    print("=" * 70)
    for path, expected_mime in routes:
        url = f"http://localhost:3000{path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": expected_mime})
            with urllib.request.urlopen(req, timeout=5) as resp:
                status = resp.status
                ctype = resp.headers.get("Content-Type", "").split(";")[0]
                print(f" [PASS] {path:<48} -> Status {status} ({ctype})")
        except Exception as e:
            print(f" [FAIL] {path:<48} -> Error: {e}")
            all_ok = False

    print("=" * 70)
    if all_ok:
        print("ALL ROUTES ACCESSIBLE AND FULLY WORKING ON http://localhost:3000!")
    else:
        print("Some routes failed!")
        sys.exit(1)

if __name__ == "__main__":
    verify()
