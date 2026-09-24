-- ============================================================
-- VIDEO GAME SALES AND ENGAGEMENT ANALYSIS
-- Analytical SQL Queries
-- ============================================================

-- ============================================================
-- QUERY 1
-- TOTAL NUMBER OF GAMES
-- ============================================================

SELECT COUNT(*) AS total_games
FROM games;


-- ============================================================
-- QUERY 2
-- TOTAL NUMBER OF SALES RECORDS
-- ============================================================

SELECT COUNT(*) AS total_sales_records
FROM sales;


-- ============================================================
-- QUERY 3
-- TOTAL GLOBAL SALES
-- ============================================================

SELECT ROUND(SUM(global_sales), 2) AS total_global_sales_million
FROM sales;


-- ============================================================
-- QUERY 4
-- AVERAGE GLOBAL SALES
-- ============================================================

SELECT ROUND(AVG(global_sales), 2) AS average_global_sales_million
FROM sales;


-- ============================================================
-- QUERY 5
-- GLOBAL SALES BY PLATFORM
-- ============================================================

SELECT
    platform,
    COUNT(*) AS game_count,
    ROUND(SUM(global_sales), 2) AS global_sales_million
FROM sales
GROUP BY platform
ORDER BY global_sales_million DESC;


-- ============================================================
-- QUERY 6
-- GLOBAL SALES BY GENRE
-- ============================================================

SELECT
    genre,
    COUNT(*) AS game_count,
    ROUND(SUM(global_sales), 2) AS global_sales_million
FROM sales
GROUP BY genre
ORDER BY global_sales_million DESC;


-- ============================================================
-- QUERY 7
-- TOP 10 PUBLISHERS BY GLOBAL SALES
-- ============================================================

SELECT
    publisher,
    COUNT(*) AS game_count,
    ROUND(SUM(global_sales), 2) AS global_sales_million
FROM sales
GROUP BY publisher
ORDER BY global_sales_million DESC
LIMIT 10;


-- ============================================================
-- QUERY 8
-- GLOBAL SALES BY YEAR
-- ============================================================

SELECT
    year,
    COUNT(*) AS game_count,
    ROUND(SUM(global_sales), 2) AS global_sales_million
FROM sales
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year;


-- ============================================================
-- QUERY 9
-- REGIONAL SALES
-- ============================================================

SELECT
    ROUND(SUM(na_sales), 2) AS na_sales_million,
    ROUND(SUM(eu_sales), 2) AS eu_sales_million,
    ROUND(SUM(jp_sales), 2) AS jp_sales_million,
    ROUND(SUM(other_sales), 2) AS other_sales_million,
    ROUND(SUM(global_sales), 2) AS global_sales_million
FROM sales;


-- ============================================================
-- QUERY 10
-- TOP 10 INDIVIDUAL GAMES BY GLOBAL SALES
-- ============================================================

SELECT
    name,
    platform,
    year,
    genre,
    publisher,
    ROUND(global_sales, 2) AS global_sales_million
FROM sales
ORDER BY global_sales DESC
LIMIT 10;


-- ============================================================
-- QUERY 11
-- AVERAGE GLOBAL SALES BY GENRE
-- ============================================================

SELECT
    genre,
    COUNT(*) AS game_count,
    ROUND(AVG(global_sales), 2) AS average_sales_million
FROM sales
GROUP BY genre
ORDER BY average_sales_million DESC;


-- ============================================================
-- QUERY 12
-- AVERAGE GLOBAL SALES BY PLATFORM
-- Only platforms with at least 50 records
-- ============================================================

SELECT
    platform,
    COUNT(*) AS game_count,
    ROUND(AVG(global_sales), 2) AS average_sales_million
FROM sales
GROUP BY platform
HAVING COUNT(*) >= 50
ORDER BY average_sales_million DESC;


-- ============================================================
-- QUERY 13
-- GAME ENGAGEMENT WITH GLOBAL SALES
--
-- Important:
-- Games and sales can contain multiple records for the same
-- normalized title. Therefore both datasets are aggregated
-- before joining to prevent many-to-many duplication.
-- ============================================================

WITH games_agg AS (
    SELECT
        normalized_title,
        MAX(title) AS title,
        AVG(rating) AS rating,
        MAX(plays) AS plays,
        MAX(playing) AS playing,
        MAX(backlogs) AS backlogs,
        MAX(wishlist) AS wishlist
    FROM games
    GROUP BY normalized_title
),

sales_agg AS (
    SELECT
        normalized_name,
        SUM(global_sales) AS total_global_sales
    FROM sales
    GROUP BY normalized_name
)

SELECT
    g.title,
    ROUND(g.rating, 2) AS rating,
    g.plays,
    g.playing,
    g.backlogs,
    g.wishlist,
    ROUND(s.total_global_sales, 2) AS total_global_sales_million
FROM games_agg g
JOIN title_mapping tm
    ON g.normalized_title = tm.normalized_title
JOIN sales_agg s
    ON s.normalized_name = tm.normalized_title
ORDER BY s.total_global_sales DESC;


-- ============================================================
-- QUERY 14
-- RATING GROUP VS GLOBAL SALES
-- ============================================================

WITH games_agg AS (
    SELECT
        normalized_title,
        AVG(rating) AS rating
    FROM games
    WHERE rating IS NOT NULL
    GROUP BY normalized_title
),

sales_agg AS (
    SELECT
        normalized_name,
        SUM(global_sales) AS total_global_sales
    FROM sales
    GROUP BY normalized_name
),

merged AS (
    SELECT
        g.normalized_title,
        g.rating,
        s.total_global_sales
    FROM games_agg g
    JOIN title_mapping tm
        ON g.normalized_title = tm.normalized_title
    JOIN sales_agg s
        ON s.normalized_name = tm.normalized_title
)

SELECT
    CASE
        WHEN rating < 2 THEN 'Below 2'
        WHEN rating < 3 THEN '2 - 2.99'
        WHEN rating < 4 THEN '3 - 3.99'
        WHEN rating < 5 THEN '4 - 4.99'
        ELSE '5'
    END AS rating_group,

    COUNT(*) AS game_count,

    ROUND(AVG(total_global_sales), 2) AS average_sales_million

FROM merged

GROUP BY rating_group

ORDER BY
    CASE rating_group
        WHEN 'Below 2' THEN 1
        WHEN '2 - 2.99' THEN 2
        WHEN '3 - 3.99' THEN 3
        WHEN '4 - 4.99' THEN 4
        WHEN '5' THEN 5
    END;


-- ============================================================
-- QUERY 15
-- PLAYS VS GLOBAL SALES
-- ============================================================

WITH games_agg AS (
    SELECT
        normalized_title,
        MAX(title) AS title,
        MAX(plays) AS plays
    FROM games
    WHERE plays IS NOT NULL
    GROUP BY normalized_title
),

sales_agg AS (
    SELECT
        normalized_name,
        SUM(global_sales) AS total_global_sales
    FROM sales
    GROUP BY normalized_name
)

SELECT
    g.title,
    g.plays,
    ROUND(s.total_global_sales, 2) AS total_global_sales_million

FROM games_agg g

JOIN title_mapping tm
    ON g.normalized_title = tm.normalized_title

JOIN sales_agg s
    ON s.normalized_name = tm.normalized_title

ORDER BY
    g.plays DESC;