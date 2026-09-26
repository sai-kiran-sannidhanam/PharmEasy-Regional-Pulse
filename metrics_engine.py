"""metrics_engine.py -- Operational alert flagging engine and state persistence."""
import json
import sqlite3
from typing import Dict, List

def compute_percentage_change_v1(current: float, previous: float) -> float:
    """Computes percentage change, safely returning 0.0 on division by zero."""
    if previous is None or previous == 0:
        return 0.0
    return round(((current - previous) / previous) * 100.0, 2)

def flag_significant_regions_v1(changes: Dict[str, float], threshold: float = 8.0) -> Dict[str, dict]:
    """Flags regions whose absolute percentage change exceeds the alert threshold."""
    flagged = {}
    for region, change in changes.items():
        if abs(change) > threshold:
            flagged[region] = {
                "change_pct": change,
                "flagged": True,
                "direction": "SURGE" if change > 0 else "DROP"
            }
    return flagged

def save_state_v1(month_summary: dict, path: str):
    """Persists computed monthly metrics summary as JSON."""
    with open(path, "w") as f:
        json.dump(month_summary, f, indent=2)

def load_previous_state_v1(path: str) -> dict:
    """Loads previous monthly metrics summary from JSON."""
    with open(path, "r") as f:
        return json.load(f)

def run_metrics_pipeline(db_path: str = "pharmeasy.db"):
    conn = sqlite3.connect(db_path)
    
    # Query monthly sales per region
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT 
            r.region,
            SUBSTR(o.order_date, 1, 7) AS month,
            ROUND(SUM(o.sales_inr), 2) AS total_sales,
            ROUND(SUM(o.profit_inr), 2) AS total_profit,
            COUNT(o.order_id) AS order_count
        FROM regions_master r
        LEFT JOIN orders_clean o ON r.region = o.region
        GROUP BY r.region, month;
    """).fetchall()
    conn.close()

    monthly_data = {"2026-04": {}, "2026-05": {}, "2026-06": {}}
    for region, month, sales, profit, count in rows:
        if month:
            monthly_data[month][region] = {
                "sales": sales or 0.0,
                "profit": profit or 0.0,
                "orders": count or 0
            }

    # Save state files
    save_state_v1(monthly_data["2026-04"], "state_2026_04.json")
    save_state_v1(monthly_data["2026-05"], "state_2026_05.json")
    save_state_v1(monthly_data["2026-06"], "state_2026_06.json")

    # Compute changes: Apr -> May
    apr_state = load_previous_state_v1("state_2026_04.json")
    may_state = load_previous_state_v1("state_2026_05.json")
    jun_state = load_previous_state_v1("state_2026_06.json")

    changes_apr_may = {}
    for r in apr_state:
        changes_apr_may[r] = compute_percentage_change_v1(may_state[r]["sales"], apr_state[r]["sales"])

    changes_may_jun = {}
    for r in may_state:
        changes_may_jun[r] = compute_percentage_change_v1(jun_state[r]["sales"], may_state[r]["sales"])

    flagged_apr_may = flag_significant_regions_v1(changes_apr_may, threshold=8.0)
    flagged_may_jun = flag_significant_regions_v1(changes_may_jun, threshold=8.0)

    print("April -> May Flagged Regions (threshold > 8%):")
    for r, info in sorted(flagged_apr_may.items()):
        print(f"  - {r:15}: {info['change_pct']:+6.2f}% ({info['direction']})")

    print("\nMay -> June Flagged Regions (threshold > 8%):")
    for r, info in sorted(flagged_may_jun.items()):
        print(f"  - {r:15}: {info['change_pct']:+6.2f}% ({info['direction']})")

    return {
        "monthly_data": monthly_data,
        "flagged_apr_may": flagged_apr_may,
        "flagged_may_jun": flagged_may_jun,
    }

if __name__ == "__main__":
    run_metrics_pipeline()