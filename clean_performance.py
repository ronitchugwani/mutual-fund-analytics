import pandas as pd
import os

source_file = "data/raw/scheme_performance.csv"
target_file = "data/processed/scheme_performance_clean.csv"

if not os.path.exists(source_file):
    print(f"Error: Source file '{source_file}' not found.")
    exit(1)

perf = pd.read_csv(source_file)

return_cols = [
    'return_1y',
    'return_3y',
    'return_5y'
]

for col in return_cols:
    perf[col] = pd.to_numeric(
        perf[col],
        errors='coerce'
    )

# Flag anomalies
for col in return_cols:
    anomalies = perf[
        (perf[col] > 100) |
        (perf[col] < -50)
    ]
    print(f"{col} anomalies:", len(anomalies))

# Expense ratio validation
invalid_expense = perf[
    (perf['expense_ratio'] < 0.1) |
    (perf['expense_ratio'] > 2.5)
]

print("Expense Ratio Issues:", len(invalid_expense))

# Ensure output directory exists
os.makedirs(os.path.dirname(target_file), exist_ok=True)

perf.to_csv(
    target_file,
    index=False
)
print(f"Data cleaning complete. Cleaned performance saved to '{target_file}'.")
