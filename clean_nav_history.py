import pandas as pd

# Load the raw NAV history data
nav = pd.read_csv("data/raw/nav_history.csv")

# Parse dates
nav['date'] = pd.to_datetime(nav['date'], dayfirst=True, errors='coerce')

# Remove duplicates
nav = nav.drop_duplicates()

# Sort by scheme code and date
nav = nav.sort_values(['scheme_code', 'date'])

# Forward fill NAV within each scheme
nav['nav'] = nav.groupby('scheme_code')['nav'].ffill()

# Validate NAV > 0
invalid_nav = nav[nav['nav'] <= 0]

if len(invalid_nav) > 0:
    print(f"Found {len(invalid_nav)} invalid NAV records")

nav = nav[nav['nav'] > 0]

# Save to processed directory
nav.to_csv("data/processed/nav_history_clean.csv", index=False)
print("Data cleaning complete. Saved cleaned NAV history to 'data/processed/nav_history_clean.csv'.")
