import pandas as pd

from title_normalization import normalize_title


GAMES_PATH = "data/processed/games_cleaned.csv"
VGSALES_PATH = "data/processed/vgsales_cleaned.csv"


def main():

    print("=" * 70)
    print("CROSS-DATASET TITLE VALIDATION")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load cleaned datasets
    # ---------------------------------------------------------

    games = pd.read_csv(GAMES_PATH)
    vgsales = pd.read_csv(VGSALES_PATH)

    print("\nDataset sizes:")
    print("Games:", games.shape)
    print("VGSales:", vgsales.shape)

    # ---------------------------------------------------------
    # Rebuild normalized titles using final normalization
    # ---------------------------------------------------------

    games["Normalized_Title"] = games["Title"].apply(normalize_title)
    vgsales["Normalized_Name"] = vgsales["Name"].apply(normalize_title)

    # ---------------------------------------------------------
    # Unique normalized titles
    # ---------------------------------------------------------

    games_titles = set(
        games["Normalized_Title"].dropna().unique()
    )

    vgsales_titles = set(
        vgsales["Normalized_Name"].dropna().unique()
    )

    matched_titles = games_titles.intersection(vgsales_titles)

    unmatched_games = games_titles - vgsales_titles
    unmatched_vgsales = vgsales_titles - games_titles

    print("\n" + "=" * 70)
    print("TITLE MATCHING RESULTS")
    print("=" * 70)

    print("\nUnique normalized titles:")
    print("Games:", len(games_titles))
    print("VGSales:", len(vgsales_titles))

    print("\nMatched normalized titles:", len(matched_titles))

    print(
        "Games match percentage:",
        round(
            len(matched_titles) / len(games_titles) * 100,
            2
        ),
        "%"
    )

    print(
        "VGSales match percentage:",
        round(
            len(matched_titles) / len(vgsales_titles) * 100,
            2
        ),
        "%"
    )

    print("\nUnmatched games titles:", len(unmatched_games))
    print("Unmatched VGSales titles:", len(unmatched_vgsales))

    # ---------------------------------------------------------
    # Duplicate normalized titles
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("DUPLICATE NORMALIZED TITLES")
    print("=" * 70)

    games_duplicates = (
        games.groupby("Normalized_Title")
        .size()
        .reset_index(name="Count")
        .query("Count > 1")
        .sort_values("Count", ascending=False)
    )

    vgsales_duplicates = (
        vgsales.groupby("Normalized_Name")
        .size()
        .reset_index(name="Count")
        .query("Count > 1")
        .sort_values("Count", ascending=False)
    )

    print("\nGames duplicate normalized titles:")
    print(len(games_duplicates))

    print("\nTop 20:")
    print(games_duplicates.head(20).to_string(index=False))

    print("\nVGSales duplicate normalized titles:")
    print(len(vgsales_duplicates))

    print("\nTop 20:")
    print(vgsales_duplicates.head(20).to_string(index=False))

    # ---------------------------------------------------------
    # Show matched examples
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("MATCHED TITLE EXAMPLES")
    print("=" * 70)

    matched_games = (
        games[
            games["Normalized_Title"].isin(matched_titles)
        ][["Title", "Normalized_Title"]]
        .drop_duplicates()
        .sort_values("Title")
    )

    matched_vgsales = (
        vgsales[
            vgsales["Normalized_Name"].isin(matched_titles)
        ][["Name", "Normalized_Name"]]
        .drop_duplicates()
        .sort_values("Name")
    )

    matched_examples = (
        matched_games
        .merge(
            matched_vgsales,
            left_on="Normalized_Title",
            right_on="Normalized_Name",
            how="inner"
        )
        .drop(columns=["Normalized_Name"])
        .drop_duplicates()
    )

    print(
        matched_examples.head(30).to_string(index=False)
    )

    # ---------------------------------------------------------
    # Save mapping candidates
    # ---------------------------------------------------------

    mapping = matched_examples[
        ["Title", "Name", "Normalized_Title"]
    ].copy()

    mapping = mapping.rename(
        columns={
            "Normalized_Title": "Normalized_Title"
        }
    )

    mapping.to_csv(
        "data/processed/title_mapping_candidates.csv",
        index=False
    )

    print("\nMapping candidates saved to:")
    print(
        "data/processed/title_mapping_candidates.csv"
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("CROSS-DATASET VALIDATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()