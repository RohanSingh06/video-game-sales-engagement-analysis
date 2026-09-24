import pandas as pd
import re
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "vgsales.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "vgsales_cleaned.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("VGSALES.CSV DATA CLEANING")
print("=" * 70)

vgsales = pd.read_csv(RAW_FILE)

print("\nOriginal shape:")
print(vgsales.shape)


# ============================================================
# 1. CLEAN COLUMN NAMES
# ============================================================

vgsales.columns = vgsales.columns.str.strip()


# ============================================================
# 2. CLEAN TEXT COLUMNS
# ============================================================

text_columns = [
    "Name",
    "Platform",
    "Genre",
    "Publisher"
]

for column in text_columns:

    vgsales[column] = (
        vgsales[column]
        .astype("string")
        .str.strip()
    )


# ============================================================
# 3. HANDLE MISSING PUBLISHER
# ============================================================

vgsales["Publisher"] = vgsales["Publisher"].fillna("Unknown")


# ============================================================
# 4. CLEAN PLATFORM VALUES
# ============================================================

vgsales["Platform"] = (
    vgsales["Platform"]
    .str.upper()
    .str.strip()
)


# ============================================================
# 5. CLEAN GENRE VALUES
# ============================================================

vgsales["Genre"] = (
    vgsales["Genre"]
    .str.strip()
)


# ============================================================
# 6. CLEAN PUBLISHER VALUES
# ============================================================

vgsales["Publisher"] = (
    vgsales["Publisher"]
    .str.strip()
)


# ============================================================
# 7. CLEAN YEAR
# ============================================================

vgsales["Year"] = pd.to_numeric(
    vgsales["Year"],
    errors="coerce"
)

# Keep missing years as missing.
# Do not invent years.

vgsales["Year"] = vgsales["Year"].astype("Int64")


# ============================================================
# 8. CREATE NORMALIZED GAME NAME
# ============================================================

def normalize_title(title):

    if pd.isna(title):
        return ""

    title = str(title)

    title = title.lower()

    title = title.strip()

    title = re.sub(r"\s+", " ", title)

    # Remove punctuation
    title = re.sub(r"[^a-z0-9\s]", "", title)

    # Remove extra spaces
    title = re.sub(r"\s+", " ", title)

    return title.strip()


vgsales["Normalized_Name"] = (
    vgsales["Name"]
    .apply(normalize_title)
)


# ============================================================
# 9. SALES COLUMNS
# ============================================================

sales_columns = [
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales"
]

for column in sales_columns:

    vgsales[column] = pd.to_numeric(
        vgsales[column],
        errors="coerce"
    )


# ============================================================
# 10. CREATE TOTAL REGIONAL SALES
# ============================================================

vgsales["Calculated_Global_Sales"] = (
    vgsales["NA_Sales"]
    + vgsales["EU_Sales"]
    + vgsales["JP_Sales"]
    + vgsales["Other_Sales"]
)


# ============================================================
# 11. CHECK SALES CONSISTENCY
# ============================================================

vgsales["Sales_Difference"] = (
    vgsales["Global_Sales"]
    - vgsales["Calculated_Global_Sales"]
).abs()

sales_mismatch_count = (
    vgsales["Sales_Difference"] > 0.01
).sum()

print("\nSales records with difference > 0.01:")
print(sales_mismatch_count)


# ============================================================
# 12. REMOVE SALES VALIDATION HELPER COLUMNS
# ============================================================

vgsales = vgsales.drop(
    columns=[
        "Calculated_Global_Sales",
        "Sales_Difference"
    ]
)


# ============================================================
# 13. CHECK DUPLICATES
# ============================================================

duplicate_rows = vgsales.duplicated().sum()

print("\nDuplicate rows:")
print(duplicate_rows)


# ============================================================
# 14. CHECK MISSING VALUES
# ============================================================

print("\nMissing values after cleaning:")
print(vgsales.isnull().sum())


# ============================================================
# 15. CHECK DATA TYPES
# ============================================================

print("\nData types after cleaning:")
print(vgsales.dtypes)


# ============================================================
# 16. CHECK CATEGORICAL VALUES
# ============================================================

print("\nNumber of unique platforms:")
print(vgsales["Platform"].nunique())

print("\nNumber of unique genres:")
print(vgsales["Genre"].nunique())

print("\nNumber of unique publishers:")
print(vgsales["Publisher"].nunique())

print("\nTop 15 platforms:")
print(vgsales["Platform"].value_counts().head(15))

print("\nTop 15 genres:")
print(vgsales["Genre"].value_counts().head(15))


# ============================================================
# 17. SALES SUMMARY
# ============================================================

print("\nSales summary:")

print(
    vgsales[
        [
            "NA_Sales",
            "EU_Sales",
            "JP_Sales",
            "Other_Sales",
            "Global_Sales"
        ]
    ].describe()
)


# ============================================================
# 18. SAVE CLEANED DATA
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

vgsales.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CLEANED VGSALES DATASET")
print("=" * 70)

print("\nFinal shape:")
print(vgsales.shape)

print("\nColumns:")
print(list(vgsales.columns))

print("\nSample cleaned data:")
print(vgsales.head())

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("PHASE 3B VGSALES CLEANING COMPLETED")
print("=" * 70)