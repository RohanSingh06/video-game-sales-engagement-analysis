import os
import sqlite3
import pandas as pd


# ============================================================
# PATHS
# ============================================================

GAMES_PATH = "data/processed/games_cleaned.csv"
VGSALES_PATH = "data/processed/vgsales_cleaned.csv"

DATABASE_DIR = "database"
DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "video_game_analysis.db"
)


# ============================================================
# DATABASE CREATION
# ============================================================

def create_database():

    print("=" * 70)
    print("VIDEO GAME ANALYSIS DATABASE CREATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Create database directory
    # --------------------------------------------------------

    os.makedirs(DATABASE_DIR, exist_ok=True)

    # --------------------------------------------------------
    # Load cleaned datasets
    # --------------------------------------------------------

    print("\nLoading cleaned datasets...")

    games = pd.read_csv(GAMES_PATH)
    vgsales = pd.read_csv(VGSALES_PATH)

    print("Games records:", len(games))
    print("VGSales records:", len(vgsales))

    # --------------------------------------------------------
    # Verify required source columns
    # --------------------------------------------------------

    required_games_columns = [
        "Title",
        "Normalized_Title"
    ]

    required_sales_columns = [
        "Name",
        "Normalized_Name"
    ]

    for column in required_games_columns:
        if column not in games.columns:
            raise ValueError(
                f"Required Games column missing: {column}"
            )

    for column in required_sales_columns:
        if column not in vgsales.columns:
            raise ValueError(
                f"Required VGSales column missing: {column}"
            )

    # --------------------------------------------------------
    # Create controlled title mapping
    # --------------------------------------------------------

    print("\nCreating controlled title mapping...")

    games_titles = (
        games[
            ["Title", "Normalized_Title"]
        ]
        .dropna(subset=["Normalized_Title"])
        .drop_duplicates()
    )

    vgsales_titles = (
        vgsales[
            ["Name", "Normalized_Name"]
        ]
        .dropna(subset=["Normalized_Name"])
        .drop_duplicates()
    )

    # --------------------------------------------------------
    # Rename mapping columns
    # --------------------------------------------------------

    games_titles = games_titles.rename(
        columns={
            "Title": "games_title",
            "Normalized_Title": "normalized_title"
        }
    )

    vgsales_titles = vgsales_titles.rename(
        columns={
            "Name": "vgsales_name",
            "Normalized_Name": "normalized_title"
        }
    )

    # --------------------------------------------------------
    # One representative title per normalized title
    # --------------------------------------------------------

    games_titles = (
        games_titles
        .sort_values("games_title")
        .drop_duplicates(
            subset=["normalized_title"],
            keep="first"
        )
    )

    vgsales_titles = (
        vgsales_titles
        .sort_values("vgsales_name")
        .drop_duplicates(
            subset=["normalized_title"],
            keep="first"
        )
    )

    # --------------------------------------------------------
    # Controlled inner join
    # --------------------------------------------------------

    title_mapping = games_titles.merge(
        vgsales_titles,
        on="normalized_title",
        how="inner"
    )

    print(
        "Controlled title mappings:",
        len(title_mapping)
    )

    # --------------------------------------------------------
    # Rename Games columns
    # --------------------------------------------------------

    games = games.rename(
        columns={
            "Title": "title",
            "Normalized_Title": "normalized_title",
            "Release Date": "release_date",
            "Release_Year": "release_year",
            "Release_Month": "release_month",
            "Release_Month_Name": "release_month_name",
            "Team": "team",
            "Rating": "rating",
            "Times Listed": "times_listed",
            "Number of Reviews": "number_of_reviews",
            "Genres": "genres",
            "Summary": "summary",
            "Reviews": "reviews",
            "Plays": "plays",
            "Playing": "playing",
            "Backlogs": "backlogs",
            "Wishlist": "wishlist"
        }
    )

    # --------------------------------------------------------
    # Rename VGSales columns
    # --------------------------------------------------------

    vgsales = vgsales.rename(
        columns={
            "Rank": "rank",
            "Name": "name",
            "Normalized_Name": "normalized_name",
            "Platform": "platform",
            "Year": "year",
            "Genre": "genre",
            "Publisher": "publisher",
            "NA_Sales": "na_sales",
            "EU_Sales": "eu_sales",
            "JP_Sales": "jp_sales",
            "Other_Sales": "other_sales",
            "Global_Sales": "global_sales"
        }
    )

    # --------------------------------------------------------
    # Verify renamed columns
    # --------------------------------------------------------

    if "normalized_title" not in games.columns:
        raise ValueError(
            "Games column 'normalized_title' was not created."
        )

    if "normalized_name" not in vgsales.columns:
        raise ValueError(
            "Sales column 'normalized_name' was not created."
        )

    # --------------------------------------------------------
    # Connect to SQLite
    # --------------------------------------------------------

    print("\nCreating SQLite database...")

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Enable foreign key enforcement
    cursor.execute(
        "PRAGMA foreign_keys = ON"
    )

    # --------------------------------------------------------
    # Drop existing tables
    # --------------------------------------------------------

    cursor.execute(
        "DROP TABLE IF EXISTS games"
    )

    cursor.execute(
        "DROP TABLE IF EXISTS sales"
    )

    cursor.execute(
        "DROP TABLE IF EXISTS title_mapping"
    )

    # --------------------------------------------------------
    # TITLE MAPPING TABLE
    # --------------------------------------------------------

    # Parent table must be created first.

    cursor.execute("""
        CREATE TABLE title_mapping (

            mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,

            normalized_title TEXT NOT NULL UNIQUE,

            games_title TEXT NOT NULL,

            vgsales_name TEXT NOT NULL
        )
    """)

    # --------------------------------------------------------
    # Insert title mapping
    # --------------------------------------------------------

    print("\nInserting title mapping...")

    title_mapping.to_sql(
        "title_mapping",
        connection,
        if_exists="append",
        index=False,
        chunksize=50
    )

    # --------------------------------------------------------
    # Retrieve generated mapping IDs
    # --------------------------------------------------------

    mapping_ids = pd.read_sql_query(
        """
        SELECT
            mapping_id,
            normalized_title
        FROM title_mapping
        """,
        connection
    )

    print(
        "Generated mapping IDs:",
        len(mapping_ids)
    )

    # --------------------------------------------------------
    # Add mapping_id to Games
    # --------------------------------------------------------

    games = games.merge(
        mapping_ids,
        on="normalized_title",
        how="left"
    )

    # --------------------------------------------------------
    # Add mapping_id to Sales
    # --------------------------------------------------------

    vgsales = vgsales.merge(
        mapping_ids,
        left_on="normalized_name",
        right_on="normalized_title",
        how="left"
    )

    # Remove mapping-side normalized title
    vgsales = vgsales.drop(
        columns=["normalized_title"]
    )

    # --------------------------------------------------------
    # GAMES TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE games (

            game_id INTEGER PRIMARY KEY AUTOINCREMENT,

            mapping_id INTEGER,

            title TEXT NOT NULL,

            normalized_title TEXT NOT NULL,

            release_date TEXT,

            release_year INTEGER,

            release_month INTEGER,

            release_month_name TEXT,

            team TEXT,

            rating REAL,

            times_listed INTEGER,

            number_of_reviews INTEGER,

            genres TEXT,

            summary TEXT,

            reviews TEXT,

            plays INTEGER,

            playing INTEGER,

            backlogs INTEGER,

            wishlist INTEGER,

            FOREIGN KEY (mapping_id)
                REFERENCES title_mapping(mapping_id)
        )
    """)

    # --------------------------------------------------------
    # SALES TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE sales (

            sales_id INTEGER PRIMARY KEY AUTOINCREMENT,

            mapping_id INTEGER,

            rank INTEGER,

            name TEXT NOT NULL,

            normalized_name TEXT NOT NULL,

            platform TEXT NOT NULL,

            year INTEGER,

            genre TEXT,

            publisher TEXT,

            na_sales REAL,

            eu_sales REAL,

            jp_sales REAL,

            other_sales REAL,

            global_sales REAL,

            FOREIGN KEY (mapping_id)
                REFERENCES title_mapping(mapping_id)
        )
    """)

    # --------------------------------------------------------
    # Insert Games data
    # --------------------------------------------------------

    print("\nInserting Games data...")

    games.to_sql(
        "games",
        connection,
        if_exists="append",
        index=False,
        chunksize=50
    )

    # --------------------------------------------------------
    # Insert Sales data
    # --------------------------------------------------------

    print("Inserting VGSales data...")

    vgsales.to_sql(
        "sales",
        connection,
        if_exists="append",
        index=False,
        chunksize=50
    )

    # --------------------------------------------------------
    # Create indexes
    # --------------------------------------------------------

    print("\nCreating indexes...")

    cursor.execute("""
        CREATE INDEX idx_games_normalized_title
        ON games(normalized_title)
    """)

    cursor.execute("""
        CREATE INDEX idx_games_mapping_id
        ON games(mapping_id)
    """)

    cursor.execute("""
        CREATE INDEX idx_sales_normalized_name
        ON sales(normalized_name)
    """)

    cursor.execute("""
        CREATE INDEX idx_sales_mapping_id
        ON sales(mapping_id)
    """)

    cursor.execute("""
        CREATE INDEX idx_sales_platform
        ON sales(platform)
    """)

    cursor.execute("""
        CREATE INDEX idx_sales_genre
        ON sales(genre)
    """)

    cursor.execute("""
        CREATE INDEX idx_sales_publisher
        ON sales(publisher)
    """)

    cursor.execute("""
        CREATE INDEX idx_sales_year
        ON sales(year)
    """)

    # --------------------------------------------------------
    # Commit
    # --------------------------------------------------------

    connection.commit()

    # --------------------------------------------------------
    # DATABASE VALIDATION
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATABASE VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Foreign key status
    # --------------------------------------------------------

    foreign_keys_status = cursor.execute(
        "PRAGMA foreign_keys"
    ).fetchone()[0]

    print(
        "\nForeign key enforcement:",
        "ON" if foreign_keys_status == 1 else "OFF"
    )

    # --------------------------------------------------------
    # Tables
    # --------------------------------------------------------

    tables = cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

    print("\nTables created:")

    for table in tables:
        print("-", table[0])

    # --------------------------------------------------------
    # Record counts
    # --------------------------------------------------------

    print("\nRecord counts:")

    for table_name in [
        "games",
        "sales",
        "title_mapping"
    ]:

        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        print(
            f"{table_name}: {count}"
        )

    # --------------------------------------------------------
    # Validate mapping
    # --------------------------------------------------------

    mapping_count = cursor.execute("""
        SELECT COUNT(*)
        FROM title_mapping
    """).fetchone()[0]

    print(
        "\nControlled title matches:",
        mapping_count
    )

    # --------------------------------------------------------
    # Mapping coverage
    # --------------------------------------------------------

    games_mapped = cursor.execute("""
        SELECT COUNT(*)
        FROM games
        WHERE mapping_id IS NOT NULL
    """).fetchone()[0]

    sales_mapped = cursor.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE mapping_id IS NOT NULL
    """).fetchone()[0]

    print("\nForeign key mapping coverage:")

    print(
        f"Games mapped: {games_mapped} / {len(games)}"
    )

    print(
        f"Sales mapped: {sales_mapped} / {len(vgsales)}"
    )

    # --------------------------------------------------------
    # Foreign key integrity check
    # --------------------------------------------------------

    fk_errors = cursor.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    print("\nForeign key integrity check:")

    if len(fk_errors) == 0:
        print(
            "PASSED — No foreign key violations found."
        )
    else:
        print(
            "FAILED — Foreign key violations found:"
        )

        for error in fk_errors:
            print(error)

    # --------------------------------------------------------
    # Foreign key definitions
    # --------------------------------------------------------

    print("\nGames foreign keys:")

    games_fks = cursor.execute(
        "PRAGMA foreign_key_list(games)"
    ).fetchall()

    for fk in games_fks:
        print(fk)

    print("\nSales foreign keys:")

    sales_fks = cursor.execute(
        "PRAGMA foreign_key_list(sales)"
    ).fetchall()

    for fk in sales_fks:
        print(fk)

    # --------------------------------------------------------
    # Sample Games record
    # --------------------------------------------------------

    print("\nSample Games record:")

    sample_game = cursor.execute("""
        SELECT
            game_id,
            mapping_id,
            title,
            normalized_title,
            rating
        FROM games
        LIMIT 1
    """).fetchone()

    print(sample_game)

    # --------------------------------------------------------
    # Sample Sales record
    # --------------------------------------------------------

    print("\nSample Sales record:")

    sample_sale = cursor.execute("""
        SELECT
            sales_id,
            mapping_id,
            name,
            platform,
            global_sales
        FROM sales
        LIMIT 1
    """).fetchone()

    print(sample_sale)

    # --------------------------------------------------------
    # Sample Title Mapping
    # --------------------------------------------------------

    print("\nSample Title Mapping:")

    sample_mapping = cursor.execute("""
        SELECT
            mapping_id,
            games_title,
            vgsales_name
        FROM title_mapping
        LIMIT 1
    """).fetchone()

    print(sample_mapping)

    # --------------------------------------------------------
    # Close database
    # --------------------------------------------------------

    connection.close()

    print("\nDatabase saved to:")
    print(DATABASE_PATH)

    print("\n" + "=" * 70)
    print("DATABASE CREATION COMPLETED")
    print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    create_database()