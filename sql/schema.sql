-- DDL for Mutual Fund Analytics Database Schema

CREATE TABLE dim_fund (
    fund_key INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER UNIQUE,
    fund_name TEXT,
    category TEXT,
    sub_category TEXT,
    fund_house TEXT
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    day INTEGER,
    month INTEGER,
    quarter INTEGER,
    year INTEGER
);

CREATE TABLE fact_nav (
    nav_key INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_key INTEGER,
    date_key INTEGER,
    nav REAL,
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE fact_transactions (
    transaction_key INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_key INTEGER,
    date_key INTEGER,
    investor_id TEXT,
    transaction_type TEXT,
    amount REAL,
    units REAL,
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE fact_performance (
    performance_key INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_key INTEGER,
    date_key INTEGER,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    expense_ratio REAL,
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE fact_aum (
    aum_key INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_key INTEGER,
    date_key INTEGER,
    aum REAL,
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);
