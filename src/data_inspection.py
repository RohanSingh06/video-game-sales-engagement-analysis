import pandas as pd


# ============================================================
# VIDEO GAME SALES AND ENGAGEMENT ANALYSIS
# PHASE 1 - DATASET INSPECTION
# ============================================================


# ------------------------------------------------------------
# 1. Load datasets
# ------------------------------------------------------------

games_path = "data/raw/games.csv"
vgsales_path = "data/raw/vgsales.csv"

games = pd.read_csv(games_path)
vgsales = pd.read_csv(vgsales_path)


# ------------------------------------------------------------
# 2. Basic information
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("GAMES.CSV")
print("=" * 70)

print("\nShape:")
print(games.shape)

print("\nColumns:")
print(games.columns.tolist())

print("\nData Types:")
print(games.dtypes)


print("\n" + "=" * 70)
print("VGSALES.CSV")
print("=" * 70)

print("\nShape:")
print(vgsales.shape)

print("\nColumns:")
print(vgsales.columns.tolist())

print("\nData Types:")
print(vgsales.dtypes)


# ------------------------------------------------------------
# 3. First 5 rows
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FIRST 5 ROWS - GAMES")
print("=" * 70)

print(games.head())


print("\n" + "=" * 70)
print("FIRST 5 ROWS - VGSALES")
print("=" * 70)

print(vgsales.head())


# ------------------------------------------------------------
# 4. Missing values
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MISSING VALUES - GAMES")
print("=" * 70)

print(games.isnull().sum())


print("\n" + "=" * 70)
print("MISSING VALUES - VGSALES")
print("=" * 70)

print(vgsales.isnull().sum())


# ------------------------------------------------------------
# 5. Duplicate rows
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DUPLICATES")
print("=" * 70)

print("Games duplicates:", games.duplicated().sum())
print("VGSales duplicates:", vgsales.duplicated().sum())


# ------------------------------------------------------------
# 6. Statistical summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("STATISTICAL SUMMARY - GAMES")
print("=" * 70)

print(games.describe(include="all"))


print("\n" + "=" * 70)
print("STATISTICAL SUMMARY - VGSALES")
print("=" * 70)

print(vgsales.describe(include="all"))


# ------------------------------------------------------------
# 7. Unique values
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("UNIQUE VALUES - GAMES")
print("=" * 70)

for column in games.columns:
    print(column, ":", games[column].nunique())


print("\n" + "=" * 70)
print("UNIQUE VALUES - VGSALES")
print("=" * 70)

for column in vgsales.columns:
    print(column, ":", vgsales[column].nunique())


# ------------------------------------------------------------
# 8. Important categorical values
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("GAMES - GENRES")
print("=" * 70)

print(games["Genres"].value_counts().head(20))


print("\n" + "=" * 70)
print("GAMES - TEAMS / DEVELOPERS")
print("=" * 70)

print(games["Team"].value_counts().head(20))


print("\n" + "=" * 70)
print("VGSALES - GENRES")
print("=" * 70)

print(vgsales["Genre"].value_counts())


print("\n" + "=" * 70)
print("VGSALES - PLATFORMS")
print("=" * 70)

print(vgsales["Platform"].value_counts())


print("\n" + "=" * 70)
print("VGSALES - PUBLISHERS")
print("=" * 70)

print(vgsales["Publisher"].value_counts().head(20))


# ------------------------------------------------------------
# 9. Dataset inspection completed
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PHASE 1 DATASET INSPECTION COMPLETED")
print("=" * 70)