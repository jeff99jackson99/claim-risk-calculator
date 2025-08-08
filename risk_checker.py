import streamlit as st
import pandas as pd
from risk_checker import find_high_risk

def main():
    st.title("Claim Risk Checker")

    uploaded_file = st.file_uploader("Upload your Excel workbook", type=["xlsx"])
    if uploaded_file is not None:
        # Read the uploaded workbook
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        
        # Run high-risk detection
        results = find_high_risk(df)

        if results:
            st.subheader("📋 High-Risk Patterns Detected")
            for pattern, subset in results.items():
                # Format pattern name nicely
                title = pattern.replace('_', ' ').title()
                st.markdown(f"### {title}")
                st.write(f"Records found: {len(subset)}")
                st.dataframe(subset)
        else:
            st.success("✅ No high-risk patterns detected.")

if __name__ == "__main__":
    main()