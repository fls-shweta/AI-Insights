import streamlit as st
import pandas as pd
from analysis_engine import run_ai_cost_analysis

df = pd.read_excel("ppv_output_filtered_combined.xlsx")

st.set_page_config(page_title="AI Based Insights", layout="wide")

st.title("🤖 AI Based Insights")

# ---- Data Description ----
st.markdown("""
### 📊 Dataset Overview

This dataset contains supplier-level cost estimation data including:

- Supplier name
- Predicted cost vs last known cost
- Lead times
- Covered region and country
- Item-level aggregation

The AI engine analyzes cost variations, supplier performance, and regional distribution to generate executive-level insights.
""")    

st.subheader("Sample Data (First 5 Rows)")
st.dataframe(df.head())

if st.button("Generate Insights"):

    with st.spinner("Generating AI Insights..."):

        insights = run_ai_cost_analysis(df)

    st.subheader("Executive Insights")
    st.markdown(insights)
