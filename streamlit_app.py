import streamlit as st
import pandas as pd
from analysis_engine import run_ai_cost_analysis

st.set_page_config(page_title="AI Based Insights", layout="wide")

st.title("🤖 AI Based Insights")

uploaded_file = st.file_uploader("Upload Cost Estimation Excel File", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    st.subheader("Sample Data (First 5 Rows)")
    st.dataframe(df.head())

    if st.button("Generate Insights"):

        with st.spinner("Generating AI Insights..."):

            insights = run_ai_cost_analysis(df)

        st.subheader("Executive Insights")
        st.markdown(insights)