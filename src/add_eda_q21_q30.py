import json

NOTEBOOK_PATH = r"notebooks\01_dataset_inspection.ipynb"

with open(NOTEBOOK_PATH, "r", encoding="utf-8-sig") as f:
    notebook = json.load(f)

cells = notebook["cells"]

# Find the existing Q21-Q30 placeholder
target_index = None

for i, cell in enumerate(cells):
    source = "".join(cell.get("source", []))
    if "## Combined Analysis — Q21 to Q30" in source:
        target_index = i
        break

if target_index is None:
    raise ValueError("Q21-Q30 placeholder not found.")

new_cells = []


def markdown(text):
    new_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(True)
    })


def code(text):
    new_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(True)
    })


# ============================================================
# SECTION INTRODUCTION
# ============================================================

markdown("""# Combined Dataset Analysis — Q21 to Q30

This section combines the cleaned game engagement dataset with the cleaned sales dataset.

The analysis uses controlled title-level matching through `Normalized_Title` and
`Normalized_Name` to reduce many-to-many duplication.

**Matched title-level records:** 486

The questions examine relationships between genres, ratings, engagement,
wishlists, platforms and regional sales.
""")

# ============================================================
# PREPARATION
# ============================================================

markdown("""## Combined Dataset Preparation

Before answering Q21–Q30, the two datasets are aggregated at title level.

This is important because a direct merge can duplicate records when multiple
rows represent the same normalized game title.
""")

code("""# Title-level aggregation

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

merged = games_agg.merge(
    sales_agg,
    left_on="Normalized_Title",
    right_on="Normalized_Name",
    how="inner"
)

print("Matched title-level records:", len(merged))
merged.head()
""")

# ============================================================
# Q21
# ============================================================

markdown("""## Q21. Which game genres generate the most global sales?

Genres are split where a game contains multiple genres.

A matched game contributes its global sales to each associated genre.
""")

code("""genre_sales = []

for _, row in merged.iterrows():

    if pd.isna(row["Genres"]):
        continue

    for genre in str(row["Genres"]).split(","):

        genre = genre.strip()

        if genre:
            genre_sales.append({
                "Genre": genre,
                "Global_Sales": row["Global_Sales"]
            })

q21 = pd.DataFrame(genre_sales)

q21_result = (
    q21.groupby("Genre")
    .agg(
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Global_Sales", "count")
    )
    .sort_values("Total_Global_Sales", ascending=False)
)

q21_result
""")

markdown("""**Interpretation:** Adventure records generate the highest total global
sales in the matched dataset, followed by Shooter and Platform.

Because multi-genre games are counted under each associated genre, these totals
should not be interpreted as mutually exclusive market shares.
""")

# ============================================================
# Q22
# ============================================================

markdown("""## Q22. How does user rating affect global sales?

The relationship is examined using rating groups and a Pearson correlation
between rating and global sales.
""")

code("""rating_data = merged.dropna(
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

rating_corr = rating_data[
    ["Rating", "Global_Sales"]
].corr().iloc[0, 1]

print(q22_result)
print("\\nRating vs Global Sales correlation:", round(rating_corr, 4))
""")

markdown("""**Interpretation:** The rating-to-sales correlation in this matched
sample is approximately **0.0121**. This indicates that the two variables have
almost no linear relationship in this dataset.

Correlation should not be interpreted as causation.
""")

# ============================================================
# Q23
# ============================================================

markdown("""## Q23. Which platforms have the most games with high ratings?

A high rating is defined according to the project question as a rating **above 4**.
""")

code("""q23_data = sales.merge(
    games_agg[
        ["Normalized_Title", "Rating", "Title"]
    ],
    left_on="Normalized_Name",
    right_on="Normalized_Title",
    how="inner"
)

high_rated = q23_data[
    q23_data["Rating"] > 4
]

q23_result = (
    high_rated.groupby("Platform")
    .agg(
        High_Rated_Games=("Normalized_Name", "nunique"),
        Average_Rating=("Rating", "mean")
    )
    .sort_values("High_Rated_Games", ascending=False)
)

q23_result
""")

markdown("""**Interpretation:** PS2 has the largest number of matched high-rated
game records in this analysis, followed by PC and PS3.

The result is a count of high-rated matched games, not a platform quality score.
""")

# ============================================================
# Q24
# ============================================================

markdown("""## Q24. What’s the trend of releases and sales over time?

Release counts come from `games.csv`, while sales totals come from `vgsales.csv`.

The two datasets have different year coverage, so missing sales values are
retained as missing rather than being treated as zero.
""")

code("""games_year = (
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

q24_result = (
    games_year
    .join(sales_year, how="outer")
    .sort_index()
)

q24_result
""")

markdown("""**Interpretation:** The combined yearly view shows increasing release
activity through the 2000s and substantial sales totals during the same period.

Late-year values require caution because the two source datasets have incomplete
and different temporal coverage. Missing sales values do not represent zero sales.
""")

# ============================================================
# Q25
# ============================================================

markdown("""## Q25. Do highly wishlisted games lead to more sales?

The relationship between wishlist counts and global sales is examined using
correlation and wishlist quartiles.
""")

code("""q25_data = merged.dropna(
    subset=["Wishlist", "Global_Sales"]
).copy()

q25_corr = q25_data[
    ["Wishlist", "Global_Sales"]
].corr().iloc[0, 1]

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

print("Wishlist vs Global Sales correlation:",
      round(q25_corr, 4))

q25_result
""")

markdown("""**Interpretation:** The wishlist-to-global-sales correlation is
approximately **-0.0691** in the matched sample.

The relationship is therefore weak in this dataset, and higher wishlist counts
do not correspond to a simple increasing sales pattern.

This is an association analysis, not evidence that wishlisting causes lower or
higher sales.
""")

# ============================================================
# Q26
# ============================================================

markdown("""## Q26. Which genres have the highest engagement but lowest sales?

For this project, an engagement measure is constructed as:

**Plays + Playing + Backlogs + Wishlist**

Genres are then compared using their average engagement and average global sales.
""")

code("""genre_engagement = []

for _, row in merged.iterrows():

    if pd.isna(row["Genres"]):
        continue

    engagement = (
        row["Plays"]
        + row["Playing"]
        + row["Backlogs"]
        + row["Wishlist"]
    )

    for genre in str(row["Genres"]).split(","):

        genre = genre.strip()

        if genre:
            genre_engagement.append({
                "Genre": genre,
                "Engagement": engagement,
                "Global_Sales": row["Global_Sales"]
            })

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

q26_result["Engagement_Rank"] = (
    q26_result["Average_Engagement"].rank(pct=True)
)

q26_result["Sales_Rank"] = (
    q26_result["Average_Global_Sales"].rank(pct=True)
)

q26_result["Engagement_Sales_Gap"] = (
    q26_result["Engagement_Rank"]
    - q26_result["Sales_Rank"]
)

q26_result.sort_values(
    "Engagement_Sales_Gap",
    ascending=False
)
""")

markdown("""**Interpretation:** Genres such as Indie, Turn Based Strategy,
Visual Novel and Point-and-Click show relatively high engagement compared with
their average sales in this matched dataset.

The engagement measure is a project-defined composite metric and should be
interpreted as a comparative indicator rather than an official industry metric.
""")

# ============================================================
# Q27
# ============================================================

markdown("""## Q27. Do highly listed games (wishlist/backlogs) correlate with better ratings?

A combined listing-interest measure is created from:

**Times Listed + Backlogs + Wishlist**

The relationship with user rating is then measured.
""")

code("""q27_data = merged.dropna(
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

print(
    "Total listed interest vs Rating correlation:",
    round(q27_corr, 4)
)

q27_result
""")

markdown("""**Interpretation:** Total listed interest and rating have a
correlation of approximately **0.5082** in the matched sample.

The quartile analysis also shows increasing average ratings across the four
listing-interest groups.

This demonstrates association within the dataset and does not establish a
causal relationship.
""")

# ============================================================
# Q28
# ============================================================

markdown("""## Q28. How does user engagement differ across genres?

Average engagement is compared across genres using the same project-defined
engagement measure from Q26.
""")

code("""q28_result = (
    q26.groupby("Genre")
    .agg(
        Average_Engagement=("Engagement", "mean"),
        Average_Global_Sales=("Global_Sales", "mean"),
        Game_Count=("Global_Sales", "count")
    )
    .sort_values(
        "Average_Engagement",
        ascending=False
    )
)

q28_result
""")

markdown("""**Interpretation:** Shooter has the highest average engagement in
the matched dataset, followed by Adventure, Indie and Turn Based Strategy.

Genre counts differ substantially, so average engagement should be considered
alongside `Game_Count`.
""")

# ============================================================
# Q29
# ============================================================

markdown("""## Q29. What are the top-performing combinations of Genre + Platform?

The sales dataset is grouped by both genre and platform to identify combinations
with the highest cumulative global sales.
""")

code("""q29_result = (
    sales.groupby(
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

q29_result.head(30)
""")

markdown("""**Interpretation:** Among the combinations in the dataset, Action +
PS3 has the largest cumulative global sales, followed by Sports + Wii and
Shooter + X360.

Cumulative sales are affected by the number of records in each
genre-platform combination, so `Game_Count` should be considered alongside
total sales.
""")

# ============================================================
# Q30
# ============================================================

markdown("""## Q30. What does a regional sales heatmap by genre reveal?

Regional sales are aggregated by genre across North America, Europe, Japan and
Other regions.

The resulting table can directly support a heatmap in the visualization stage.
""")

code("""q30_result = (
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

q30_result
""")

markdown("""**Interpretation:** North America has the largest sales totals for
many genres, while Japan has a comparatively strong contribution for
Role-Playing and Fighting games.

For example, Role-Playing records show **352.31M** in Japan compared with
**327.28M** in North America.

The regional heatmap should therefore be used to reveal differences in genre
sales patterns rather than treating all regions as having the same preferences.
""")

# ============================================================
# SECTION SUMMARY
# ============================================================

markdown("""## Q21–Q30 Summary

The combined analysis examined:

- Genre-level global sales
- Rating and sales relationships
- High-rated games by platform
- Release and sales trends over time
- Wishlist and sales relationships
- Engagement versus sales
- Listing interest and ratings
- Engagement differences across genres
- Genre + platform sales combinations
- Regional sales patterns by genre

### Methodological Notes

1. The merged analysis uses controlled title matching.
2. Multi-genre games can contribute to more than one genre.
3. Engagement is defined for this project as Plays + Playing + Backlogs + Wishlist.
4. Listing interest is defined as Times Listed + Backlogs + Wishlist.
5. Correlation measures association, not causation.
6. Different source datasets have different temporal coverage.
7. Missing yearly sales values are not treated as zero.
""")

# Replace placeholder
cells[target_index:target_index + 1] = new_cells

notebook["cells"] = cells

with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Q21–Q30 notebook section added successfully.")
print(f"Notebook: {NOTEBOOK_PATH}")
print(f"Total cells: {len(notebook['cells'])}")