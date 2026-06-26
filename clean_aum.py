import pandas as pd
import os

source_file = "data/raw/scheme_aum.csv"
target_file = "data/processed/scheme_aum_clean.csv"

if not os.path.exists(source_file):
    print(f"Error: Source file '{source_file}' not found.")
    exit(1)

aum_df = pd.read_csv(source_file)

# Date formatting
aum_df['date'] = pd.to_datetime(
    aum_df['date'],
    dayfirst=True,
    errors='coerce'
)

# Validate AUM > 0
invalid_aum = aum_df[aum_df['aum'] <= 0]
print("Invalid AUM Rows (<= 0):", len(invalid_aum))

# Filter AUM
aum_df = aum_df[aum_df['aum'] > 0]

# Ensure output directory exists
os.makedirs(os.path.dirname(target_file), exist_ok=True)

# Save
aum_df.to_csv(
    target_file,
    index=False
)
print(f"Data cleaning complete. Cleaned AUM saved to '{target_file}'.")
