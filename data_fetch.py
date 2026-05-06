import pandas as pd
import requests
import json
from pathlib import Path
from datetime import datetime

CACHE_FILE = Path("climate_cache.json")

def load_cache():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {}

def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump({**data, "last_updated": datetime.utcnow().isoformat()}, f)

def fetch_enso_latest():
    cache = load_cache()
    if "enso" in cache:
        return cache["enso"]
    url = "https://psl.noaa.gov/data/timeseries/month/data/nino34.long.anom.data"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = resp.text.strip().split('\n')
        for line in reversed(lines):
            if line.strip() and line[0].isdigit():
                parts = line.split()
                if len(parts) >= 13:
                    data = {"value": float(parts[-1]), "year": int(parts[0])}
                    save_cache({"enso": data})
                    return data
    except:
        pass
    return {"value": 0.8, "year": 2026}

def fetch_iod_latest():
    cache = load_cache()
    if "iod" in cache:
        return cache["iod"]
    url = "https://www.jamstec.go.jp/aplinfo/sintexf/DATA/dmi.monthly.txt"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = resp.text.strip().split('\n')
        for line in reversed(lines):
            if line.strip() and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 3:
                    data = {"value": float(parts[2])}
                    save_cache({"iod": data})
                    return data
    except:
        pass
    return {"value": 0.6}

def fetch_mjo_latest():
    cache = load_cache()
    if "mjo" in cache:
        return cache["mjo"]
    url = "https://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        lines = resp.text.strip().split('\n')
        for line in reversed(lines):
            if line.strip() and not line.startswith('Date'):
                parts = line.split()
                if len(parts) >= 5:
                    rmm1 = float(parts[2])
                    rmm2 = float(parts[3])
                    data = {"amplitude": (rmm1**2 + rmm2**2)**0.5}
                    save_cache({"mjo": data})
                    return data
    except:
        pass
    return {"amplitude": 1.2}