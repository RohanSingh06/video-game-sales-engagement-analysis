import json

path = "notebooks/01_dataset_inspection.ipynb"

with open(path, "r", encoding="utf-8-sig") as f:
    notebook = json.load(f)


cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Games Analysis — Q1 to Q9"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q1. What are the top-rated games by user reviews?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "top_rated = games[[\"Title\", \"Rating\", \"Number_of_Reviews\"]].dropna(subset=[\"Rating\"])\n",
            "top_rated = top_rated.sort_values(\n",
            "    [\"Rating\", \"Number_of_Reviews\"],\n",
            "    ascending=[False, False]\n",
            ").head(10)\n",
            "\n",
            "display(top_rated)"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** This table identifies games with the highest recorded user ratings, with number of reviews used as a secondary ordering field."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q2. Which developers (Teams) have the highest average ratings?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "team_rating = games.dropna(subset=[\"Rating\"]).groupby(\"Team\").agg(\n",
            "    Average_Rating=(\"Rating\", \"mean\"),\n",
            "    Game_Count=(\"Title\", \"count\")\n",
            ").sort_values(\"Average_Rating\", ascending=False)\n",
            "\n",
            "display(team_rating.head(10))"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** Developer teams are compared using their average recorded user rating. Game count is included to provide context."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q3. What are the most common genres in the dataset?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "genre_counts = (\n",
            "    games[\"Genres\"]\n",
            "    .dropna()\n",
            "    .str.split(\",\")\n",
            "    .explode()\n",
            "    .str.strip()\n",
            "    .value_counts()\n",
            ")\n",
            "\n",
            "display(genre_counts.head(10))\n",
            "\n",
            "plt.figure(figsize=(10, 6))\n",
            "genre_counts.head(10).sort_values().plot(kind=\"barh\")\n",
            "plt.title(\"Most Common Game Genres\")\n",
            "plt.xlabel(\"Number of Records\")\n",
            "plt.ylabel(\"Genre\")\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** Genre frequency shows which categories appear most often in the Games metadata dataset."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q4. Which games have the highest backlog compared to wishlist?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "backlog_analysis = games[[\"Title\", \"Backlogs\", \"Wishlist\"]].copy()\n",
            "\n",
            "backlog_analysis[\"Backlog_to_Wishlist\"] = (\n",
            "    backlog_analysis[\"Backlogs\"] /\n",
            "    backlog_analysis[\"Wishlist\"].replace(0, np.nan)\n",
            ")\n",
            "\n",
            "backlog_analysis = backlog_analysis.dropna(\n",
            "    subset=[\"Backlog_to_Wishlist\"]\n",
            ")\n",
            "\n",
            "display(\n",
            "    backlog_analysis\n",
            "    .sort_values(\"Backlog_to_Wishlist\", ascending=False)\n",
            "    .head(10)\n",
            ")"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** The ratio compares backlog volume with wishlist volume. A higher ratio indicates relatively more backlog entries than wishlist entries."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q5. What is the game release trend across years?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "release_trend = (\n",
            "    games.dropna(subset=[\"Release_Year\"])\n",
            "    .groupby(\"Release_Year\")\n",
            "    .size()\n",
            ")\n",
            "\n",
            "display(release_trend.to_frame(\"Game_Count\"))\n",
            "\n",
            "plt.figure(figsize=(12, 6))\n",
            "release_trend.plot(kind=\"line\", marker=\"o\")\n",
            "plt.title(\"Game Release Trend Across Years\")\n",
            "plt.xlabel(\"Release Year\")\n",
            "plt.ylabel(\"Number of Games\")\n",
            "plt.grid(True)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** The line chart shows how the number of games represented in the metadata dataset changes across release years."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q6. What is the distribution of user ratings?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "rating_data = games[\"Rating\"].dropna()\n",
            "\n",
            "print(\"Mean rating:\", round(rating_data.mean(), 2))\n",
            "print(\"Median rating:\", round(rating_data.median(), 2))\n",
            "\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.histplot(rating_data, bins=20, kde=True)\n",
            "plt.title(\"Distribution of User Ratings\")\n",
            "plt.xlabel(\"Rating\")\n",
            "plt.ylabel(\"Number of Games\")\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** The histogram shows the distribution and concentration of recorded user ratings."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q7. What are the top 10 most wishlisted games?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "top_wishlisted = (\n",
            "    games[[\"Title\", \"Wishlist\"]]\n",
            "    .sort_values(\"Wishlist\", ascending=False)\n",
            "    .head(10)\n",
            ")\n",
            "\n",
            "display(top_wishlisted)\n",
            "\n",
            "plt.figure(figsize=(10, 6))\n",
            "plot_data = top_wishlisted.sort_values(\"Wishlist\")\n",
            "plt.barh(plot_data[\"Title\"], plot_data[\"Wishlist\"])\n",
            "plt.title(\"Top 10 Most Wishlisted Games\")\n",
            "plt.xlabel(\"Wishlist Count\")\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** These are the ten games with the highest recorded wishlist counts in the Games dataset."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q8. What’s the average number of plays per genre?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "plays_genre = games.dropna(\n",
            "    subset=[\"Genres\", \"Plays\"]\n",
            ").copy()\n",
            "\n",
            "plays_genre[\"Genre\"] = plays_genre[\"Genres\"].str.split(\",\")\n",
            "plays_genre = plays_genre.explode(\"Genre\")\n",
            "plays_genre[\"Genre\"] = plays_genre[\"Genre\"].str.strip()\n",
            "\n",
            "average_plays = (\n",
            "    plays_genre.groupby(\"Genre\")[\"Plays\"]\n",
            "    .mean()\n",
            "    .sort_values(ascending=False)\n",
            ")\n",
            "\n",
            "display(average_plays.to_frame(\"Average_Plays\"))"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** Average plays are calculated after expanding records containing multiple genres so that each listed genre contributes to its genre-level average."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Q9. Which developer studios are the most productive and impactful?"
        ]
    },

    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "studio_analysis = games.groupby(\"Team\").agg(\n",
            "    Games_Released=(\"Title\", \"count\"),\n",
            "    Average_Rating=(\"Rating\", \"mean\"),\n",
            "    Total_Reviews=(\"Number_of_Reviews\", \"sum\"),\n",
            "    Total_Plays=(\"Plays\", \"sum\")\n",
            ").sort_values(\n",
            "    [\"Games_Released\", \"Average_Rating\"],\n",
            "    ascending=[False, False]\n",
            ")\n",
            "\n",
            "display(studio_analysis.head(10))"
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation:** Productivity is represented by the number of games in the dataset. Impact is described using accompanying engagement indicators such as average rating, total reviews, and total plays."
        ]
    },

    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Q1–Q9 Games Analysis Completed"
        ]
    }
]


# Find the existing Games Analysis placeholder
index = None

for i, cell in enumerate(notebook["cells"]):
    text = "".join(cell.get("source", []))
    if text.strip() == "## Games Analysis — Q1 to Q9":
        index = i
        break

if index is None:
    raise ValueError("Games Analysis placeholder not found.")


# Replace placeholder with actual Q1-Q9 cells
notebook["cells"] = notebook["cells"][:index] + cells + notebook["cells"][index + 1:]


with open(path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)


print("Q1-Q9 added successfully.")
print("Total notebook cells:", len(notebook["cells"]))