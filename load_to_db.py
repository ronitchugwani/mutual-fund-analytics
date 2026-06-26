import pandas as pd
# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine
import os

db_path = "data/mutual_fund_analytics.db"
engine = create_engine(f"sqlite:///{db_path}")

def main():
    # 1. Populate dim_fund
    fund_master_path = "data/raw/fund_master.csv"
    if os.path.exists(fund_master_path):
        print("Populating dim_fund...")
        fm = pd.read_csv(fund_master_path)
        dim_fund = pd.DataFrame({
            'amfi_code': fm['scheme_code'],
            'fund_name': fm['scheme_name'],
            'category': fm['category'],
            'sub_category': fm['subcategory'],
            'fund_house': fm['fund_house']
        })
        
        # Insert or ignore duplicate fund entries
        with engine.begin() as conn:
            # We fetch existing to insert only new ones
            try:
                existing_codes = pd.read_sql("SELECT amfi_code FROM dim_fund", conn)['amfi_code'].tolist()
            except Exception:
                existing_codes = []
            
            new_funds = dim_fund[~dim_fund['amfi_code'].isin(existing_codes)]
            if len(new_funds) > 0:
                new_funds.to_sql('dim_fund', conn, if_exists='append', index=False)
                print(f"Loaded {len(new_funds)} new funds into dim_fund.")
            else:
                print("No new funds to load into dim_fund.")
    else:
        print(f"Warning: {fund_master_path} not found. Skipping dim_fund population.")

    # Fetch dim_fund lookup mapping
    try:
        dim_fund_lookup = pd.read_sql("SELECT fund_key, amfi_code FROM dim_fund", engine)
    except Exception as e:
        print("Error reading dim_fund lookup. Have you initialized the schema?", e)
        return

    # Helper function to populate dim_date and get keys mapping
    def get_or_create_date_keys(dates_series):
        dates = pd.to_datetime(dates_series).dropna().unique()
        if len(dates) == 0:
            return pd.DataFrame()
        
        date_df = pd.DataFrame({'full_date': dates})
        date_df['date_key'] = date_df['full_date'].dt.strftime('%Y%m%d').astype(int)
        date_df['day'] = date_df['full_date'].dt.day
        date_df['month'] = date_df['full_date'].dt.month
        date_df['quarter'] = date_df['full_date'].dt.quarter
        date_df['year'] = date_df['full_date'].dt.year
        date_df['full_date'] = date_df['full_date'].dt.strftime('%Y-%m-%d')
        
        # Load existing dates to avoid duplicate key errors
        with engine.begin() as conn:
            try:
                existing_dates = pd.read_sql("SELECT date_key FROM dim_date", conn)['date_key'].tolist()
            except Exception:
                existing_dates = []
            
            new_dates = date_df[~date_df['date_key'].isin(existing_dates)]
            if len(new_dates) > 0:
                new_dates.to_sql('dim_date', conn, if_exists='append', index=False)
                print(f"Loaded {len(new_dates)} new dates into dim_date.")
                
        return date_df[['full_date', 'date_key']]

    # 2. Populate fact_nav
    nav_path = "data/processed/nav_history_clean.csv"
    if os.path.exists(nav_path):
        print("Populating fact_nav...")
        nav = pd.read_csv(nav_path)
        
        # Parse dates and map keys
        nav['date_parsed'] = pd.to_datetime(nav['date'])
        date_mapping = get_or_create_date_keys(nav['date_parsed'])
        nav['full_date_str'] = nav['date_parsed'].dt.strftime('%Y-%m-%d')
        
        # Joins to get surrogate keys
        nav = nav.merge(date_mapping, left_on='full_date_str', right_on='full_date', how='inner')
        nav = nav.merge(dim_fund_lookup, left_on='scheme_code', right_on='amfi_code', how='inner')
        
        fact_nav = nav[['fund_key', 'date_key', 'nav']]
        
        # Replaces fact_nav data while preserving DB schema constraints
        with engine.begin() as conn:
            conn.exec_driver_sql("DELETE FROM fact_nav")
            fact_nav.to_sql('fact_nav', conn, if_exists='append', index=False)
        print(f"Successfully loaded {len(fact_nav)} records into fact_nav.")
    else:
        print(f"Warning: {nav_path} not found. Skipping fact_nav.")

    # 3. Populate fact_transactions
    tx_path = "data/processed/investor_transactions_clean.csv"
    if os.path.exists(tx_path):
        print("Populating fact_transactions...")
        tx = pd.read_csv(tx_path)
        
        tx['date_parsed'] = pd.to_datetime(tx['transaction_date'])
        date_mapping = get_or_create_date_keys(tx['date_parsed'])
        tx['full_date_str'] = tx['date_parsed'].dt.strftime('%Y-%m-%d')
        
        tx = tx.merge(date_mapping, left_on='full_date_str', right_on='full_date', how='inner')
        
        # Identify scheme/amfi code column
        scheme_col = 'scheme_code' if 'scheme_code' in tx.columns else ('amfi_code' if 'amfi_code' in tx.columns else None)
        if scheme_col:
            tx = tx.merge(dim_fund_lookup, left_on=scheme_col, right_on='amfi_code', how='inner')
        
        fact_tx = tx[['fund_key', 'date_key', 'investor_id', 'transaction_type', 'amount']]
        fact_tx['units'] = tx['units'] if 'units' in tx.columns else None
        
        with engine.begin() as conn:
            conn.exec_driver_sql("DELETE FROM fact_transactions")
            fact_tx.to_sql('fact_transactions', conn, if_exists='append', index=False)
        print(f"Successfully loaded {len(fact_tx)} records into fact_transactions.")
    else:
        print("Warning: Cleaned transactions file not found. Skipping fact_transactions.")

    # 4. Populate fact_performance
    perf_path = "data/processed/scheme_performance_clean.csv"
    if os.path.exists(perf_path):
        print("Populating fact_performance...")
        perf = pd.read_csv(perf_path)
        
        date_col = 'date' if 'date' in perf.columns else ('calculation_date' if 'calculation_date' in perf.columns else None)
        perf['date_parsed'] = pd.to_datetime(perf[date_col]) if date_col else pd.Timestamp.now().normalize()
        
        date_mapping = get_or_create_date_keys(perf['date_parsed'])
        perf['full_date_str'] = perf['date_parsed'].dt.strftime('%Y-%m-%d')
        
        perf = perf.merge(date_mapping, left_on='full_date_str', right_on='full_date', how='inner')
        
        scheme_col = 'scheme_code' if 'scheme_code' in perf.columns else ('amfi_code' if 'amfi_code' in perf.columns else None)
        if scheme_col:
            perf = perf.merge(dim_fund_lookup, left_on=scheme_col, right_on='amfi_code', how='inner')
            
        fact_perf = perf[['fund_key', 'date_key', 'return_1y', 'return_3y', 'return_5y', 'expense_ratio']]
        
        with engine.begin() as conn:
            conn.exec_driver_sql("DELETE FROM fact_performance")
            fact_perf.to_sql('fact_performance', conn, if_exists='append', index=False)
        print(f"Successfully loaded {len(fact_perf)} records into fact_performance.")
    else:
        print("Warning: Cleaned performance file not found. Skipping fact_performance.")

    # 5. Populate fact_aum
    aum_path = "data/processed/scheme_aum_clean.csv"
    if os.path.exists(aum_path):
        print("Populating fact_aum...")
        aum = pd.read_csv(aum_path)
        
        aum['date_parsed'] = pd.to_datetime(aum['date'])
        date_mapping = get_or_create_date_keys(aum['date_parsed'])
        aum['full_date_str'] = aum['date_parsed'].dt.strftime('%Y-%m-%d')
        
        aum = aum.merge(date_mapping, left_on='full_date_str', right_on='full_date', how='inner')
        
        scheme_col = 'scheme_code' if 'scheme_code' in aum.columns else ('amfi_code' if 'amfi_code' in aum.columns else None)
        if scheme_col:
            aum = aum.merge(dim_fund_lookup, left_on=scheme_col, right_on='amfi_code', how='inner')
            
        fact_aum = aum[['fund_key', 'date_key', 'aum']]
        
        with engine.begin() as conn:
            conn.exec_driver_sql("DELETE FROM fact_aum")
            fact_aum.to_sql('fact_aum', conn, if_exists='append', index=False)
        print(f"Successfully loaded {len(fact_aum)} records into fact_aum.")
    else:
        print("Warning: Cleaned AUM file not found. Skipping fact_aum.")

if __name__ == "__main__":
    main()
