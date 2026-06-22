import pandas as pd

fund_master = pd.read_csv("../data/raw/fund_master.csv")
nav_history = pd.read_csv("../data/raw/nav_history.csv")

master_codes = set(fund_master["scheme_code"])

nav_codes = set(nav_history["scheme_code"])

missing = master_codes - nav_codes

print("Missing Codes:", len(missing))

if len(missing):
    print(list(missing)[:20])
else:
    print("All codes validated.")
