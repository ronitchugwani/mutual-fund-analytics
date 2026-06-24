# Mutual Fund Analytics Data Dictionary

## dim_fund

| Column | Type | Definition |
|----------|----------|----------|
| fund_key | INTEGER | Surrogate key (Autoincrement) |
| amfi_code | INTEGER | AMFI scheme code (Unique) |
| fund_name | TEXT | Mutual fund scheme name |
| category | TEXT | Fund category |
| sub_category | TEXT | Fund subcategory |
| fund_house | TEXT | AMC name |

## dim_date

| Column | Type | Definition |
|----------|----------|----------|
| date_key | INTEGER | Date identifier in YYYYMMDD format (Primary Key) |
| full_date | DATE | Calendar date |
| day | INTEGER | Day of the month |
| month | INTEGER | Month of the year |
| quarter | INTEGER | Quarter of the year (1-4) |
| year | INTEGER | Year |

## fact_nav

| Column | Type | Definition |
|----------|----------|----------|
| nav_key | INTEGER | Surrogate key (Autoincrement) |
| fund_key | INTEGER | Reference to `dim_fund(fund_key)` |
| date_key | INTEGER | Reference to `dim_date(date_key)` |
| nav | REAL | Net Asset Value |

## fact_transactions

| Column | Type | Definition |
|----------|----------|----------|
| transaction_key | INTEGER | Surrogate key (Autoincrement) |
| fund_key | INTEGER | Reference to `dim_fund(fund_key)` |
| date_key | INTEGER | Reference to `dim_date(date_key)` |
| investor_id | TEXT | Unique ID of the investor |
| transaction_type | TEXT | Type of transaction (e.g. SIP, Lumpsum, Redemption) |
| amount | REAL | Transaction amount |
| units | REAL | Number of units purchased or redeemed |

## fact_performance

| Column | Type | Definition |
|----------|----------|----------|
| performance_key | INTEGER | Surrogate key (Autoincrement) |
| fund_key | INTEGER | Reference to `dim_fund(fund_key)` |
| date_key | INTEGER | Reference to `dim_date(date_key)` |
| return_1y | REAL | 1-year annualized return |
| return_3y | REAL | 3-year annualized return |
| return_5y | REAL | 5-year annualized return |
| expense_ratio | REAL | Expense ratio percentage |

## fact_aum

| Column | Type | Definition |
|----------|----------|----------|
| aum_key | INTEGER | Surrogate key (Autoincrement) |
| fund_key | INTEGER | Reference to `dim_fund(fund_key)` |
| date_key | INTEGER | Reference to `dim_date(date_key)` |
| aum | REAL | Assets Under Management |

Source:
- AMFI NAV History
- Investor Transaction Files
- Scheme Performance Files
