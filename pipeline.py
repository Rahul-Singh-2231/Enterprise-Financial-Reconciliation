"""
Enterprise Financial Data Architecture & Revenue Reconciliation Pipeline
Author: Rahul Singh (rahulsinghrajput2231@gmail.com)
Role: Data Analyst
Description: End-to-end automated ETL and financial reconciliation pipeline
integrating SQLite customer state history, semi-structured server logs, and
daily FX foreign exchange market rates.
"""

import sqlite3
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_pipeline():
    print("=" * 70)
    print("STARTING ENTERPRISE FINANCIAL DATA RECONCILIATION PIPELINE")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # PHASE 1: SQL EXTRACTION (SLOWLY CHANGING DIMENSIONS & ACTIVE CUSTOMERS)
    # -------------------------------------------------------------------------
    print("\n[PHASE 1] Extracting verified active customer states from SQLite...")
    conn = sqlite3.connect('enterprise_database.db')
    query_active_users = """
    WITH RankedUsers AS (
        SELECT 
            user_id,
            name,
            status,
            updated_at,
            ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
        FROM users
    )
    SELECT 
        user_id,
        name,
        status,
        updated_at
    FROM RankedUsers
    WHERE rn = 1 AND status = 'Active';
    """
    df_active_users = pd.read_sql(query_active_users, conn)
    conn.close()

    df_active_users['User ID'] = df_active_users['user_id']
    
    # Validations
    assert len(df_active_users) == df_active_users['user_id'].nunique(), "Duplicate active user IDs detected!"
    assert (df_active_users['status'] == 'Active').all(), "Non-active user status found in extraction!"
    print(f"  -> Extracted {len(df_active_users):,} unique active customer records (Deduplicated with zero errors).")

    # -------------------------------------------------------------------------
    # PHASE 2: REGEX & UNSTRUCTURED DATA WRANGLING
    # -------------------------------------------------------------------------
    print("\n[PHASE 2] Parsing 100,000 raw server logs using vectorized regex...")
    df_logs_raw = pd.read_csv('server_logs.txt')
    total_raw_logs = len(df_logs_raw)

    # Filter out system error logs
    clean_logs = df_logs_raw[~df_logs_raw['Raw_Server_Log'].str.contains("ERROR", na=False)].copy()
    error_logs_dropped = total_raw_logs - len(clean_logs)

    # Vectorized regex extraction with named capture groups
    log_regex_pattern = r'\[(?P<Date>\d{4}-\d{2}-\d{2})[^\]]*\]\s*INFO:.*?"u":\s*"(?P<User_ID>[^"]+)".*?"item_code":\s*"(?P<Product_ID>[^"]+)".*?"eur_val":\s*(?P<Euro_Value>[\d\.]+)'
    extracted_data = clean_logs['Raw_Server_Log'].str.extract(log_regex_pattern)
    extracted_data['Euro_Value'] = extracted_data['Euro_Value'].astype(float)
    extracted_data.rename(columns={
        'User_ID': 'User ID',
        'Product_ID': 'Product ID',
        'Euro_Value': 'Euro Value'
    }, inplace=True)

    assert extracted_data.isnull().sum().sum() == 0, "Missing values found in log extraction!"
    assert len(extracted_data) == 94902, f"Expected 94,902 clean transactions, found {len(extracted_data)}"
    print(f"  -> Processed {total_raw_logs:,} total raw lines.")
    print(f"  -> Filtered {error_logs_dropped:,} system failure ERROR logs.")
    print(f"  -> Extracted {len(extracted_data):,} valid transactions with 100% match rate (0 nulls).")

    # -------------------------------------------------------------------------
    # PHASE 3: FINANCIAL RECONCILIATION & FX TEMPORAL FORWARD-FILL
    # -------------------------------------------------------------------------
    print("\n[PHASE 3] Reconciling temporal FX market gap & multi-source merging...")
    rates_df = pd.read_csv('daily_exchange_rates.csv')
    rates_df['Date'] = rates_df['Date'].astype(str)
    weekend_nulls_before = rates_df['EUR_to_USD'].isnull().sum()

    # Forward-fill weekend market closures
    rates_df['EUR_to_USD'] = rates_df['EUR_to_USD'].ffill()
    weekend_nulls_after = rates_df['EUR_to_USD'].isnull().sum()

    # Join transactions with FX rates
    merged_rates = pd.merge(extracted_data, rates_df, on='Date', how='inner')
    assert len(merged_rates) == len(extracted_data), "Data loss occurred during FX rate join!"

    # Merge with active customer records
    df_final = pd.merge(
        merged_rates,
        df_active_users[['user_id', 'User ID', 'name', 'status', 'updated_at']],
        on='User ID',
        how='inner'
    )

    # Compute USD revenue
    df_final['USD_Revenue'] = df_final['Euro Value'] * df_final['EUR_to_USD']
    total_revenue = df_final['USD_Revenue'].sum()

    print(f"  -> Handled {weekend_nulls_before} weekend market gaps via .ffill() (Retained 100% weekend purchases).")
    print(f"  -> Reconciled {len(df_final):,} active customer transactions.")
    print(f"  -> AUDITED TOTAL GENUINE REVENUE: ${total_revenue:,.2f} USD")

    # -------------------------------------------------------------------------
    # PHASE 4: AGGREGATION & VISUALIZATION (CFO DASHBOARD)
    # -------------------------------------------------------------------------
    print("\n[PHASE 4] Computing monthly revenue trajectory and top customer spend...")
    df_final['Month'] = pd.to_datetime(df_final['Date']).dt.to_period('M').astype(str)
    monthly_rev = df_final.groupby('Month')['USD_Revenue'].sum().reset_index()
    
    customer_rev = df_final.groupby(['user_id', 'name'])['USD_Revenue'].sum().reset_index()
    top_5_cust = customer_rev.sort_values(by='USD_Revenue', ascending=False).head(5)

    print("\n=== Monthly Revenue Trajectory ===")
    for _, row in monthly_rev.iterrows():
        print(f"  {row['Month']}: ${row['USD_Revenue']:,.2f}")

    print("\n=== Top 5 Most Valuable Customers ===")
    for _, row in top_5_cust.iterrows():
        print(f"  {row['user_id']} ({row['name']}): ${row['USD_Revenue']:,.2f}")

    # Generate and save high-resolution dashboard
    os.makedirs('assets', exist_ok=True)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    # Chart 1: Monthly USD Revenue
    ax1 = axes[0]
    bars1 = ax1.bar(
        monthly_rev['Month'],
        monthly_rev['USD_Revenue'] / 1e6,
        color='#1f77b4',
        edgecolor='#0d47a1',
        linewidth=1.2,
        alpha=0.85
    )
    ax1.plot(
        monthly_rev['Month'],
        monthly_rev['USD_Revenue'] / 1e6,
        color='#d62728',
        marker='o',
        linewidth=2.5,
        markersize=7,
        label='Monthly Trend'
    )
    ax1.set_title('Total USD Revenue by Month (2023)', fontsize=14, fontweight='bold', pad=12)
    ax1.set_xlabel('Month', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Total Revenue (Millions USD)', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, max(monthly_rev['USD_Revenue'] / 1e6) * 1.22)
    ax1.tick_params(axis='x', rotation=45, labelsize=9.5)
    ax1.legend(loc='upper right', frameon=True)
    ax1.bar_label(bars1, fmt='$%.2fM', padding=3, fontweight='bold', fontsize=8.5)

    # Chart 2: Top 5 Customers
    ax2 = axes[1]
    bars2 = ax2.bar(
        top_5_cust['user_id'],
        top_5_cust['USD_Revenue'],
        color='#2ca02c',
        edgecolor='#1b5e20',
        linewidth=1.2,
        alpha=0.85
    )
    ax2.set_title('Top 5 Most Valuable Customers by Total USD Spend', fontsize=14, fontweight='bold', pad=12)
    ax2.set_xlabel('Customer ID', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Total Spend (USD)', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, max(top_5_cust['USD_Revenue']) * 1.15)
    ax2.tick_params(axis='x', labelsize=10)
    customer_labels = [f'${val:,.2f}' for val in top_5_cust['USD_Revenue']]
    ax2.bar_label(bars2, labels=customer_labels, padding=3, fontweight='bold', fontsize=8.5)

    plt.tight_layout()
    chart_path = os.path.join('assets', 'cfo_revenue_dashboard.png')
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"\nSaved dashboard visualization to: {chart_path}")
    print("=" * 70)
    print("PIPELINE EXECUTED SUCCESSFULLY - AUDIT COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    run_pipeline()
