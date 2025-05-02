import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="Service Metrics Dashboard", layout="wide")
st.title("📊 Microservice Observability Dashboard")

base_path = "data/parquet_output"
if not os.path.exists(base_path):
    st.error("No data found. Please run the pipeline to generate Parquet files.")
    st.stop()

services = [f.name for f in os.scandir(base_path) if f.is_dir()]
selected_service = st.selectbox("Select a service", services)

# Locate latest partition by date
dates = sorted([
    d.name for d in os.scandir(os.path.join(base_path, f"service={selected_service}")) if d.is_dir()
], reverse=True)

if dates:
    latest_date = dates[0]
    parquet_path = os.path.join(base_path, f"service={selected_service}", f"date={latest_date}", "data.parquet")
    df = pd.read_parquet(parquet_path)

    st.subheader(f"🛠 Service: `{selected_service}` | 📅 Date: {latest_date}")
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Avg Latency", f"{df['latency_ms'].mean():.2f} ms")
    col2.metric("🚨 P95 Latency", f"{df['latency_ms'].quantile(0.95):.2f} ms")
    col3.metric("❌ Error Rate", f"{(df['is_error'].mean() * 100):.2f}%")

    st.markdown("### 📉 Latency over Time")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    st.line_chart(df.set_index('timestamp')['latency_ms'])

    st.markdown("### 🧾 Raw Logs")
    st.dataframe(df.sort_values("timestamp", ascending=False).reset_index(drop=True))
else:
    st.warning(f"No logs found for {selected_service}.")
