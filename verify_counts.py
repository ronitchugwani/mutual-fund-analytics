from sqlalchemy import create_engine
import pandas as pd

db_path = "data/mutual_fund_analytics.db"
engine = create_engine(f"sqlite:///{db_path}")

tables = [
    "fact_nav",
    "fact_transactions",
    "fact_performance"
]

for table in tables:
    count = pd.read_sql(
        f"SELECT COUNT(*) cnt FROM {table}",
        engine
    )
    print(table, count.iloc[0]["cnt"])
