import pandas as pd
import os

source_file = "data/raw/investor_transactions.csv"
target_file = "data/processed/investor_transactions_clean.csv"

if not os.path.exists(source_file):
    print(f"Error: Source file '{source_file}' not found.")
    exit(1)

tx = pd.read_csv(source_file)

# Date formatting (using dayfirst=True to handle standard formats consistently)
tx['transaction_date'] = pd.to_datetime(
    tx['transaction_date'],
    dayfirst=True,
    errors='coerce'
)

# Standardize transaction types
tx['transaction_type'] = (
    tx['transaction_type']
    .str.strip()
    .str.upper()
)

mapping = {
    'SIP': 'SIP',
    'SYSTEMATIC INVESTMENT PLAN': 'SIP',
    'LUMPSUM': 'Lumpsum',
    'LUMP SUM': 'Lumpsum',
    'REDEMPTION': 'Redemption',
    'REDEEM': 'Redemption'
}

tx['transaction_type'] = tx['transaction_type'].replace(mapping)

# Amount validation
invalid_amt = tx[tx['amount'] <= 0]

# KYC validation
valid_kyc = ['Verified', 'Pending', 'Rejected']
invalid_kyc = tx[~tx['kyc_status'].isin(valid_kyc)]

print("Invalid Amount Rows:", len(invalid_amt))
print("Invalid KYC Rows:", len(invalid_kyc))

# Filter amount
tx = tx[tx['amount'] > 0]

# Ensure output directory exists
os.makedirs(os.path.dirname(target_file), exist_ok=True)

tx.to_csv(
    target_file,
    index=False
)
print(f"Data cleaning complete. Cleaned transactions saved to '{target_file}'.")
