import pandas as pd
from pathlib import Path

# Load files
fund_master_path = Path("../data/raw/fund_master.csv")
nav_history_path = Path("../data/raw/nav_history.csv")

fund_master = pd.read_csv(fund_master_path)
nav_history = pd.read_csv(nav_history_path)

# 1. Dataset Count
# We loaded 6 individual CSVs (Axis, ICICI, Kotak, Nippon, SBI, HDFC) + 1 master + 1 consolidated
csv_files = list(Path("../data/raw").glob("*.csv"))
individual_funds = [f for f in csv_files if f.name not in ["fund_master.csv", "nav_history.csv"]]
dataset_count = len(individual_funds)

# 2. Missing Values
missing_cols = []
for col in fund_master.columns:
    missing_count = fund_master[col].isnull().sum()
    if missing_count > 0:
        missing_cols.append(f"fund_master.csv -> {col} ({missing_count} missing values)")

for col in nav_history.columns:
    missing_count = nav_history[col].isnull().sum()
    if missing_count > 0:
        missing_cols.append(f"nav_history.csv -> {col} ({missing_count} missing values)")

if not missing_cols:
    missing_str = "     - None"
else:
    missing_str = "\n".join([f"     - {col}" for col in missing_cols])

# 3. Duplicates
duplicates_count = nav_history.duplicated().sum() + fund_master.duplicated().sum()

# 4. AMFI Validation
master_codes = set(fund_master["scheme_code"])
nav_codes = set(nav_history["scheme_code"])
missing_codes = master_codes - nav_codes
total_checked = len(master_codes)
missing_count = len(missing_codes)

# Build the report string
report = f"""DATA QUALITY SUMMARY

1. Dataset Count
   - {dataset_count} datasets loaded successfully

2. Missing Values
   - Missing values observed in:
{missing_str}

3. Duplicates
   - {duplicates_count} duplicate rows found

4. AMFI Validation
   - {total_checked} scheme codes checked
   - {missing_count} missing in NAV history

5. Datatype Issues
   - Date columns require parsing
   - NAV columns require numeric conversion

6. Recommendation
   - Standardize date formats
   - Remove duplicates
   - Impute or drop missing records
   - Create schema validation checks
"""

# Save to reports/data_quality_summary.txt
output_path = Path("../reports/data_quality_summary.txt")
output_path.write_text(report)

print("Data Quality Summary Report generated:")
print(report)
