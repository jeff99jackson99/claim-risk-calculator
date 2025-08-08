import pandas as pd
from datetime import datetime

def days_between(start, end):
    try:
        d1 = datetime.strptime(start, '%m/%d/%Y')
        d2 = datetime.strptime(end, '%m/%d/%Y')
        return (d2 - d1).days
    except:
        return 9999

def check_risks(row):
    flags = []

    # Rule: High mileage
    if pd.to_numeric(row.get('Mileage', 0), errors='coerce') > 120000:
        flags.append('R2: High mileage')

    # Rule: Claim filed within 30 days of contract start
    if days_between(row.get('Contract Start'), row.get('Claim Date')) < 30:
        flags.append('R1: Early claim')

    # Rule: Suspicious notes
    notes = str(row.get('Notes', '')).lower()
    if 'pre-exist' in notes or 'continued operation' in notes:
        flags.append('R5: Pre-existing/continued use')

    # Rule: Near Limit of Liability
    try:
        repair_total = float(row.get('Repair Total', 0))
        lol = float(row.get('Limit of Liability', 999999))
        if repair_total >= lol * 0.9:
            flags.append('R4: Near LoL')
    except:
        pass

    return '; '.join(flags)

def main():
    try:
        df = pd.read_csv('/Users/jeffjackson/Desktop/python/claims.csv')
        df['Risk Flags'] = df.apply(check_risks, axis=1)
        flagged = df[df['Risk Flags'] != '']
        if not flagged.empty:
            flagged.to_csv('flagged_claims.csv', index=False)
            print("✅ Flagged claims saved to 'flagged_claims.csv'")
        else:
            print("✅ No high-risk claims found.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()