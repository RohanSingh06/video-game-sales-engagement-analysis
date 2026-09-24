
# Video Game Sales and Engagement Analysis
## Key Insights

This document summarizes the major findings from the completed data cleaning, SQL analysis, EDA Q1–Q30, anomaly detection, and forecasting phases of the project.

---

## 1. Dataset Overview

The project uses two complementary datasets.

### Games Dataset

The games dataset contains:

- 1,512 game records
- Game titles
- Release dates
- Teams/developers
- Ratings
- Times Listed
- Number of Reviews
- Genres
- Plays
- Playing
- Backlogs
- Wishlist

### Sales Dataset

The sales dataset contains:

- 16,598 records
- Game names
- Platforms
- Years
- Genres
- Publishers
- North American sales
- European sales
- Japanese sales
- Other regional sales
- Global sales

The cleaned sales dataset contains:

- 31 platforms
- 12 genres
- 578 publishers

Total recorded global sales:

**8,920.44 million units**

---

# 2. Data Quality Insights

## Games Dataset

The original games dataset contained 1,512 rows and 14 columns.

Missing values were found in:

| Column | Missing Values |
|---|---:|
| Team | 1 |
| Rating | 13 |
| Summary | 1 |

The cleaning process included:

- Removing the unused `Unnamed: 0` column
- Trimming text values
- Handling missing Team values
- Handling missing Summary values
- Converting Release Date into datetime format
- Converting K notation into numeric values
- Parsing list-like Genre and Team fields
- Creating normalized titles
- Extracting release year
- Extracting release month
- Extracting month names

The cleaned games dataset contains:

**1,512 rows × 17 columns**

No exact duplicate rows were present in the original dataset.

---

## Sales Dataset

The original sales dataset contained 16,598 rows and 11 columns.

Missing values were found in:

| Column | Missing Values |
|---|---:|
| Year | 271 |
| Publisher | 58 |

The sales cleaning process included:

- Converting Year to numeric format
- Handling missing values
- Standardizing categorical values
- Creating normalized game names

A sales consistency check compared `Global_Sales` with the sum of regional sales.

The maximum observed discrepancy was:

**0.02 million**

No discrepancy exceeded 0.05 million.

The original `Global_Sales` values were therefore retained.

---

# 3. Database Insights

The project uses SQLite as the relational database.

The database contains:

| Table | Records |
|---|---:|
| games | 1,512 |
| sales | 16,598 |
| title_mapping | 486 |

Foreign-key relationships were implemented between the game/sales records and the title-mapping table.

Foreign-key integrity validation passed.

The database provides the structured foundation for SQL analysis and dashboard integration.

---

# 4. Title Matching Insights

The two datasets use different title columns:

- Games dataset: `Title`
- Sales dataset: `Name`

A normalized-title matching process was implemented.

The controlled title-mapping process produced:

**486 title mappings**

Matching results included:

- 671 games records matched through the mapping relationship
- 1,022 sales records matched through the mapping relationship
- 428 title-level records available for engagement-sales anomaly analysis

Ambiguous normalized titles were handled separately rather than blindly joining them.

This reduced the risk of many-to-many duplication during cross-dataset analysis.

---

# 5. Sales Insights

## 5.1 Regional Sales

| Region | Sales (Million) |
|---|---:|
| North America | 4,392.95 |
| Europe | 2,434.13 |
| Japan | 1,291.02 |
| Other | 797.75 |

North America has the largest aggregate recorded sales volume.

---

## 5.2 Platform Sales

The highest-selling platforms include:

| Platform | Global Sales (Million) |
|---|---:|
| PS2 | 1,255.64 |
| X360 | 979.96 |
| PS3 | 957.84 |
| WII | 926.71 |
| DS | 822.49 |
| PS | 730.66 |

---

## 5.3 Genre Sales

The highest-selling genres include:

| Genre | Global Sales (Million) |
|---|---:|
| Action | 1,751.18 |
| Sports | 1,330.93 |
| Shooter | 1,037.37 |
| RPG | 927.37 |
| Platform | 831.37 |

---

## 5.4 Publisher Sales

The highest-selling publishers include:

| Publisher | Global Sales (Million) |
|---|---:|
| Nintendo | 1,786.56 |
| Electronic Arts | 1,110.32 |
| Activision | 727.46 |
| Sony Computer Entertainment | 607.50 |
| Ubisoft | 474.72 |

Publisher averages should be interpreted carefully when publishers have very few games.

---

# 6. Best-Selling Games

The highest-selling individual games include:

| Game | Global Sales (Million) |
|---|---:|
| Wii Sports | 82.74 |
| Super Mario Bros. | 40.24 |
| Mario Kart Wii | 35.82 |
| Wii Sports Resort | 33.00 |
| Pokémon Red/Blue | 31.37 |
| Tetris | 30.26 |

---

# 7. Historical Sales Trend

Annual global sales were analyzed from 1980 to 2016.

The highest annual sales occurred in:

**2008 — 678.90 million**

Selected annual values:

| Year | Global Sales (Million) |
|---|---:|
| 2008 | 678.90 |
| 2009 | 667.30 |
| 2010 | 600.45 |
| 2011 | 515.99 |
| 2012 | 363.54 |
| 2013 | 368.11 |
| 2014 | 337.05 |
| 2015 | 264.44 |
| 2016 | 70.93 |

The dataset becomes sparse after 2016.

Therefore, the decline after 2016 should not be interpreted as a complete representation of the real-world video-game market.

---

# 8. Game Ratings

The games dataset contains:

- Rated games: **1,499**
- Mean rating: **3.72**
- Median rating: **3.80**
- Minimum rating: **0.70**
- Maximum rating: **4.80**

The correlation between user rating and global sales was:

**0.0121**

This indicates a very weak linear relationship between rating and global sales within the analyzed data.

Correlation does not establish causation.

---

# 9. Wishlist and Sales

The correlation between wishlist count and global sales was:

**-0.0691**

Average sales across wishlist quartiles:

| Wishlist Quartile | Average Sales (Million) |
|---|---:|
| Q1 | 4.894 |
| Q2 | 5.004 |
| Q3 | 3.998 |
| Q4 | 3.730 |

The analysis does not show a strong positive linear relationship between wishlist count and global sales.

---

# 10. Engagement Analysis

The engagement measure used:

```text
Plays + Playing + Backlogs + Wishlist
