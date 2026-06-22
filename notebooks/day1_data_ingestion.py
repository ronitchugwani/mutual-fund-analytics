import pandas as pd
from pathlib import Path

RAW_DIR = Path("../data/raw")

csv_files = list(RAW_DIR.glob("*.csv"))

for file in csv_files:
    print("=" * 80)
    print(f"FILE: {file.name}")

    try:
        df = pd.read_csv(file)

        print("\nShape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nHead:")
        print(df.head())

        print("\nPotential Anomalies:")

        print("Missing Values:")
        print(df.isnull().sum().sort_values(ascending=False).head())

        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

    except Exception as e:
        print(f"Error reading file: {e}")
