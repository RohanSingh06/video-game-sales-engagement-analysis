import sqlite3


# ============================================================
# PATH
# ============================================================

DATABASE_PATH = "database/video_game_analysis.db"


# ============================================================
# CONNECT TO DATABASE
# ============================================================

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


# ============================================================
# QUERY 1
# Total number of games
# ============================================================

query_1 = """
SELECT COUNT(*) AS total_games
FROM games;
"""

result = cursor.execute(query_1).fetchone()

print("\nQUERY 1 — TOTAL NUMBER OF GAMES")
print("Total games:", result[0])


# ============================================================
# QUERY 2
# Total number of sales records
# ============================================================

query_2 = """
SELECT COUNT(*) AS total_sales_records
FROM sales;
"""

result = cursor.execute(query_2).fetchone()

print("\nQUERY 2 — TOTAL SALES RECORDS")
print("Total sales records:", result[0])


# ============================================================
# QUERY 3
# Total global sales
# ============================================================

query_3 = """
SELECT
    ROUND(SUM(global_sales), 2) AS total_global_sales
FROM sales;
"""

result = cursor.execute(query_3).fetchone()

print("\nQUERY 3 — TOTAL GLOBAL SALES")
print("Total global sales:", result[0], "million")


# ============================================================
# QUERY 4
# Average global sales
# ============================================================

query_4 = """
SELECT
    ROUND(AVG(global_sales), 2) AS average_global_sales
FROM sales;
"""

result = cursor.execute(query_4).fetchone()

print("\nQUERY 4 — AVERAGE GLOBAL SALES")
print("Average global sales:", result[0], "million")


# ============================================================
# QUERY 5
# Global sales by platform
# ============================================================

query_5 = """
SELECT
    platform,
    COUNT(*) AS number_of_games,
    ROUND(SUM(global_sales), 2) AS total_global_sales
FROM sales
GROUP BY platform
ORDER BY total_global_sales DESC;
"""

results = cursor.execute(query_5).fetchall()

print("\nQUERY 5 — GLOBAL SALES BY PLATFORM")
print("-" * 60)

for row in results:
    print(
        f"Platform: {row[0]:<6} | "
        f"Games: {row[1]:<5} | "
        f"Global Sales: {row[2]} million"
    )


# ============================================================
# QUERY 6
# Global sales by genre
# ============================================================

query_6 = """
SELECT
    genre,
    COUNT(*) AS number_of_games,
    ROUND(SUM(global_sales), 2) AS total_global_sales
FROM sales
GROUP BY genre
ORDER BY total_global_sales DESC;
"""

results = cursor.execute(query_6).fetchall()

print("\nQUERY 6 — GLOBAL SALES BY GENRE")
print("-" * 60)

for row in results:
    print(
        f"Genre: {row[0]:<15} | "
        f"Games: {row[1]:<5} | "
        f"Global Sales: {row[2]} million"
    )


# ============================================================
# QUERY 7
# Top 10 publishers by global sales
# ============================================================

query_7 = """
SELECT
    publisher,
    COUNT(*) AS number_of_games,
    ROUND(SUM(global_sales), 2) AS total_global_sales
FROM sales
GROUP BY publisher
ORDER BY total_global_sales DESC
LIMIT 10;
"""

results = cursor.execute(query_7).fetchall()

print("\nQUERY 7 — TOP 10 PUBLISHERS BY GLOBAL SALES")
print("-" * 70)

for row in results:
    print(
        f"Publisher: {row[0]:<30} | "
        f"Games: {row[1]:<5} | "
        f"Global Sales: {row[2]} million"
    )


# ============================================================
# QUERY 8
# Global sales by year
# ============================================================

query_8 = """
SELECT
    year,
    COUNT(*) AS number_of_games,
    ROUND(SUM(global_sales), 2) AS total_global_sales
FROM sales
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year;
"""

results = cursor.execute(query_8).fetchall()

print("\nQUERY 8 — GLOBAL SALES BY YEAR")
print("-" * 60)

for row in results:
    print(
        f"Year: {row[0]} | "
        f"Games: {row[1]:<5} | "
        f"Global Sales: {row[2]} million"
    )


# ============================================================
# QUERY 9
# Regional sales comparison
# ============================================================

query_9 = """
SELECT
    ROUND(SUM(na_sales), 2) AS north_america_sales,
    ROUND(SUM(eu_sales), 2) AS europe_sales,
    ROUND(SUM(jp_sales), 2) AS japan_sales,
    ROUND(SUM(other_sales), 2) AS other_sales
FROM sales;
"""

result = cursor.execute(query_9).fetchone()

print("\nQUERY 9 — REGIONAL SALES COMPARISON")
print("-" * 60)

print("North America:", result[0], "million")
print("Europe:", result[1], "million")
print("Japan:", result[2], "million")
print("Other regions:", result[3], "million")


# ============================================================
# QUERY 10
# Top 10 individual games by global sales
# ============================================================

query_10 = """
SELECT
    name,
    platform,
    genre,
    publisher,
    ROUND(global_sales, 2) AS global_sales
FROM sales
ORDER BY global_sales DESC
LIMIT 10;
"""

results = cursor.execute(query_10).fetchall()

print("\nQUERY 10 — TOP 10 GAMES BY GLOBAL SALES")
print("-" * 90)

for row in results:
    print(
        f"Game: {row[0]:<35} | "
        f"Platform: {row[1]:<5} | "
        f"Genre: {row[2]:<15} | "
        f"Sales: {row[4]} million"
    )


# ============================================================
# QUERY 11
# Average global sales by genre
# ============================================================

query_11 = """
SELECT
    genre,
    COUNT(*) AS number_of_games,
    ROUND(AVG(global_sales), 2) AS average_global_sales
FROM sales
GROUP BY genre
ORDER BY average_global_sales DESC;
"""

results = cursor.execute(query_11).fetchall()

print("\nQUERY 11 — AVERAGE GLOBAL SALES BY GENRE")
print("-" * 70)

for row in results:
    print(
        f"Genre: {row[0]:<15} | "
        f"Games: {row[1]:<5} | "
        f"Average Sales: {row[2]} million"
    )


# ============================================================
# QUERY 12
# Average global sales by platform
# ============================================================

query_12 = """
SELECT
    platform,
    COUNT(*) AS number_of_games,
    ROUND(AVG(global_sales), 2) AS average_global_sales
FROM sales
GROUP BY platform
HAVING COUNT(*) >= 50
ORDER BY average_global_sales DESC;
"""

results = cursor.execute(query_12).fetchall()

print("\nQUERY 12 — AVERAGE GLOBAL SALES BY PLATFORM")
print("(Platforms with at least 50 records)")
print("-" * 70)

for row in results:
    print(
        f"Platform: {row[0]:<6} | "
        f"Games: {row[1]:<5} | "
        f"Average Sales: {row[2]} million"
    )


# ============================================================
# QUERY 13
# Game engagement with total global sales
# ============================================================

query_13 = """
SELECT
    g.title,
    ROUND(AVG(g.rating), 2) AS rating,
    MAX(g.plays) AS plays,
    MAX(g.playing) AS playing,
    MAX(g.backlogs) AS backlogs,
    MAX(g.wishlist) AS wishlist,
    ROUND(SUM(sales_data.global_sales), 2) AS total_global_sales

FROM games g

JOIN title_mapping tm
    ON g.normalized_title = tm.normalized_title

JOIN (
    SELECT
        normalized_name,
        SUM(global_sales) AS global_sales
    FROM sales
    GROUP BY normalized_name
) sales_data

    ON sales_data.normalized_name = tm.normalized_title

GROUP BY
    g.title,
    g.normalized_title

ORDER BY total_global_sales DESC;
"""

results = cursor.execute(query_13).fetchall()

print("\nQUERY 13 — GAME ENGAGEMENT WITH GLOBAL SALES")
print("-" * 110)

for row in results[:20]:
    print(
        f"Game: {row[0]:<35} | "
        f"Rating: {row[1]} | "
        f"Plays: {row[2]} | "
        f"Playing: {row[3]} | "
        f"Wishlist: {row[5]} | "
        f"Sales: {row[6]} million"
    )


# ============================================================
# QUERY 14
# Rating group vs global sales
# ============================================================

query_14 = """
SELECT
    rating_group,
    COUNT(*) AS number_of_games,
    ROUND(AVG(total_global_sales), 2) AS average_global_sales

FROM (

    SELECT
        g.normalized_title,

        CASE
            WHEN AVG(g.rating) < 2 THEN 'Below 2'
            WHEN AVG(g.rating) < 3 THEN '2 - 2.99'
            WHEN AVG(g.rating) < 4 THEN '3 - 3.99'
            WHEN AVG(g.rating) < 5 THEN '4 - 4.99'
            ELSE '5'
        END AS rating_group,

        SUM(sales_data.global_sales) AS total_global_sales

    FROM games g

    JOIN title_mapping tm
        ON g.normalized_title = tm.normalized_title

    JOIN (
        SELECT
            normalized_name,
            SUM(global_sales) AS global_sales
        FROM sales
        GROUP BY normalized_name
    ) sales_data

        ON sales_data.normalized_name = tm.normalized_title

    WHERE g.rating IS NOT NULL

    GROUP BY
        g.normalized_title
)

GROUP BY rating_group
ORDER BY rating_group;
"""

results = cursor.execute(query_14).fetchall()

print("\nQUERY 14 — RATING GROUP VS GLOBAL SALES")
print("-" * 70)

for row in results:
    print(
        f"Rating Group: {row[0]:<12} | "
        f"Games: {row[1]:<5} | "
        f"Average Sales: {row[2]} million"
    )


# ============================================================
# QUERY 15
# Plays vs global sales
# ============================================================

query_15 = """
SELECT
    g.title,
    MAX(g.plays) AS plays,
    ROUND(SUM(sales_data.global_sales), 2) AS total_global_sales

FROM games g

JOIN title_mapping tm
    ON g.normalized_title = tm.normalized_title

JOIN (
    SELECT
        normalized_name,
        SUM(global_sales) AS global_sales
    FROM sales
    GROUP BY normalized_name
) sales_data

    ON sales_data.normalized_name = tm.normalized_title

WHERE g.plays IS NOT NULL

GROUP BY
    g.title,
    g.normalized_title

ORDER BY plays DESC;
"""

results = cursor.execute(query_15).fetchall()

print("\nQUERY 15 — PLAYS VS GLOBAL SALES")
print("-" * 80)

for row in results[:20]:
    print(
        f"Game: {row[0]:<35} | "
        f"Plays: {row[1]:<10} | "
        f"Sales: {row[2]} million"
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()

print("\n" + "=" * 60)
print("SQL QUERIES 1–15 EXECUTED")
print("=" * 60)