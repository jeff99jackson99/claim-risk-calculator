import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🛡️ High-Risk Claim Checker")

uploaded_file = st.file_uploader("Upload an Excel File (.xlsx)", type="xlsx")

def days_between(start, end):
    try:
        d1 = datetime.strptime(str(start), '%m/%d/%Y')
        d2 = datetime.strptime(str(end), '%m/%d/%Y')
        return (d2 - d1).days
    except:
        return 9999

def check_risks(row):
    flags = []

    if pd.to_numeric(row.get('Mileage', 0), errors='coerce') > 120000:
        flags.append('R2: High mileage')

    if days_between(row.get('Contract Start'), row.get('Claim Date')) < 30:
        flags.append('R1: Early claim')

    notes = str(row.get('Notes', '')).lower()
    if 'pre-exist' in notes or 'continued operation' in notes:
        flags.append('R5: Pre-existing/continued use')

    try:
        repair_total = float(row.get('Repair Total', 0))
        lol = float(row.get('Limit of Liability', 999999))
        if repair_total >= lol * 0.9:
            flags.append('R4: Near LoL')
    except:
        pass

    return '; '.join(flags)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df['Risk Flags'] = df.apply(check_risks, axis=1)
    flagged = df[df['Risk Flags'] != '']
    
    if not flagged.empty:
        st.success("⚠️ High-risk claims found!")
        st.dataframe(flagged)
        st.download_button("📥 Download Flagged Claims", flagged.to_csv(index=False), file_name="flagged_claims.csv")
    else:
        st.info("✅ No high-risk claims found.")