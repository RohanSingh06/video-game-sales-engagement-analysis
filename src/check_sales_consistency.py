import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "vgsales_cleaned.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("VGSALES SALES CONSISTENCY CHECK")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)


# ============================================================
# CALCULATE REGIONAL TOTAL
# ============================================================

df["Calculated_Global_Sales"] = (
    df["NA_Sales"]
    + df["EU_Sales"]
    + df["JP_Sales"]
    + df["Other_Sales"]
)


# ============================================================
# CALCULATE DIFFERENCE
# ============================================================

df["Sales_Difference"] = (
    df["Global_Sales"]
    - df["Calculated_Global_Sales"]
).abs()


# ============================================================
# SUMMARY
# ============================================================

print("\nDifference statistics:")

print(
    df["Sales_Difference"].describe()
)


# ============================================================
# DIFFERENCE THRESHOLDS
# ============================================================

print("\nRecords exceeding different thresholds:")

for threshold in [0.001, 0.01, 0.02, 0.05, 0.10, 0.50]:

    count = (
        df["Sales_Difference"] > threshold
    ).sum()

    print(
        f"Difference > {threshold:.3f}: {count}"
    )


# ============================================================
# LARGEST DIFFERENCES
# ============================================================

print("\nTop 20 largest sales differences:")

columns = [
    "Rank",
    "Name",
    "Platform",
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales",
    "Calculated_Global_Sales",
    "Sales_Difference"
]

print(
    df[
        columns
    ]
    .sort_values(
        "Sales_Difference",
        ascending=False
    )
    .head(20)
    .to_string(index=False)
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("SALES CONSISTENCY CHECK COMPLETED")
print("=" * 70)