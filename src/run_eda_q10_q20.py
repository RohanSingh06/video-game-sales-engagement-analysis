import pandas as pd
import numpy as np

print("=" * 70)
print("VIDEO GAME ANALYSIS — EDA QUESTIONS Q10–Q20")
print("=" * 70)

# ---------------------------------------------------------
# LOAD CLEANED SALES DATA
# ---------------------------------------------------------

sales = pd.read_csv(r"data\processed\vgsales_cleaned.csv")

print("\nDataset loaded successfully.")
print("Sales records:", len(sales))

print("\nColumns:")
print(sales.columns.tolist())


# =========================================================
# Q10 — WHICH REGION GENERATES THE MOST GAME SALES?
# =========================================================

print("\n" + "=" * 70)
print("Q10. REGION GENERATING THE MOST GAME SALES")
print("=" * 70)

regional_sales = {
    "North America": sales["NA_Sales"].sum(),
    "Europe": sales["EU_Sales"].sum(),
    "Japan": sales["JP_Sales"].sum(),
    "Other": sales["Other_Sales"].sum()
}

q10 = (
    pd.Series(regional_sales, name="Sales_Millions")
    .sort_values(ascending=False)
)

print(q10.to_string())

print(
    f"\nHighest regional sales: "
    f"{q10.index[0]} — {q10.iloc[0]:.2f} million"
)


# =========================================================
# Q11 — BEST-SELLING PLATFORMS
# =========================================================

print("\n" + "=" * 70)
print("Q11. BEST-SELLING PLATFORMS")
print("=" * 70)

q11 = (
    sales
    .groupby("Platform")
    .agg(
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Name", "count")
    )
    .sort_values("Total_Global_Sales", ascending=False)
    .head(15)
)

print(q11.to_string())


# =========================================================
# Q12 — TREND OF GAME RELEASES AND SALES OVER YEARS
# =========================================================

print("\n" + "=" * 70)
print("Q12. GAME RELEASES AND SALES TREND OVER YEARS")
print("=" * 70)

q12 = (
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

print(q12.to_string(index=False))


# =========================================================
# Q13 — TOP PUBLISHERS BY SALES
# =========================================================

print("\n" + "=" * 70)
print("Q13. TOP PUBLISHERS BY GLOBAL SALES")
print("=" * 70)

q13 = (
    sales
    .groupby("Publisher")
    .agg(
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Name", "count")
    )
    .sort_values("Total_Global_Sales", ascending=False)
    .head(15)
)

print(q13.to_string())


# =========================================================
# Q14 — TOP 10 BEST-SELLING GAMES GLOBALLY
# =========================================================

print("\n" + "=" * 70)
print("Q14. TOP 10 BEST-SELLING GAMES GLOBALLY")
print("=" * 70)

q14 = (
    sales[
        ["Name", "Platform", "Year", "Publisher", "Global_Sales"]
    ]
    .sort_values("Global_Sales", ascending=False)
    .head(10)
)

print(q14.to_string(index=False))


# =========================================================
# Q15 — REGIONAL SALES FOR SPECIFIC PLATFORMS
# =========================================================

print("\n" + "=" * 70)
print("Q15. REGIONAL SALES BY PLATFORM")
print("=" * 70)

q15 = (
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
    .head(15)
)

print(q15.to_string())


# =========================================================
# Q16 — MARKET EVOLUTION BY PLATFORM OVER TIME
# =========================================================

print("\n" + "=" * 70)
print("Q16. MARKET EVOLUTION BY PLATFORM OVER TIME")
print("=" * 70)

q16 = (
    sales
    .dropna(subset=["Year"])
    .groupby(["Year", "Platform"])
    .agg(
        Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Name", "count")
    )
    .reset_index()
    .sort_values(["Year", "Global_Sales"], ascending=[True, False])
)

print(q16.to_string(index=False))


# =========================================================
# Q17 — REGIONAL GENRE PREFERENCES
# =========================================================

print("\n" + "=" * 70)
print("Q17. REGIONAL GENRE PREFERENCES")
print("=" * 70)

q17 = (
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

print(q17.to_string())


# =========================================================
# Q18 — YEARLY SALES CHANGE PER REGION
# =========================================================

print("\n" + "=" * 70)
print("Q18. YEARLY SALES CHANGE PER REGION")
print("=" * 70)

q18 = (
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

# Calculate year-over-year absolute change
q18["NA_Change"] = q18["North_America"].diff()
q18["EU_Change"] = q18["Europe"].diff()
q18["JP_Change"] = q18["Japan"].diff()
q18["Other_Change"] = q18["Other"].diff()

print(q18.to_string(index=False))


# =========================================================
# Q19 — AVERAGE SALES PER PUBLISHER
# =========================================================

print("\n" + "=" * 70)
print("Q19. AVERAGE SALES PER PUBLISHER")
print("=" * 70)

q19 = (
    sales
    .groupby("Publisher")
    .agg(
        Average_Global_Sales=("Global_Sales", "mean"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Game_Count=("Name", "count")
    )
    .sort_values("Average_Global_Sales", ascending=False)
    .head(15)
)

print(q19.to_string())


# =========================================================
# Q20 — TOP 5 BEST-SELLING GAMES PER PLATFORM
# =========================================================

print("\n" + "=" * 70)
print("Q20. TOP 5 BEST-SELLING GAMES PER PLATFORM")
print("=" * 70)

q20 = (
    sales
    .sort_values(
        ["Platform", "Global_Sales"],
        ascending=[True, False]
    )
    .groupby("Platform")
    .head(5)
)

for platform, group in q20.groupby("Platform"):
    print("\n" + "-" * 50)
    print(f"Platform: {platform}")
    print("-" * 50)

    print(
        group[
            ["Name", "Year", "Global_Sales"]
        ].to_string(index=False)
    )


# =========================================================
# COMPLETION
# =========================================================

print("\n" + "=" * 70)
print("Q10–Q20 EDA EXECUTION COMPLETED SUCCESSFULLY")
print("=" * 70)