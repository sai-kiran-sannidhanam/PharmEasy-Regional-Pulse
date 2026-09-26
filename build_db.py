"""build_db.py -- Builds local SQLite database from cleaned CSV files."""
import sqlite3
import pandas as pd

def build_database(db_path: str = "pharmeasy.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Drop existing tables
    cur.execute("DROP TABLE IF EXISTS orders_clean;")
    cur.execute("DROP TABLE IF EXISTS regions_master;")

    # Create tables
    cur.execute("""
    CREATE TABLE regions_master (
        region TEXT PRIMARY KEY,
        state TEXT NOT NULL,
        tier TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE orders_clean (
        order_id TEXT PRIMARY KEY,
        order_date TEXT NOT NULL,
        region TEXT NOT NULL,
        category TEXT NOT NULL,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        sales_inr REAL NOT NULL,
        profit_inr REAL NOT NULL,
        FOREIGN KEY (region) REFERENCES regions_master (region)
    );
    """)

    # Load data
    regions_df = pd.read_csv("regions_master.csv")
    orders_df = pd.read_csv("orders_clean.csv")

    regions_df.to_sql("regions_master", conn, if_exists="append", index=False)
    orders_df.to_sql("orders_clean", conn, if_exists="append", index=False)

    conn.commit()

    # Verify counts
    r_count = cur.execute("SELECT COUNT(*) FROM regions_master;").fetchone()[0]
    o_count = cur.execute("SELECT COUNT(*) FROM orders_clean;").fetchone()[0]
    print(f"Successfully built {db_path}:")
    print(f" - regions_master: {r_count} rows (Expected: 10)")
    print(f" - orders_clean:   {o_count} rows (Expected: 2100)")

    conn.close()

if __name__ == "__main__":
    build_database()