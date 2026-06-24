-- Ten Analytical SQL Queries for Mutual Fund Analytics

-- 1. Top 5 Funds by AUM
SELECT fund_name, SUM(aum) total_aum
FROM fact_aum fa
JOIN dim_fund df ON fa.fund_key = df.fund_key
GROUP BY fund_name
ORDER BY total_aum DESC
LIMIT 5;

-- 2. Average NAV Per Month
SELECT
    year,
    month,
    AVG(nav) avg_nav
FROM fact_nav fn
JOIN dim_date dd ON fn.date_key = dd.date_key
GROUP BY year, month;

-- 3. SIP YoY Growth
SELECT
    year,
    SUM(amount) sip_amount
FROM fact_transactions ft
JOIN dim_date dd ON ft.date_key = dd.date_key
WHERE transaction_type = 'SIP'
GROUP BY year;

-- 4. Transactions by State
-- NOTE: Currently, `fact_transactions` does not have a `state` column in the DDL.
-- This query requires adding `state` to `fact_transactions` or joining with an investor dimension.
SELECT
    state,
    COUNT(*) txn_count
FROM fact_transactions
GROUP BY state;

-- 5. Funds with Expense Ratio < 1%
SELECT fund_name, expense_ratio
FROM fact_performance fp
JOIN dim_fund df ON fp.fund_key = df.fund_key
WHERE expense_ratio < 1;

-- 6. Highest 1Y Return Funds
SELECT fund_name, return_1y
FROM fact_performance fp
JOIN dim_fund df ON fp.fund_key = df.fund_key
ORDER BY return_1y DESC
LIMIT 10;

-- 7. Monthly Redemption Trend
SELECT
    year,
    month,
    SUM(amount) total_redemption
FROM fact_transactions ft
JOIN dim_date dd ON ft.date_key = dd.date_key
WHERE transaction_type = 'Redemption'
GROUP BY year, month;

-- 8. Average Expense Ratio by Category
SELECT
    category,
    AVG(expense_ratio) avg_expense_ratio
FROM fact_performance fp
JOIN dim_fund df ON fp.fund_key = df.fund_key
GROUP BY category;

-- 9. Fund Count by Category
SELECT
    category,
    COUNT(*) fund_count
FROM dim_fund
GROUP BY category;

-- 10. Highest Transaction Volume Funds
SELECT
    fund_name,
    SUM(amount) volume
FROM fact_transactions ft
JOIN dim_fund df ON ft.fund_key = df.fund_key
GROUP BY fund_name
ORDER BY volume DESC
LIMIT 10;
