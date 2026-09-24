import pandas as pd
import numpy as np

print("=" * 70)
print("VIDEO GAME ANALYSIS — EDA QUESTIONS Q21–Q30")
print("=" * 70)

# ------------------------------------------------------------
# LOAD CLEANED DATA
# ------------------------------------------------------------

games = pd.read_csv(".\\data\\processed\\games_cleaned.csv")
sales = pd.read_csv(".\\data\\processed\\vgsales_cleaned.csv")

print("\nDatasets loaded successfully.")
print(f"Games records: {len(games)}")
print(f"Sales records: {len(sales)}")

# ------------------------------------------------------------
# PREPARE DATA
# ------------------------------------------------------------

# Numeric columns
game_numeric = [
    "Rating",
    "Times Listed",
    "Number of Reviews",
    "Plays",
    "Playing",
    "Backlogs",
    "Wishlist"
]

for col in game_numeric:
    games[col] = pd.to_numeric(games[col], errors="coerce")

sales["Global_Sales"] = pd.to_numeric(
    sales["Global_Sales"], errors="coerce"
)

sales["NA_Sales"] = pd.to_numeric(
    sales["NA_Sales"], errors="coerce"
)

sales["EU_Sales"] = pd.to_numeric(
    sales["EU_Sales"], errors="coerce"
)

sales["JP_Sales"] = pd.to_numeric(
    sales["JP_Sales"], errors="coerce"
)

sales["Other_Sales"] = pd.to_numeric(
    sales["Other_Sales"], errors="coerce"
)

# ------------------------------------------------------------
# TITLE-LEVEL AGGREGATION
# Prevents many-to-many duplication when merging datasets.
# ------------------------------------------------------------

games_agg = (
    games.groupby("Normalized_Title", as_index=False)
    .agg({
        "Title": "first",
        "Rating": "mean",
        "Times Listed": "max",
        "Number of Reviews": "max",
        "Plays": "max",
        "Playing": "max",
        "Backlogs": "max",
        "Wishlist": "max",
        "Genres": "first"
    })
)

sales_agg = (
    sales.groupby("Normalized_Name", as_index=False)
    .agg({
        "Global_Sales": "sum",
        "NA_Sales": "sum",
        "EU_Sales": "sum",
        "JP_Sales": "sum",
        "Other_Sales": "sum"
    })
)

# ------------------------------------------------------------
# MERGE GAMES + SALES
# ------------------------------------------------------------

merged = games_agg.merge(
    sales_agg,
    left_on="Normalized_Title",
    right_on="Normalized_Name",
    how="inner"
)

print(f"Matched title-level records: {len(merged)}")

# ============================================================
# Q21
# Which game genres generate the most global sales?
# ============================================================

print("\n" + "=" * 70)
print("Q21. GAME GENRES WITH THE MOST GLOBAL SALES")
print("=" * 70)

genre_sales = []

for _, row in merged.iterrows():

    if pd.isna(row["Genres"]):
        continue

    genres = str(row["Genres"]).split(",")

    for genre in genres:

        genre = genre.strip()

        if genre:
            genre_sales.append(
                {
                    "Genre": genre,
                    "Global_Sales": row["Global_Sales"]
                }
            )

q21 = pd.DataFrame(genre_sales)

q21_result = (
    q21.groupby("Genre")
    .agg(
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Global_Sales", "count")
    )
    .sort_values("Total_Global_Sales", ascending=False)
)

print(q21_result)

# ============================================================
# Q22
# How does user rating affect global sales?
# ============================================================

print("\n" + "=" * 70)
print("Q22. USER RATING VS GLOBAL SALES")
print("=" * 70)

rating_data = merged.dropna(
    subset=["Rating", "Global_Sales"]
).copy()

rating_data["Rating_Group"] = pd.cut(
    rating_data["Rating"],
    bins=[0, 1, 2, 3, 4, 5],
    labels=[
        "Below 1",
        "1–1.99",
        "2–2.99",
        "3–3.99",
        "4–4.99"
    ],
    include_lowest=True
)

q22_result = (
    rating_data.groupby("Rating_Group", observed=False)
    .agg(
        Game_Count=("Global_Sales", "count"),
        Average_Global_Sales=("Global_Sales", "mean"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Average_Rating=("Rating", "mean")
    )
)

print(q22_result)

rating_corr = rating_data[
    ["Rating", "Global_Sales"]
].corr().iloc[0, 1]

print(f"\nRating vs Global Sales correlation: {rating_corr:.4f}")

# ============================================================
# Q23
# Which platforms have the most games with high ratings?
# ============================================================

print("\n" + "=" * 70)
print("Q23. PLATFORMS WITH HIGH-RATED GAMES")
print("=" * 70)

# Platform information comes from sales data.
# Join matched game titles with platform records.

q23_data = sales.merge(
    games_agg[
        [
            "Normalized_Title",
            "Rating",
            "Title"
        ]
    ],
    left_on="Normalized_Name",
    right_on="Normalized_Title",
    how="inner"
)

high_rated = q23_data[
    q23_data["Rating"] > 4
].copy()

q23_result = (
    high_rated.groupby("Platform")
    .agg(
        High_Rated_Games=("Normalized_Name", "nunique"),
        Average_Rating=("Rating", "mean")
    )
    .sort_values(
        "High_Rated_Games",
        ascending=False
    )
)

print(q23_result)

# ============================================================
# Q24
# What's the trend of releases and sales over time?
# ============================================================

print("\n" + "=" * 70)
print("Q24. RELEASES AND SALES TREND OVER TIME")
print("=" * 70)

games_year = (
    games.dropna(subset=["Release_Year"])
    .groupby("Release_Year")
    .agg(
        Game_Releases=("Normalized_Title", "nunique")
    )
)

sales_year = (
    sales.dropna(subset=["Year"])
    .groupby("Year")
    .agg(
        Global_Sales=("Global_Sales", "sum")
    )
)

games_year.index = games_year.index.astype(int)
sales_year.index = sales_year.index.astype(int)

q24_result = games_year.join(
    sales_year,
    how="outer"
).sort_index()

print(q24_result)

# ============================================================
# Q25
# Do highly wishlisted games lead to more sales?
# ============================================================

print("\n" + "=" * 70)
print("Q25. WISHLIST VS GLOBAL SALES")
print("=" * 70)

q25_data = merged.dropna(
    subset=["Wishlist", "Global_Sales"]
).copy()

q25_corr = q25_data[
    ["Wishlist", "Global_Sales"]
].corr().iloc[0, 1]

print(
    f"Wishlist vs Global Sales correlation: "
    f"{q25_corr:.4f}"
)

q25_data["Wishlist_Group"] = pd.qcut(
    q25_data["Wishlist"],
    q=4,
    duplicates="drop"
)

q25_result = (
    q25_data.groupby("Wishlist_Group", observed=False)
    .agg(
        Game_Count=("Global_Sales", "count"),
        Average_Wishlist=("Wishlist", "mean"),
        Average_Global_Sales=("Global_Sales", "mean"),
        Total_Global_Sales=("Global_Sales", "sum")
    )
)

print("\nWishlist quartiles:")
print(q25_result)

# ============================================================
# Q26
# Which genres have the highest engagement but lowest sales?
# ============================================================

print("\n" + "=" * 70)
print("Q26. HIGH ENGAGEMENT BUT LOW SALES GENRES")
print("=" * 70)

genre_engagement = []

for _, row in merged.iterrows():

    if pd.isna(row["Genres"]):
        continue

    genres = str(row["Genres"]).split(",")

    engagement = (
        row["Plays"]
        + row["Playing"]
        + row["Backlogs"]
        + row["Wishlist"]
    )

    for genre in genres:

        genre = genre.strip()

        if genre:
            genre_engagement.append(
                {
                    "Genre": genre,
                    "Engagement": engagement,
                    "Global_Sales": row["Global_Sales"]
                }
            )

q26 = pd.DataFrame(genre_engagement)

q26_result = (
    q26.groupby("Genre")
    .agg(
        Average_Engagement=("Engagement", "mean"),
        Average_Global_Sales=("Global_Sales", "mean"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Global_Sales", "count")
    )
)

# Standardized scores allow engagement and sales
# to be compared on different scales.

q26_result["Engagement_Rank"] = (
    q26_result["Average_Engagement"]
    .rank(pct=True)
)

q26_result["Sales_Rank"] = (
    q26_result["Average_Global_Sales"]
    .rank(pct=True)
)

q26_result["Engagement_Sales_Gap"] = (
    q26_result["Engagement_Rank"]
    - q26_result["Sales_Rank"]
)

q26_result = q26_result.sort_values(
    "Engagement_Sales_Gap",
    ascending=False
)

print(q26_result)

# ============================================================
# Q27
# Do highly listed games correlate with better ratings?
# ============================================================

print("\n" + "=" * 70)
print("Q27. LISTINGS VS USER RATINGS")
print("=" * 70)

q27_data = merged.dropna(
    subset=[
        "Times Listed",
        "Backlogs",
        "Wishlist",
        "Rating"
    ]
).copy()

q27_data["Total_Listed_Interest"] = (
    q27_data["Times Listed"]
    + q27_data["Backlogs"]
    + q27_data["Wishlist"]
)

q27_corr = q27_data[
    ["Total_Listed_Interest", "Rating"]
].corr().iloc[0, 1]

print(
    "Total listed interest vs Rating correlation: "
    f"{q27_corr:.4f}"
)

q27_data["Listing_Group"] = pd.qcut(
    q27_data["Total_Listed_Interest"],
    q=4,
    duplicates="drop"
)

q27_result = (
    q27_data.groupby("Listing_Group", observed=False)
    .agg(
        Game_Count=("Rating", "count"),
        Average_Listed_Interest=(
            "Total_Listed_Interest",
            "mean"
        ),
        Average_Rating=("Rating", "mean")
    )
)

print("\nListing-interest quartiles:")
print(q27_result)

# ============================================================
# Q28
# How does user engagement differ across genres?
# ============================================================

print("\n" + "=" * 70)
print("Q28. USER ENGAGEMENT ACROSS GENRES")
print("=" * 70)

q28_result = (
    q26.groupby("Genre")
    .agg(
        Average_Plays=("Engagement", "mean"),
        Average_Global_Sales=("Global_Sales", "mean"),
        Game_Count=("Global_Sales", "count")
    )
    .sort_values(
        "Average_Plays",
        ascending=False
    )
)

print(q28_result)

# ============================================================
# Q29
# What are the top-performing combinations of Genre + Platform?
# ============================================================

print("\n" + "=" * 70)
print("Q29. TOP GENRE + PLATFORM COMBINATIONS")
print("=" * 70)

genre_platform = []

for _, row in sales.iterrows():

    if pd.isna(row["Genre"]) or pd.isna(row["Platform"]):
        continue

    genre_platform.append(
        {
            "Genre": str(row["Genre"]).strip(),
            "Platform": str(row["Platform"]).strip(),
            "Global_Sales": row["Global_Sales"]
        }
    )

q29 = pd.DataFrame(genre_platform)

q29_result = (
    q29.groupby(
        ["Genre", "Platform"]
    )
    .agg(
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Global_Sales", "count"),
        Average_Global_Sales=("Global_Sales", "mean")
    )
    .sort_values(
        "Total_Global_Sales",
        ascending=False
    )
)

print(q29_result.head(30))

# ============================================================
# Q30
# What does a regional sales heatmap by genre reveal?
# ============================================================

print("\n" + "=" * 70)
print("Q30. REGIONAL SALES BY GENRE")
print("=" * 70)

q30_result = (
    sales.groupby("Genre")
    .agg(
        NA_Sales=("NA_Sales", "sum"),
        EU_Sales=("EU_Sales", "sum"),
        JP_Sales=("JP_Sales", "sum"),
        Other_Sales=("Other_Sales", "sum"),
        Global_Sales=("Global_Sales", "sum")
    )
    .sort_values(
        "Global_Sales",
        ascending=False
    )
)

print(q30_result)

# ------------------------------------------------------------
# COMPLETION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("Q21–Q30 EDA COMPLETED")
print("=" * 70)