import pandas as pd
import numpy as np

print("=" * 70)
print("VIDEO GAME ANALYSIS — EDA QUESTIONS Q1–Q9")
print("=" * 70)

# ---------------------------------------------------------
# LOAD CLEANED DATA
# ---------------------------------------------------------

games = pd.read_csv(r"data\processed\games_cleaned.csv")

print("\nDataset loaded successfully.")
print("Games:", len(games))


# =========================================================
# Q1 — TOP-RATED GAMES BY USER REVIEWS
# =========================================================

print("\n" + "=" * 70)
print("Q1. TOP-RATED GAMES BY USER REVIEWS")
print("=" * 70)

# One record per normalized game title
q1 = (
    games[
        ["Normalized_Title", "Title", "Rating", "Number of Reviews"]
    ]
    .dropna(subset=["Rating"])
    .sort_values(
        ["Normalized_Title", "Rating", "Number of Reviews"],
        ascending=[True, False, False]
    )
    .drop_duplicates("Normalized_Title")
)

q1 = (
    q1
    .sort_values(
        ["Rating", "Number of Reviews"],
        ascending=[False, False]
    )
    .head(10)
)

print(
    q1[
        ["Title", "Rating", "Number of Reviews"]
    ].to_string(index=False)
)


# =========================================================
# Q2 — DEVELOPERS WITH HIGHEST AVERAGE RATINGS
# =========================================================

print("\n" + "=" * 70)
print("Q2. DEVELOPERS WITH HIGHEST AVERAGE RATINGS")
print("=" * 70)

# Split multiple developers into individual studio names
q2_data = games[
    ["Title", "Team", "Rating"]
].dropna(subset=["Team", "Rating"]).copy()

q2_data["Team"] = q2_data["Team"].str.split(",")

q2_data = q2_data.explode("Team")

q2_data["Team"] = q2_data["Team"].str.strip()

q2 = (
    q2_data
    .groupby("Team")
    .agg(
        Average_Rating=("Rating", "mean"),
        Game_Count=("Title", "count")
    )
    .sort_values(
        ["Average_Rating", "Game_Count"],
        ascending=[False, False]
    )
    .head(10)
)

print(q2.to_string())


# =========================================================
# Q3 — MOST COMMON GENRES
# =========================================================

print("\n" + "=" * 70)
print("Q3. MOST COMMON GENRES")
print("=" * 70)

q3 = (
    games["Genres"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)

print(q3.to_string())


# =========================================================
# Q4 — HIGHEST BACKLOG COMPARED TO WISHLIST
# =========================================================

print("\n" + "=" * 70)
print("Q4. HIGHEST BACKLOG-TO-WISHLIST RATIO")
print("=" * 70)

q4 = games[
    ["Title", "Backlogs", "Wishlist"]
].copy()

q4["Backlog_to_Wishlist"] = (
    q4["Backlogs"] /
    q4["Wishlist"].replace(0, np.nan)
)

q4 = (
    q4
    .dropna(subset=["Backlog_to_Wishlist"])
    .sort_values(
        "Backlog_to_Wishlist",
        ascending=False
    )
    .head(10)
)

print(q4.to_string(index=False))


# =========================================================
# Q5 — GAME RELEASE TREND ACROSS YEARS
# =========================================================

print("\n" + "=" * 70)
print("Q5. GAME RELEASE TREND ACROSS YEARS")
print("=" * 70)

q5 = (
    games
    .dropna(subset=["Release_Year"])
    .groupby("Release_Year")
    .size()
    .reset_index(name="Game_Count")
)

print(q5.to_string(index=False))


# =========================================================
# Q6 — DISTRIBUTION OF USER RATINGS
# =========================================================

print("\n" + "=" * 70)
print("Q6. DISTRIBUTION OF USER RATINGS")
print("=" * 70)

ratings = games["Rating"].dropna()

print(f"Count  : {len(ratings)}")
print(f"Mean   : {ratings.mean():.2f}")
print(f"Median : {ratings.median():.2f}")
print(f"Minimum: {ratings.min():.2f}")
print(f"Maximum: {ratings.max():.2f}")

print("\nRating distribution:")

print(
    ratings
    .round(1)
    .value_counts()
    .sort_index()
    .to_string()
)


# =========================================================
# Q7 — TOP 10 MOST WISHLISTED GAMES
# =========================================================

print("\n" + "=" * 70)
print("Q7. TOP 10 MOST WISHLISTED GAMES")
print("=" * 70)

# One record per normalized title
q7 = (
    games[
        ["Normalized_Title", "Title", "Wishlist"]
    ]
    .dropna(subset=["Wishlist"])
    .sort_values(
        ["Normalized_Title", "Wishlist"],
        ascending=[True, False]
    )
    .drop_duplicates("Normalized_Title")
    .sort_values(
        "Wishlist",
        ascending=False
    )
    .head(10)
)

print(
    q7[
        ["Title", "Wishlist"]
    ].to_string(index=False)
)


# =========================================================
# Q8 — AVERAGE NUMBER OF PLAYS PER GENRE
# =========================================================

print("\n" + "=" * 70)
print("Q8. AVERAGE NUMBER OF PLAYS PER GENRE")
print("=" * 70)

genre_plays = games[
    ["Genres", "Plays"]
].dropna(
    subset=["Genres", "Plays"]
).copy()

genre_plays["Genres"] = genre_plays["Genres"].str.split(",")

genre_plays = genre_plays.explode("Genres")

genre_plays["Genres"] = genre_plays["Genres"].str.strip()

q8 = (
    genre_plays
    .groupby("Genres")["Plays"]
    .mean()
    .sort_values(ascending=False)
)

print(q8.to_string())


# =========================================================
# Q9 — MOST PRODUCTIVE AND IMPACTFUL DEVELOPER STUDIOS
# =========================================================

print("\n" + "=" * 70)
print("Q9. MOST PRODUCTIVE AND IMPACTFUL DEVELOPER STUDIOS")
print("=" * 70)

q9_data = games[
    [
        "Title",
        "Team",
        "Rating",
        "Number of Reviews",
        "Plays"
    ]
].dropna(subset=["Team"]).copy()

# Split multiple developers into individual studios
q9_data["Team"] = q9_data["Team"].str.split(",")

q9_data = q9_data.explode("Team")

q9_data["Team"] = q9_data["Team"].str.strip()

q9 = (
    q9_data
    .groupby("Team")
    .agg(
        Games_Released=("Title", "count"),
        Average_Rating=("Rating", "mean"),
        Total_Reviews=("Number of Reviews", "sum"),
        Total_Plays=("Plays", "sum")
    )
    .sort_values(
        ["Games_Released", "Average_Rating"],
        ascending=[False, False]
    )
    .head(10)
)

print(q9.to_string())


# =========================================================
# COMPLETION
# =========================================================

print("\n" + "=" * 70)
print("Q1–Q9 EDA EXECUTION COMPLETED SUCCESSFULLY")
print("=" * 70)