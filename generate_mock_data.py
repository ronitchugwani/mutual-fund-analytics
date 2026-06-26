import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Schemes and names from fund_master
schemes = {
    125497: "HDFC_Top100",
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_Large_Cap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip"
}
scheme_codes = list(schemes.keys())

# Define date range matching NAV history
start_date = datetime(2013, 1, 1)
end_date = datetime(2025, 12, 31)

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days)
    random_day = random.randrange(int_delta)
    return start + timedelta(days=random_day)

# 1. Generate Mock Investor Transactions
# Let's generate a list of investors
investors = [f"INV{i:04d}" for i in range(1, 101)]
kyc_statuses = ["Verified", "Verified", "Verified", "Pending", "Rejected"]

transactions = []
# SIP transactions (recurring monthly)
for inv in investors:
    # Each investor has a couple of SIPs in random funds
    active_funds = random.sample(scheme_codes, k=random.randint(1, 3))
    kyc = random.choice(kyc_statuses)
    for fund in active_funds:
        sip_amount = random.choice([1000, 2000, 5000, 10000])
        # Generate monthly SIPs from a random start year (e.g. 2018 to 2024)
        sip_start_year = random.randint(2018, 2024)
        current = datetime(sip_start_year, random.randint(1, 12), 5)
        while current <= end_date:
            transactions.append({
                "transaction_date": current.strftime("%d-%m-%Y"),
                "transaction_type": "SIP",
                "amount": float(sip_amount),
                "units": float(sip_amount / random.uniform(10.0, 100.0)), # approximation
                "scheme_code": fund,
                "investor_id": inv,
                "kyc_status": kyc
            })
            # move to next month
            if current.month == 12:
                current = datetime(current.year + 1, 1, 5)
            else:
                current = datetime(current.year, current.month + 1, 5)

# Lumpsum and redemption transactions
for _ in range(300):
    inv = random.choice(investors)
    fund = random.choice(scheme_codes)
    txn_type = random.choice(["Lumpsum", "Redemption"])
    kyc = random.choice(kyc_statuses)
    txn_date = random_date(datetime(2018, 1, 1), end_date)
    
    amount = float(random.choice([10000, 25000, 50000, 100000]))
    if txn_type == "Redemption":
        amount = float(random.choice([5000, 10000, 20000]))
        
    transactions.append({
        "transaction_date": txn_date.strftime("%d-%m-%Y"),
        "transaction_type": txn_type,
        "amount": amount,
        "units": float(amount / random.uniform(20.0, 150.0)),
        "scheme_code": fund,
        "investor_id": inv,
        "kyc_status": kyc
    })

df_tx = pd.DataFrame(transactions)
df_tx.to_csv("data/raw/investor_transactions.csv", index=False)
print(f"Generated {len(df_tx)} transaction records.")

# 2. Generate Mock Scheme Performance
performance_records = []
# Quarterly records from 2018 to 2025
current = datetime(2018, 3, 31)
while current <= end_date:
    for fund in scheme_codes:
        expense_ratio = random.uniform(0.5, 2.2)
        performance_records.append({
            "scheme_code": fund,
            "date": current.strftime("%d-%m-%Y"),
            "return_1y": round(random.uniform(-15.0, 35.0), 2),
            "return_3y": round(random.uniform(-5.0, 25.0), 2),
            "return_5y": round(random.uniform(5.0, 20.0), 2),
            "expense_ratio": round(expense_ratio, 2)
        })
    # Move to next quarter
    if current.month == 3:
        current = datetime(current.year, 6, 30)
    elif current.month == 6:
        current = datetime(current.year, 9, 30)
    elif current.month == 9:
        current = datetime(current.year, 12, 31)
    else:
        current = datetime(current.year + 1, 3, 31)

df_perf = pd.DataFrame(performance_records)
df_perf.to_csv("data/raw/scheme_performance.csv", index=False)
print(f"Generated {len(df_perf)} performance records.")

# 3. Generate Mock Scheme AUM
aum_records = []
# Monthly AUM records from 2018 to 2025
current = datetime(2018, 1, 31)
base_aum = {fund: random.uniform(1000.0, 15000.0) for fund in scheme_codes}
while current <= end_date:
    for fund in scheme_codes:
        # AUM generally grows with random fluctuations
        growth = random.uniform(-0.02, 0.05)
        base_aum[fund] = base_aum[fund] * (1.0 + growth)
        aum_records.append({
            "scheme_code": fund,
            "date": current.strftime("%d-%m-%Y"),
            "aum": round(base_aum[fund], 2)
        })
    # Move to next month-end
    if current.month == 12:
        current = datetime(current.year + 1, 1, 31)
    else:
        next_month = current.month + 1
        # Quick last day of month calculator
        if next_month in [4, 6, 9, 11]:
            current = datetime(current.year, next_month, 30)
        elif next_month == 2:
            is_leap = (current.year % 4 == 0) and (current.year % 100 != 0 or current.year % 400 == 0)
            day = 29 if is_leap else 28
            current = datetime(current.year, next_month, day)
        else:
            current = datetime(current.year, next_month, 31)

df_aum = pd.DataFrame(aum_records)
df_aum.to_csv("data/raw/scheme_aum.csv", index=False)
print(f"Generated {len(df_aum)} AUM records.")
