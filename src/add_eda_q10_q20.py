import json
from pathlib import Path


NOTEBOOK = Path(r"notebooks\01_dataset_inspection.ipynb")


def markdown(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(True)
    }


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(True)
    }


with open(NOTEBOOK, "r", encoding="utf-8-sig") as f:
    notebook = json.load(f)


cells = notebook["cells"]

# ---------------------------------------------------------
# FIND Q10–Q20 PLACEHOLDER
# ---------------------------------------------------------

placeholder_index = None

for i, cell in enumerate(cells):
    source = "".join(cell.get("source", []))

    if "## Sales Analysis — Q10 to Q20" in source:
        placeholder_index = i
        break


if placeholder_index is None:
    raise ValueError(
        "Q10–Q20 placeholder was not found in the notebook."
    )


# ---------------------------------------------------------
# Q10–Q20 NOTEBOOK CELLS
# ---------------------------------------------------------

new_cells = []


new_cells.append(
    markdown(
        """## Sales Analysis — Q10 to Q20

This section analyzes the cleaned `vgsales` dataset.

The analysis covers regional sales, platform performance, yearly sales trends,
publishers, individual best-selling games, regional-platform relationships,
platform evolution, regional genre preferences, yearly regional changes,
publisher-level averages, and platform-specific best sellers.

**Unit of sales:** million units, as represented in the source dataset.

**Important data limitation:** The dataset becomes sparse in the most recent
years. Therefore, very low sales values in 2017 and 2020 should not be
interpreted as a confirmed industry decline."""
    )
)


# ---------------------------------------------------------
# Q10
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q10. Which region generates the most game sales?

Regional sales are calculated by summing the four regional sales columns:
`NA_Sales`, `EU_Sales`, `JP_Sales`, and `Other_Sales`."""
    )
)

new_cells.append(
    code(
        """regional_sales = {
    "North America": sales["NA_Sales"].sum(),
    "Europe": sales["EU_Sales"].sum(),
    "Japan": sales["JP_Sales"].sum(),
    "Other": sales["Other_Sales"].sum()
}

q10 = (
    pd.Series(regional_sales, name="Sales_Millions")
    .sort_values(ascending=False)
)

display(q10.to_frame())"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** North America records the largest cumulative
sales in the dataset, followed by Europe, Japan, and Other regions.

This describes cumulative sales within this dataset and does not by itself
represent current market share."""
    )
)


# ---------------------------------------------------------
# Q11
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q11. What are the best-selling platforms?

Platform performance is measured using total `Global_Sales`.
`Game_Count` is included to provide context for the sales totals."""
    )
)

new_cells.append(
    code(
        """q11 = (
    sales
    .groupby("Platform")
    .agg(
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Name", "count")
    )
    .sort_values("Total_Global_Sales", ascending=False)
)

display(q11.head(15))"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** PS2 has the largest cumulative global sales in
this dataset. Other high-volume platforms include X360, PS3, Wii, DS, and PS.

Platform totals are influenced by both the number of games represented and
their sales performance."""
    )
)


# ---------------------------------------------------------
# Q12
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q12. What is the trend of game releases and sales over years?

The analysis groups records by release year and calculates both the number of
game records and total global sales."""
    )
)

new_cells.append(
    code(
        """q12 = (
    sales
    .dropna(subset=["Year"])
    .groupby("Year")
    .agg(
        Game_Releases=("Name", "count"),
        Global_Sales=("Global_Sales", "sum")
    )
    .reset_index()
    .sort_values("Year")
)

display(q12)"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** Game releases and recorded global sales increase
substantially through the 2000s, with high activity around the late 2000s and
early 2010s.

The dataset has very limited observations for the most recent years. In
particular, 2017 and 2020 contain very few records, so their low sales totals
should be treated as a data-coverage limitation rather than automatically
interpreted as a market decline."""
    )
)


# ---------------------------------------------------------
# Q13
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q13. Who are the top publishers by sales?

Publishers are ranked by the sum of their recorded `Global_Sales`."""
    )
)

new_cells.append(
    code(
        """q13 = (
    sales
    .groupby("Publisher")
    .agg(
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Name", "count")
    )
    .sort_values("Total_Global_Sales", ascending=False)
)

display(q13.head(15))"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** Nintendo has the largest cumulative global sales
in the dataset, followed by Electronic Arts and Activision.

The `Game_Count` column provides context because publishers have different
numbers of records in the dataset."""
    )
)


# ---------------------------------------------------------
# Q14
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q14. Which games are the top 10 best-sellers globally?

The ranking uses the `Global_Sales` value recorded for each game/platform
record in the sales dataset."""
    )
)

new_cells.append(
    code(
        """q14 = (
    sales[
        ["Name", "Platform", "Year", "Publisher", "Global_Sales"]
    ]
    .sort_values("Global_Sales", ascending=False)
    .head(10)
)

display(q14)"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** Wii Sports has the largest recorded global sales
value in the dataset, followed by Super Mario Bros. and Mario Kart Wii.

These are sales records as represented in the source dataset."""
    )
)


# ---------------------------------------------------------
# Q15
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q15. How do regional sales compare for specific platforms?

Regional sales are aggregated by platform to compare North America, Europe,
Japan, and Other regions."""
    )
)

new_cells.append(
    code(
        """q15 = (
    sales
    .groupby("Platform")
    .agg(
        North_America=("NA_Sales", "sum"),
        Europe=("EU_Sales", "sum"),
        Japan=("JP_Sales", "sum"),
        Other=("Other_Sales", "sum"),
        Global_Sales=("Global_Sales", "sum")
    )
    .sort_values("Global_Sales", ascending=False)
)

display(q15.head(15))"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** Regional sales patterns differ across platforms.
For example, PS2 has large sales across North America and Europe, while
platforms such as NES, GB, and 3DS show comparatively substantial Japanese
sales within the dataset."""
    )
)


# ---------------------------------------------------------
# Q16
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q16. How has the market evolved by platform over time?

Sales are grouped by both year and platform. `Game_Count` shows the number of
records represented for each platform-year combination."""
    )
)

new_cells.append(
    code(
        """q16 = (
    sales
    .dropna(subset=["Year"])
    .groupby(["Year", "Platform"])
    .agg(
        Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Name", "count")
    )
    .reset_index()
    .sort_values(
        ["Year", "Global_Sales"],
        ascending=[True, False]
    )
)

display(q16)"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** The platform market changes over time as older
platforms decline and newer generations appear. The dataset shows transitions
from early systems such as Atari 2600 and NES through PlayStation, PS2, Xbox,
Wii/DS, and later PS4/Xbox One platforms.

Because the complete platform-year table is large, dashboard visualizations
should be used to make these transitions easier to explore."""
    )
)


# ---------------------------------------------------------
# Q17
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q17. What are the regional genre preferences?

Genre sales are aggregated separately for each geographic region."""
    )
)

new_cells.append(
    code(
        """q17 = (
    sales
    .groupby("Genre")
    .agg(
        North_America=("NA_Sales", "sum"),
        Europe=("EU_Sales", "sum"),
        Japan=("JP_Sales", "sum"),
        Other=("Other_Sales", "sum"),
        Global_Sales=("Global_Sales", "sum")
    )
    .sort_values("Global_Sales", ascending=False)
)

display(q17)"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** Action and Sports have high sales across several
regions. Role-Playing games show a comparatively large Japanese sales
component, while Shooter sales are much more concentrated in North America
and Europe within this dataset."""
    )
)


# ---------------------------------------------------------
# Q18
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q18. What is the yearly sales change per region?

Year-over-year absolute changes are calculated separately for each region."""
    )
)

new_cells.append(
    code(
        """q18 = (
    sales
    .dropna(subset=["Year"])
    .groupby("Year")
    .agg(
        North_America=("NA_Sales", "sum"),
        Europe=("EU_Sales", "sum"),
        Japan=("JP_Sales", "sum"),
        Other=("Other_Sales", "sum"),
        Global_Sales=("Global_Sales", "sum")
    )
    .reset_index()
    .sort_values("Year")
)

q18["NA_Change"] = q18["North_America"].diff()
q18["EU_Change"] = q18["Europe"].diff()
q18["JP_Change"] = q18["Japan"].diff()
q18["Other_Change"] = q18["Other"].diff()

display(q18)"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** Regional sales fluctuate substantially across
years. The strongest increases occur during periods of major platform and
market expansion, while later decreases should be interpreted alongside the
dataset's declining year coverage.

The first year has no previous year, so its change value is naturally `NaN`."""
    )
)


# ---------------------------------------------------------
# Q19
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q19. What is the average sales per publisher?

Average global sales are calculated as total recorded global sales divided by
the number of sales records for each publisher.

`Game_Count` is included because averages based on very small catalogues can
be unstable."""
    )
)

new_cells.append(
    code(
        """q19 = (
    sales
    .groupby("Publisher")
    .agg(
        Average_Global_Sales=("Global_Sales", "mean"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Name", "count")
    )
    .sort_values("Average_Global_Sales", ascending=False)
)

display(q19.head(15))"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** Publishers with only one or a few records can
have high average sales because their calculation is based on a very small
sample. Therefore, `Average_Global_Sales` should always be considered
alongside `Game_Count` and `Total_Global_Sales`."""
    )
)


# ---------------------------------------------------------
# Q20
# ---------------------------------------------------------

new_cells.append(
    markdown(
        """### Q20. What are the top 5 best-selling games per platform?

For each platform, records are sorted by global sales and the five highest
sales records are retained."""
    )
)

new_cells.append(
    code(
        """q20 = (
    sales
    .sort_values(
        ["Platform", "Global_Sales"],
        ascending=[True, False]
    )
    .groupby("Platform")
    .head(5)
)

display(
    q20[
        ["Platform", "Name", "Year", "Global_Sales"]
    ]
)"""
    )
)

new_cells.append(
    markdown(
        """**Interpretation:** The top-selling titles differ considerably by
platform. Examples include Wii Sports for Wii, Grand Theft Auto: San Andreas
for PS2, and Pokémon Red/Pokémon Blue for Game Boy.

This question is useful for platform-specific product and franchise analysis."""
    )
)


# ---------------------------------------------------------
# REPLACE PLACEHOLDER
# ---------------------------------------------------------

cells[placeholder_index:placeholder_index + 1] = new_cells

notebook["cells"] = cells

with open(NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)


print("Q10–Q20 notebook section added successfully.")
print("Notebook:", NOTEBOOK)
print("Total cells:", len(notebook["cells"]))