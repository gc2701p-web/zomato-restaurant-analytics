"""
# -*- coding: utf-8 -*-
explore_data.py
---------------
Reads the restaurant CSV file and displays its full structure:
  - Shape (rows x columns)
  - Column names and data types
  - First & last few rows
  - Missing value summary
  - Numeric column statistics
  - Categorical column value counts
"""

import os
import sys
import pandas as pd

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Path configuration ────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH  = os.path.join(BASE_DIR, "data", "raw", "restaurant_data.csv")

# ── Helper ────────────────────────────────────────────────────────────────────
DIVIDER = "─" * 60

def section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


# ── Load ──────────────────────────────────────────────────────────────────────
def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found at: {path}")
    df = pd.read_csv(path)
    print(f"\n[OK] Loaded: {path}")
    return df


# ── Inspection functions ──────────────────────────────────────────────────────
def show_shape(df: pd.DataFrame) -> None:
    section("SHAPE")
    rows, cols = df.shape
    print(f"  Rows    : {rows:,}")
    print(f"  Columns : {cols}")


def show_columns(df: pd.DataFrame) -> None:
    section("COLUMNS & DATA TYPES")
    col_info = pd.DataFrame({
        "Column"   : df.columns,
        "Dtype"    : df.dtypes.values,
        "Non-Null" : df.notna().sum().values,
        "Null"     : df.isna().sum().values,
    })
    print(col_info.to_string(index=False))


def show_sample(df: pd.DataFrame, n: int = 5) -> None:
    section(f"FIRST {n} ROWS")
    print(df.head(n).to_string(index=False))

    section(f"LAST {n} ROWS")
    print(df.tail(n).to_string(index=False))


def show_missing(df: pd.DataFrame) -> None:
    section("MISSING VALUES")
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print("  No missing values found.")
    else:
        pct = (missing / len(df) * 100).round(2)
        result = pd.DataFrame({"Missing Count": missing, "Missing %": pct})
        print(result.to_string())


def show_numeric_stats(df: pd.DataFrame) -> None:
    section("NUMERIC COLUMN STATISTICS")
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        print("  No numeric columns found.")
    else:
        print(numeric_df.describe().round(2).to_string())


def show_categorical_counts(df: pd.DataFrame, max_unique: int = 20) -> None:
    section("CATEGORICAL COLUMN VALUE COUNTS")
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    if len(cat_cols) == 0:
        print("  No categorical columns found.")
        return
    for col in cat_cols:
        n_unique = df[col].nunique()
        print(f"\n  [{col}]  -  {n_unique} unique value(s)")
        if n_unique <= max_unique:
            counts = df[col].value_counts()
            for val, cnt in counts.items():
                bar = "#" * cnt
                print(f"    {str(val):<20} {cnt:>4}  {bar}")
        else:
            print(f"    (Too many unique values - top 10 shown)")
            for val, cnt in df[col].value_counts().head(10).items():
                print(f"    {str(val):<30} {cnt:>4}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    print("=" * 60)
    print("   RESTAURANT DATA - STRUCTURAL OVERVIEW")
    print("=" * 60)

    df = load_csv(CSV_PATH)

    show_shape(df)
    show_columns(df)
    show_sample(df)
    show_missing(df)
    show_numeric_stats(df)
    show_categorical_counts(df)

    print(f"\n{'=' * 60}")
    print("   Exploration complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
