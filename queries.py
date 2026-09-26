"""queries.py -- SQL validation suite and monthly metrics aggregation."""
import sqlite3
import pandas as pd

def run_validations(db_path: str = "pharmeasy.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("==================================================")
    print("TASK 2.2: JOIN VALIDATION & DATA INTEGRITY CHECKS")
    print("==================================================")

    # 1. Row-count check: LEFT JOIN vs INNER JOIN
    left_join_count = cur.execute("""
        SELECT COUNT(*) FROM regions_master r
        LEFT JOIN orders_clean o ON r.region = o.region;
    """).fetchone()[0]

    inner_join_count = cur.execute("""
        SELECT COUNT(*) FROM regions_master r
        INNER JOIN orders_clean o ON r.region = o.region;
    """).fetchone()[0]

    print(f"\n1. Row Count Comparison:")
    print(f"   - LEFT JOIN count:  {left_join_count}")
    print(f"   - INNER JOIN count: {inner_join_count}")
    print(f"   - Row Delta:        {left_join_count - inner_join_count} (Corresponds to Kurnool's zero-order row)")

    # 2. Duplicate key check
    dup_keys = cur.execute("""
        SELECT order_id, COUNT(*) FROM orders_clean
        GROUP BY order_id HAVING COUNT(*) > 1;
    """).fetchall()
    print(f"\n2. Duplicate Key Check on order_id:")
    print(f"   - Number of duplicate order_ids: {len(dup_keys)}")

    # 3. Null check & Pitfall demonstration
    print(f"\n3. Null Check: COUNT(*) vs COUNT(o.order_id) Pitfall:")
    pitfall_df = pd.read_sql_query("""
        SELECT 
            r.region,
            r.state,
            COUNT(*) AS count_star,
            COUNT(o.order_id) AS count_fk
        FROM regions_master r
        LEFT JOIN orders_clean o ON r.region = o.region
        GROUP BY r.region, r.state
        ORDER BY count_fk ASC;
    """, conn)
    print(pitfall_df.to_string(index=False))

    print("\n   [!] PITFALL ALERT: Notice Kurnool above:")
    print("       COUNT(*) incorrectly counts the null-padded row as 1.")
    print("       COUNT(o.order_id) correctly ignores NULL and returns 0.")

    # 4. Per-region order counts
    print(f"\n4. Verified Per-Region Order Counts:")
    region_counts = pd.read_sql_query("""
        SELECT 
            r.region, 
            r.tier, 
            COUNT(o.order_id) AS verified_orders
        FROM regions_master r
        LEFT JOIN orders_clean o ON r.region = o.region
        GROUP BY r.region, r.tier
        ORDER BY verified_orders ASC;
    """, conn)
    print(region_counts.to_string(index=False))

    print("\n==================================================")
    print("TASK 2.3: REGION X MONTH SALES & MoM GROWTH")
    print("==================================================")

    monthly_sales = pd.read_sql_query("""
        SELECT 
            r.region,
            SUBSTR(o.order_date, 1, 7) AS month,
            ROUND(SUM(o.sales_inr), 2) AS total_sales,
            ROUND(SUM(o.profit_inr), 2) AS total_profit,
            COUNT(o.order_id) AS order_count
        FROM regions_master r
        INNER JOIN orders_clean o ON r.region = o.region
        GROUP BY r.region, month
        ORDER BY r.region, month;
    """, conn)

    # Pivot for clean comparison
    sales_pivot = monthly_sales.pivot(index="region", columns="month", values="total_sales").fillna(0)
    sales_pivot["Apr->May %"] = ((sales_pivot["2026-05"] - sales_pivot["2026-04"]) / sales_pivot["2026-04"] * 100).round(2)
    sales_pivot["May->Jun %"] = ((sales_pivot["2026-06"] - sales_pivot["2026-05"]) / sales_pivot["2026-05"] * 100).round(2)

    print("\nMonthly Sales (INR) and MoM Growth:")
    print(sales_pivot.to_string())

    conn.close()
    return sales_pivot

if __name__ == "__main__":
    run_validations()