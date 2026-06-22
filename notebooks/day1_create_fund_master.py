import requests
import pandas as pd

# Map of scheme_code to official SEBI riskometer ratings (risk_grade)
RISK_GRADES = {
    125497: "Very High",   # SBI Small Cap Fund - Direct Plan - Growth
    119551: "Moderate",    # Aditya Birla Sun Life Banking & PSU Debt Fund - DIRECT - IDCW
    120503: "Very High",   # Axis ELSS Tax Saver Fund - Direct Plan - Growth Option
    118632: "Very High",   # Nippon India Large Cap Fund - Direct Plan Growth Plan - Growth Option
    119092: "Moderate",    # HDFC Money Market Fund - Growth Option - Direct Plan
    120841: "Very High"    # quant Mid Cap Fund - Growth Option - Direct Plan
}

schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

meta_records = []

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    meta = response.json()["meta"]
    
    # Process Category and Subcategory
    raw_category = meta.get("scheme_category", "")
    if " - " in raw_category:
        category, subcategory = raw_category.split(" - ", 1)
    else:
        category, subcategory = raw_category, ""
        
    # Build metadata record
    record = {
        "scheme_code": code,
        "fund_house": meta.get("fund_house", ""),
        "category": category.strip(),
        "subcategory": subcategory.strip(),
        "risk_grade": RISK_GRADES.get(code, "Unknown"),
        "short_name": name,
        "scheme_name": meta.get("scheme_name", ""),
        "isin_growth": meta.get("isin_growth", ""),
        "isin_div_reinvestment": meta.get("isin_div_reinvestment", "")
    }
    meta_records.append(record)

master_df = pd.DataFrame(meta_records)

# Write to fund_master.csv in data/raw
master_df.to_csv(
    "../data/raw/fund_master.csv",
    index=False
)

print("Fund Master Updated successfully:")
print(master_df.to_string())
