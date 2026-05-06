from data_fetch import fetch_enso_latest, fetch_iod_latest, fetch_mjo_latest
import json
from pathlib import Path
from datetime import datetime

def update_cache():
    enso = fetch_enso_latest()
    iod = fetch_iod_latest()
    mjo = fetch_mjo_latest()
    
    cache = {
        "enso": enso,
        "iod": iod,
        "mjo": mjo,
        "last_updated": datetime.utcnow().isoformat()
    }
    
    Path("climate_cache.json").write_text(json.dumps(cache, indent=2))
    print(f"✅ Cache updated at {cache['last_updated']}")

if __name__ == "__main__":
    update_cache()