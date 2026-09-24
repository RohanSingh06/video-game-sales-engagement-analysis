import pandas as pd


# ============================================================
# VIDEO GAME SALES AND ENGAGEMENT ANALYSIS
# PHASE 2A - TITLE MATCHING ANALYSIS
# ============================================================


# ------------------------------------------------------------
# 1. Load datasets
# ------------------------------------------------------------

games_path = "data/raw/games.csv"
vgsales_path = "data/raw/vgsales.csv"

games = pd.read_csv(games_path)
vgsales = pd.read_csv(vgsales_path)


# ------------------------------------------------------------
# 2. Extract game titles
# ------------------------------------------------------------

game_titles = games["Title"].dropna().unique()
sales_names = vgsales["Name"].dropna().unique()


# ------------------------------------------------------------
# 3. Exact title matching
# ------------------------------------------------------------

exact_matches = set(game_titles).intersection(set(sales_names))


print("\n" + "=" * 70)
print("TITLE MATCHING ANALYSIS")
print("=" * 70)

print("\nUnique titles in games.csv:")
print(len(game_titles))

print("\nUnique names in vgsales.csv:")
print(len(sales_names))

print("\nExact title matches:")
print(len(exact_matches))


# ------------------------------------------------------------
# 4. Match percentage
# ------------------------------------------------------------

games_match_percentage = (
    len(exact_matches) / len(game_titles)
) * 100

vgsales_match_percentage = (
    len(exact_matches) / len(sales_names)
) * 100


print("\nPercentage of games.csv titles matched:")
print(round(games_match_percentage, 2), "%")

print("\nPercentage of vgsales.csv names matched:")
print(round(vgsales_match_percentage, 2), "%")


# ------------------------------------------------------------
# 5. Unmatched games.csv titles
# ------------------------------------------------------------

unmatched_games = [
    title for title in game_titles
    if title not in exact_matches
]


print("\n" + "=" * 70)
print("UNMATCHED TITLES FROM GAMES.CSV")
print("=" * 70)

print("\nNumber of unmatched titles:")
print(len(unmatched_games))

print("\nFirst 50 unmatched titles:")

for title in unmatched_games[:50]:
    print(title)


# ------------------------------------------------------------
# 6. Unmatched vgsales.csv names
# ------------------------------------------------------------

unmatched_sales = [
    name for name in sales_names
    if name not in exact_matches
]


print("\n" + "=" * 70)
print("UNMATCHED NAMES FROM VGSALES.CSV")
print("=" * 70)

print("\nNumber of unmatched names:")
print(len(unmatched_sales))

print("\nFirst 50 unmatched names:")

for name in unmatched_sales[:50]:
    print(name)


# ------------------------------------------------------------
# 7. Sample exact matches
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SAMPLE EXACT MATCHES")
print("=" * 70)

for title in list(exact_matches)[:50]:
    print(title)


# ------------------------------------------------------------
# 8. Check repeated titles in games.csv
# ------------------------------------------------------------

games_title_counts = games["Title"].value_counts()

repeated_games_titles = games_title_counts[
    games_title_counts > 1
]


print("\n" + "=" * 70)
print("REPEATED TITLES IN GAMES.CSV")
print("=" * 70)

print("\nNumber of repeated titles:")
print(len(repeated_games_titles))

print("\nTop repeated titles:")

print(repeated_games_titles.head(20))


# ------------------------------------------------------------
# 9. Check repeated names in vgsales.csv
# ------------------------------------------------------------

sales_name_counts = vgsales["Name"].value_counts()

repeated_sales_names = sales_name_counts[
    sales_name_counts > 1
]


print("\n" + "=" * 70)
print("REPEATED NAMES IN VGSALES.CSV")
print("=" * 70)

print("\nNumber of repeated names:")
print(len(repeated_sales_names))

print("\nTop repeated names:")

print(repeated_sales_names.head(20))


# ------------------------------------------------------------
# 10. Final status
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TITLE MATCHING ANALYSIS COMPLETED")
print("=" * 70)