"""clean_data.py -- PharmEasy Regional Pulse data cleaning and validation module."""
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "order_id", "order_date", "region", "category",
    "product", "quantity", "sales_inr", "profit_inr"
]

def validate_schema(df: pd.DataFrame, required_columns: list) -> dict:
    """Validates dataframe schema against required columns."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        return {
            "status": "blocked_schema",
            "row_count": len(df),
            "missing_columns": missing
        }
    return {
        "status": "validated",
        "row_count": len(df),
        "missing_columns": []
    }

def clean_pipeline(raw_csv_path: str = "pharmeasy_orders_raw.csv") -> pd.DataFrame:
    print(f"[1/5] Loading raw data from {raw_csv_path}...")
    df = pd.read_csv(raw_csv_path, dtype={"quantity": "Int64"}, keep_default_na=False)
    initial_rows = len(df)
    print(f"      Initial raw row count: {initial_rows}")

    # Step 1: Remove exact duplicates across all 8 columns
    df_dedup = df.drop_duplicates().copy()
    duplicates_removed = initial_rows - len(df_dedup)
    print(f"[2/5] Deduplication: Removed {duplicates_removed} exact duplicates. Rows remaining: {len(df_dedup)}")

    # Step 2: Normalize region strings
    raw_variants_count = df_dedup['region'].nunique()
    df_dedup['region'] = df_dedup['region'].astype(str).str.strip().str.title()
    normalized_variants_count = df_dedup['region'].nunique()
    print(f"[3/5] Normalization: Collapsed {raw_variants_count} raw region variants into {normalized_variants_count} canonical regions.")

    # Step 3: Impute missing category using deterministic Product -> Category lookup
    missing_cat_before = (df_dedup['category'] == "").sum()
    valid_cat_df = df_dedup[df_dedup['category'] != ""]
    prod_to_cat = valid_cat_df.groupby('product')['category'].first().to_dict()
    df_dedup['category'] = df_dedup.apply(
        lambda row: prod_to_cat[row['product']] if row['category'] == "" else row['category'],
        axis=1
    )
    missing_cat_after = (df_dedup['category'] == "").sum()
    print(f"[4/5] Category Imputation: Resolved {missing_cat_before} missing categories. Remaining missing: {missing_cat_after}")

    # Step 4: Impute missing profit_inr using category mean profit margin
    df_dedup['sales_inr'] = pd.to_numeric(df_dedup['sales_inr'])
    df_dedup['profit_inr'] = pd.to_numeric(df_dedup['profit_inr'].replace("", np.nan))
    
    missing_profit_before = df_dedup['profit_inr'].isna().sum()
    known_profit_df = df_dedup[df_dedup['profit_inr'].notna()].copy()
    cat_margin_series = known_profit_df.groupby('category').apply(
        lambda g: (g['profit_inr'] / g['sales_inr']).mean()
    )
    cat_margins = cat_margin_series.to_dict()

    def impute_profit(row):
        if pd.isna(row['profit_inr']):
            margin = cat_margins[row['category']]
            return round(row['sales_inr'] * margin, 2)
        return row['profit_inr']

    df_dedup['profit_inr'] = df_dedup.apply(impute_profit, axis=1)
    missing_profit_after = df_dedup['profit_inr'].isna().sum()
    print(f"[5/5] Profit Imputation: Imputed {missing_profit_before} missing profit values. Remaining missing: {missing_profit_after}")

    return df_dedup

if __name__ == "__main__":
    cleaned_df = clean_pipeline()
    
    # Run Schema Validation on Clean Data
    clean_val = validate_schema(cleaned_df, REQUIRED_COLUMNS)
    print("\nSchema Validation on Clean Data:", clean_val)
    assert clean_val["status"] == "validated", "Clean data failed schema check!"

    # Run Schema Validation on Broken Copy
    broken_df = cleaned_df.drop(columns=["profit_inr"])
    broken_val = validate_schema(broken_df, REQUIRED_COLUMNS)
    print("Schema Validation on Broken Copy:", broken_val)
    assert broken_val["status"] == "blocked_schema", "Broken data should fail schema check!"
    assert "profit_inr" in broken_val["missing_columns"], "Missing column not identified correctly!"

    # Save to orders_clean.csv
    cleaned_df.to_csv("orders_clean.csv", index=False)
    print(f"\nSuccessfully written orders_clean.csv with {len(cleaned_df)} verified rows.")