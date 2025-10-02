# app/app.py

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import json

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
METRICS_PATH = BASE_DIR.parent / "results" / "metrics.json"

# --- Load model ---
if not MODEL_PATH.exists():
    st.error("❌ Best model not found. Please run the training notebook first.")
    st.stop()

model = joblib.load(MODEL_PATH)

# --- Load metrics ---
metrics = {}
if METRICS_PATH.exists():
    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)

# --- Page config ---
st.set_page_config(
    page_title="CryptoAI 💰",
    page_icon="💰",
    layout="centered"
)

# --- Title ---
st.title("💰 CryptoAI")
st.markdown("<h4 style='text-align:center; color:#708993;'>Predict Bitcoin Close Price with AI-driven Market Signals</h4>", unsafe_allow_html=True)

# --- Sidebar inputs ---
st.sidebar.header("📊 Input Previous-Day Market Data")

btc_close = st.sidebar.number_input("BTC Previous Close (USD)", min_value=0.0, format="%.2f", value=20000.00)
btc_volume = st.sidebar.number_input("BTC Volume", min_value=0.0, format="%.2f", value=1000000.00)
eth_close = st.sidebar.number_input("ETH Previous Close (USD)", min_value=0.0, format="%.2f", value=1200.00)
eth_volume = st.sidebar.number_input("ETH Volume", min_value=0.0, format="%.2f", value=500000.00)
usdt_close = st.sidebar.number_input("USDT Previous Close (USD)", min_value=0.0, format="%.4f", value=1.0000)
usdt_volume = st.sidebar.number_input("USDT Volume", min_value=0.0, format="%.2f", value=2000000.00)

# Build dataframe
input_data = pd.DataFrame([{
    "BTC_Close_prev": btc_close,
    "BTC_Volume_prev": btc_volume,
    "ETH_Close_prev": eth_close,
    "ETH_Volume_prev": eth_volume,
    "USDT_Close_prev": usdt_close,
    "USDT_Volume_prev": usdt_volume
}])

# --- Predict ---
if st.button("🔮 Predict BTC Close Price"):
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted BTC Close Price: **${prediction:,.2f}**")

# --- Metrics section ---
st.markdown("---")
st.subheader("📈 Model Performance (on test set)")

if metrics:
    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"{float(metrics['MAE']):,.2f}")
    col2.metric("RMSE", f"{float(metrics['RMSE']):,.2f}")
    col3.metric("R²", f"{float(metrics['R2']):.4f}")
else:
    st.info("Run the notebook to generate metrics.json")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#A1C2BD;'>Built with ❤️ by Mubasshir Ahmed | CryptoAI © 2025</p>",
    unsafe_allow_html=True
)
