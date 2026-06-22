import pandas as pd
from pathlib import Path

# Load fund master to map short names to scheme codes
fund_master = pd.read_csv("../data/raw/fund_master.csv")

all_dfs = []

# Map short names to their corresponding filename (handling HDFC_Top100 specifically)
file_mapping = {
    "HDFC_Top100": "hdfc_top100_nav.csv",
    "SBI_Bluechip": "SBI_Bluechip.csv",
    "ICICI_Bluechip": "ICICI_Bluechip.csv",
    "Nippon_Large_Cap": "Nippon_Large_Cap.csv",
    "Axis_Bluechip": "Axis_Bluechip.csv",
    "Kotak_Bluechip": "Kotak_Bluechip.csv"
}

for _, row in fund_master.iterrows():
    short_name = row["short_name"]
    code = row["scheme_code"]
    filename = file_mapping.get(short_name, f"{short_name}.csv")
    filepath = Path(f"../data/raw/{filename}")
    
    if filepath.exists():
        df = pd.read_csv(filepath)
        df["scheme_code"] = code
        all_dfs.append(df)
        print(f"Loaded {filename} for scheme {code} ({len(df)} rows)")
    else:
        print(f"Warning: File {filename} not found for scheme {code}")

if all_dfs:
    consolidated_df = pd.concat(all_dfs, ignore_index=True)
    # Reorder columns to place scheme_code first
    cols = ["scheme_code", "date", "nav"]
    consolidated_df = consolidated_df[cols]
    
    # Save to data/raw/nav_history.csv
    consolidated_df.to_csv("../data/raw/nav_history.csv", index=False)
    print(f"\nSuccessfully saved {len(consolidated_df)} rows to ../data/raw/nav_history.csv")
else:
    print("No NAV history files were found to consolidate.")
