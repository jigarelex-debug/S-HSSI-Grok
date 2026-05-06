import streamlit as st
import pandas as pd
import numpy as np
from data_fetch import fetch_enso_latest, fetch_iod_latest, fetch_mjo_latest
from datetime import datetime
import json

st.set_page_config(page_title="S-HSSI Dashboard", layout="wide", page_icon="🌡️")
st.title("🌡️ State-Level Hybrid Summer Severity Index (S-HSSI)")
st.markdown("**v2.1 Production Edition with Daily Auto-Refresh** • Exact white-paper framework • May 2026 live")

# Last refresh
try:
    with open("climate_cache.json") as f:
        cache = json.load(f)
    last = datetime.fromisoformat(cache["last_updated"].replace("Z", "+00:00"))
    st.caption(f"🕒 Last auto-refreshed: {last.strftime('%d %b %Y %H:%M UTC')} (daily GitHub Action)")
except:
    st.caption("🕒 Live data fetch active")

# Coefficients, normalization, historical data (exact from white paper)
archetypes = { ... }  # (full archetypes dict from previous full version - keep as-is)
state_to_type = { ... }  # (full state_to_type dict - keep as-is)
calibration = { ... }  # (full calibration dict - keep as-is)
def normalize(v, param): ...  # (full function - keep as-is)
historical = { ... }  # (full Table 2 - keep as-is)
years = list(range(2015, 2026))
hist_df = pd.DataFrame(historical, index=years).T

# Sidebar (same as before)
st.sidebar.header("Forecast Phase")
phase = st.sidebar.radio("Phase", ["Phase 1 (Feb 15 – Preliminary)", "Phase 2 (Mar 20 – Final)"], index=1)
# ... (all sidebar inputs for enso, iod, mjo, wd, march_heat, etc. - copy from previous full app.py)

# Calculation engine (same)
def compute_shssi(...): ...  # full function
# Compute scores
scores = {state: compute_shssi(state, inputs) for state in state_to_type.keys()}
score_df = pd.DataFrame(list(scores.items()), columns=["State", "S-HSSI Score"]).sort_values("S-HSSI Score", ascending=False)

st.subheader(f"2026 S-HSSI Scores – {phase}")
st.dataframe(score_df.style.background_gradient(cmap="RdYlGn_r"), use_container_width=True)

st.subheader("Historical Validation 2015–2025")
st.dataframe(hist_df.style.background_gradient(cmap="RdYlGn_r", axis=1), use_container_width=True)

st.caption("✅ Simplified version running • Daily auto-refresh active • Full version with map coming next")
