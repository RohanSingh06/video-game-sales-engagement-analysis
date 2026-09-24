import pandas as pd
import ast
import re
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "games.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "games_cleaned.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("GAMES.CSV DATA CLEANING")
print("=" * 70)

games = pd.read_csv(RAW_FILE)

print("\nOriginal shape:")
print(games.shape)


# ============================================================
# 1. REMOVE SOURCE INDEX COLUMN
# ============================================================

if "Unnamed: 0" in games.columns:
    games = games.drop(columns=["Unnamed: 0"])

    print("\nRemoved column:")
    print("Unnamed: 0")


# ============================================================
# 2. CLEAN TEXT COLUMNS
# ============================================================

text_columns = [
    "Title",
    "Team",
    "Genres",
    "Summary",
    "Reviews"
]

for column in text_columns:

    if column in games.columns:

        games[column] = games[column].astype("string").str.strip()


# ============================================================
# 3. HANDLE MISSING TEAM
# ============================================================

games["Team"] = games["Team"].fillna("Unknown")


# ============================================================
# 4. HANDLE MISSING SUMMARY
# ============================================================

games["Summary"] = games["Summary"].fillna("Unknown")


# ============================================================
# 5. CONVERT RELEASE DATE
# ============================================================

games["Release Date"] = pd.to_datetime(
    games["Release Date"],
    errors="coerce"
)

print("\nRelease Date converted to datetime.")


# ============================================================
# 6. CONVERT K NOTATION TO NUMERIC
# ============================================================

def convert_count(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    # Remove commas
    value = value.replace(",", "")

    # Handle K notation
    if value.lower().endswith("k"):

        number = value[:-1].strip()

        try:
            return float(number) * 1000
        except ValueError:
            return None

    # Handle normal numeric values
    try:
        return float(value)

    except ValueError:
        return None


count_columns = [
    "Times Listed",
    "Number of Reviews",
    "Plays",
    "Playing",
    "Backlogs",
    "Wishlist"
]

for column in count_columns:

    games[column] = games[column].apply(convert_count)

    games[column] = games[column].astype("float64")


# ============================================================
# 7. CLEAN GENRES
# ============================================================

def clean_list_string(value):

    if pd.isna(value):
        return "Unknown"

    value = str(value).strip()

    if value == "":
        return "Unknown"

    try:

        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):

            cleaned = []

            for item in parsed:

                item = str(item).strip()

                if item:
                    cleaned.append(item)

            return ", ".join(cleaned)

    except (ValueError, SyntaxError):

        pass

    return value


games["Genres"] = games["Genres"].apply(clean_list_string)


# ============================================================
# 8. CLEAN TEAM / DEVELOPERS
# ============================================================

games["Team"] = games["Team"].apply(clean_list_string)


# ============================================================
# 9. CREATE NORMALIZED TITLE
# ============================================================

def normalize_title(title):

    if pd.isna(title):
        return ""

    title = str(title)

    title = title.lower()

    title = title.strip()

    title = re.sub(r"\s+", " ", title)

    title = re.sub(r"[^a-z0-9\s]", "", title)

    title = re.sub(r"\s+", " ", title)

    return title.strip()


games["Normalized_Title"] = games["Title"].apply(normalize_title)


# ============================================================
# 10. CREATE USEFUL DATE COLUMNS
# ============================================================

games["Release_Year"] = games["Release Date"].dt.year

games["Release_Month"] = games["Release Date"].dt.month

games["Release_Month_Name"] = games["Release Date"].dt.month_name()


# ============================================================
# 11. CHECK DUPLICATES
# ============================================================

duplicate_rows = games.duplicated().sum()

print("\nDuplicate rows after cleaning:")
print(duplicate_rows)


# ============================================================
# 12. CHECK MISSING VALUES
# ============================================================

print("\nMissing values after cleaning:")
print(games.isnull().sum())


# ============================================================
# 13. DATA TYPES
# ============================================================

print("\nData types after cleaning:")
print(games.dtypes)


# ============================================================
# 14. SAVE CLEANED DATA
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

games.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CLEANED GAMES DATASET")
print("=" * 70)

print("\nFinal shape:")
print(games.shape)

print("\nColumns:")
print(list(games.columns))

print("\nSample cleaned data:")
print(games.head())

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("PHASE 3A GAMES CLEANING COMPLETED")
print("=" * 70)