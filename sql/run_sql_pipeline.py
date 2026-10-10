"""
Run SQL Pipeline for Telco Customer Churn Project
Executes SQL migration scripts against SQLite and exports data/processed/telco_churn_cleaned.csv.
"""

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("data", "telco_churn.db")
RAW_CSV_PATH = os.path.join("data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
PROCESSED_CSV_PATH = os.path.join("data", "processed", "telco_churn_cleaned.csv")
SQL_DIR = "sql"

def run_pipeline():
    print(f"[*] Initializing SQLite database at: {DB_PATH}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(PROCESSED_CSV_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Run 01_create_tables.sql
    print("[*] Executing 01_create_tables.sql...")
    with open(os.path.join(SQL_DIR, "01_create_tables.sql"), "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    conn.commit()
    
    # 2. Ingest raw CSV into raw_customers
    print(f"[*] Ingesting raw CSV from {RAW_CSV_PATH} into raw_customers table...")
    df_raw = pd.read_csv(RAW_CSV_PATH)
    df_raw.to_sql("raw_customers", conn, if_exists="append", index=False)
    conn.commit()
    print(f"    Raw records inserted: {len(df_raw)}")
    
    # 3. Run 02_data_cleaning.sql
    print("[*] Executing 02_data_cleaning.sql...")
    with open(os.path.join(SQL_DIR, "02_data_cleaning.sql"), "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    conn.commit()
    
    # 4. Run 03_feature_engineering.sql
    print("[*] Executing 03_feature_engineering.sql...")
    with open(os.path.join(SQL_DIR, "03_feature_engineering.sql"), "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    conn.commit()
    
    # 5. Export cleaned_customers to CSV
    print(f"[*] Exporting cleaned_customers to {PROCESSED_CSV_PATH}...")
    df_cleaned = pd.read_sql_query("SELECT * FROM cleaned_customers", conn)
    df_cleaned.to_csv(PROCESSED_CSV_PATH, index=False)
    print(f"    Exported rows: {len(df_cleaned)}, columns: {len(df_cleaned.columns)}")
    print(f"    Null values count: {df_cleaned.isnull().sum().sum()}")
    
    # 6. Execute key queries from 04_analysis_queries.sql to verify findings
    print("\n" + "="*70)
    print("SQL ANALYTICAL FINDINGS REPORT (PwC CONSULTING SIMULATION)")
    print("="*70)
    
    # KPI Summary
    q1 = """
    SELECT 
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_at_risk,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM cleaned_customers;
    """
    res1 = pd.read_sql_query(q1, conn)
    print("\n[KPI Portfolio Summary]:")
    print(res1.to_string(index=False))
    
    # Contract Analysis
    q2 = """
    SELECT 
        Contract,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM cleaned_customers
    GROUP BY Contract
    ORDER BY churn_rate_pct DESC;
    """
    res2 = pd.read_sql_query(q2, conn)
    print("\n[Churn by Contract Type]:")
    print(res2.to_string(index=False))
    
    # Internet Service
    q3 = """
    SELECT 
        InternetService,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM cleaned_customers
    GROUP BY InternetService
    ORDER BY churn_rate_pct DESC;
    """
    res3 = pd.read_sql_query(q3, conn)
    print("\n[Churn by Internet Service Architecture]:")
    print(res3.to_string(index=False))
    
    # Tenure Group
    q5 = """
    SELECT 
        tenure_group,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM cleaned_customers
    GROUP BY tenure_group
    ORDER BY tenure_group ASC;
    """
    res5 = pd.read_sql_query(q5, conn)
    print("\n[Churn by Tenure Cohort]:")
    print(res5.to_string(index=False))

    # Payment Method
    q6 = """
    SELECT 
        PaymentMethod,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM cleaned_customers
    GROUP BY PaymentMethod
    ORDER BY churn_rate_pct DESC;
    """
    res6 = pd.read_sql_query(q6, conn)
    print("\n[Churn by Payment Method]:")
    print(res6.to_string(index=False))
    
    # Add-on Services Count
    q7 = """
    SELECT 
        total_services_count,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM cleaned_customers
    GROUP BY total_services_count
    ORDER BY total_services_count ASC;
    """
    res7 = pd.read_sql_query(q7, conn)
    print("\n[Churn by Service Depth (0-6 Add-ons)]:")
    print(res7.to_string(index=False))
    
    conn.close()
    print("\n[+] SQL Pipeline successfully executed and verified!")

if __name__ == "__main__":
    run_pipeline()
