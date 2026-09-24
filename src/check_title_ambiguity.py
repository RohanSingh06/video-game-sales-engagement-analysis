import pandas as pd


GAMES_PATH = "data/processed/games_cleaned.csv"
VGSALES_PATH = "data/processed/vgsales_cleaned.csv"


def main():

    print("=" * 70)
    print("TITLE AMBIGUITY CHECK")
    print("=" * 70)

    games = pd.read_csv(GAMES_PATH)
    vgsales = pd.read_csv(VGSALES_PATH)

    # ---------------------------------------------------------
    # Games ambiguity
    # ---------------------------------------------------------

    games_ambiguity = (
        games.groupby("Normalized_Title")["Title"]
        .nunique()
        .reset_index(name="Distinct_Original_Titles")
    )

    games_ambiguity = games_ambiguity[
        games_ambiguity["Distinct_Original_Titles"] > 1
    ].sort_values(
        "Distinct_Original_Titles",
        ascending=False
    )

    # ---------------------------------------------------------
    # VGSales ambiguity
    # ---------------------------------------------------------

    vgsales_ambiguity = (
        vgsales.groupby("Normalized_Name")["Name"]
        .nunique()
        .reset_index(name="Distinct_Original_Names")
    )

    vgsales_ambiguity = vgsales_ambiguity[
        vgsales_ambiguity["Distinct_Original_Names"] > 1
    ].sort_values(
        "Distinct_Original_Names",
        ascending=False
    )

    # ---------------------------------------------------------
    # Games results
    # ---------------------------------------------------------

    print("\nGames ambiguous normalized titles:")
    print(len(games_ambiguity))

    if len(games_ambiguity) > 0:

        print("\nTop 20:")
        print(
            games_ambiguity.head(20)
            .to_string(index=False)
        )

        print("\nExamples:")

        for title in games_ambiguity.head(10)["Normalized_Title"]:

            values = (
                games.loc[
                    games["Normalized_Title"] == title,
                    "Title"
                ]
                .drop_duplicates()
                .tolist()
            )

            print(f"{title} -> {values}")

    # ---------------------------------------------------------
    # VGSales results
    # ---------------------------------------------------------

    print("\nVGSales ambiguous normalized names:")
    print(len(vgsales_ambiguity))

    if len(vgsales_ambiguity) > 0:

        print("\nTop 20:")
        print(
            vgsales_ambiguity.head(20)
            .to_string(index=False)
        )

        print("\nExamples:")

        for title in vgsales_ambiguity.head(10)["Normalized_Name"]:

            values = (
                vgsales.loc[
                    vgsales["Normalized_Name"] == title,
                    "Name"
                ]
                .drop_duplicates()
                .tolist()
            )

            print(f"{title} -> {values}")

    # ---------------------------------------------------------
    # Matched titles
    # ---------------------------------------------------------

    games_titles = set(
        games["Normalized_Title"].dropna()
    )

    vgsales_titles = set(
        vgsales["Normalized_Name"].dropna()
    )

    matched = games_titles.intersection(vgsales_titles)

    print("\nMatched normalized titles:", len(matched))

    matched_games_ambiguous = games_ambiguity[
        games_ambiguity["Normalized_Title"].isin(matched)
    ]

    matched_vgsales_ambiguous = vgsales_ambiguity[
        vgsales_ambiguity["Normalized_Name"].isin(matched)
    ]

    print(
        "Ambiguous matched titles in Games:",
        len(matched_games_ambiguous)
    )

    print(
        "Ambiguous matched titles in VGSales:",
        len(matched_vgsales_ambiguous)
    )

    print("\n" + "=" * 70)
    print("TITLE AMBIGUITY CHECK COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()