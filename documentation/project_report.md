
---

# 2. `documentation/project_report.md`

Delete everything currently inside `project_report.md` and paste this:

```markdown
# Video Game Sales and Engagement Analysis

## Data Science Capstone Project Report

---

# 1. Abstract

This project presents an end-to-end analysis of video game sales and player engagement using Python, SQL, SQLite, exploratory data analysis, anomaly detection, forecasting, and an interactive Streamlit dashboard.

Two complementary datasets were analyzed.

The first dataset contains game metadata, ratings, and player-engagement indicators such as plays, playing, backlogs, wishlist counts, and times listed.

The second dataset contains historical video-game sales by platform, genre, publisher, and geographic region.

The project workflow covers:

- Data inspection
- Data cleaning
- Data normalization
- Database creation
- SQL analysis
- EDA Q1–Q30
- Anomaly detection
- Sales forecasting
- Interactive dashboard development
- Testing
- Documentation

The final application, **GAMEPULSE — Video Game Intelligence Platform**, provides an interactive interface for exploring sales, engagement, regional performance, forecasting, and anomalies.

---

# 2. Introduction

The video-game industry generates data across multiple dimensions including:

- Game characteristics
- User ratings
- Player engagement
- Platforms
- Genres
- Publishers
- Regional markets
- Commercial sales

Analyzing these dimensions together can reveal patterns in game performance and market behavior.

This project uses data science techniques to transform raw video-game datasets into structured analytical outputs and an interactive dashboard.

---

# 3. Problem Statement

Raw video-game datasets can contain:

- Missing values
- Inconsistent text
- Different title formats
- Mixed numeric formats
- Multiple categorical representations
- Separate datasets requiring controlled matching

The project addresses the following problem:

> How can video-game sales, game metadata, ratings, and player-engagement information be cleaned, integrated, analyzed, and visualized to identify meaningful patterns in game performance and market behavior?

The project also evaluates simple forecasting approaches to establish a dataset-based baseline for future sales projection.

---

# 4. Objectives

The major objectives are:

1. Inspect and understand the available datasets.
2. Identify missing and inconsistent values.
3. Clean and normalize the datasets.
4. Normalize game titles for controlled cross-dataset matching.
5. Create a structured SQLite database.
6. Implement foreign-key relationships.
7. Develop SQL analytical queries.
8. Perform EDA Q1–Q30.
9. Analyze sales, engagement, ratings, platforms, genres, publishers, and regions.
10. Detect unusual sales and engagement patterns.
11. Evaluate multiple forecasting approaches.
12. Build an interactive Streamlit dashboard.
13. Test the complete application.
14. Document the findings and limitations.

---

# 5. Dataset Description

## 5.1 Games Dataset

The games dataset contains 1,512 game records.

Important fields include:

- Title
- Release Date
- Team
- Rating
- Times Listed
- Number of Reviews
- Genres
- Summary
- Reviews
- Plays
- Playing
- Backlogs
- Wishlist

The original dataset did not contain a Platform field.

Therefore, platform-level analysis is based on the sales dataset rather than assigning unsupported platform values to the games dataset.

---

## 5.2 Sales Dataset

The sales dataset contains 16,598 records.

Important fields include:

- Rank
- Name
- Platform
- Year
- Genre
- Publisher
- NA_Sales
- EU_Sales
- JP_Sales
- Other_Sales
- Global_Sales

The sales dataset provides the primary source for:

- Platform analysis
- Publisher analysis
- Genre sales
- Regional sales
- Global sales
- Historical sales trends

---

# 6. Data Inspection

## 6.1 Games Dataset

Original dimensions:

**1,512 rows × 14 columns**

Missing values:

| Column | Missing |
|---|---:|
| Team | 1 |
| Rating | 13 |
| Summary | 1 |

No exact duplicate rows were found.

The dataset also contained:

- K notation in numeric engagement fields
- List-like Genre values
- List-like Team values
- Date values requiring standardization

---

## 6.2 Sales Dataset

Original dimensions:

**16,598 rows × 11 columns**

Missing values:

| Column | Missing |
|---|---:|
| Year | 271 |
| Publisher | 58 |

No exact duplicate rows were found.

A consistency check compared regional sales totals with `Global_Sales`.

Maximum observed discrepancy:

**0.02 million**

No discrepancy exceeded 0.05 million.

The original Global_Sales values were retained.

---

# 7. Data Cleaning

## 7.1 Games Cleaning

The games cleaning process included:

1. Removing `Unnamed: 0`.
2. Trimming text values.
3. Handling missing Team values.
4. Handling missing Summary values.
5. Converting Release Date to datetime.
6. Converting K notation into numeric values.
7. Parsing Genre and Team fields.
8. Creating normalized titles.
9. Extracting Release Year.
10. Extracting Release Month.
11. Creating Month Name.

Final dimensions:

**1,512 rows × 17 columns**

Repeated-title records were retained because exact duplicates were not present and repeated titles can represent legitimate source records.

---

## 7.2 Sales Cleaning

The sales cleaning process included:

1. Converting Year to numeric format.
2. Handling missing year values.
3. Handling missing publisher values.
4. Standardizing categorical values.
5. Creating normalized game names.

Final dimensions:

**16,598 rows × 12 columns**

---

# 8. Title Normalization and Matching

The two datasets use different title columns:

- Games: `Title`
- Sales: `Name`

A normalized-title process was implemented to improve matching.

The controlled mapping process produced:

**486 title mappings**

Matching results included:

- 671 games records matched
- 1,022 sales records matched
- 428 title-level records available for engagement-sales anomaly analysis

Ambiguous title matches were handled separately.

The project avoids uncontrolled many-to-many joins because they can artificially inflate sales and engagement calculations.

---

# 9. Database Design

The project uses SQLite.

Database file:

```text
database/video_game_analysis.db