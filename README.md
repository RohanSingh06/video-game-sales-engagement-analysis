# 🎮 Video Game Sales and Engagement Analysis

## Data Science Capstone Project

An end-to-end data science project for analyzing **video game sales, player engagement, ratings, platforms, genres, publishers, and regional markets**.

The project combines Python, SQL, SQLite, exploratory data analysis, anomaly detection, forecasting, and an interactive Streamlit dashboard into a single analytical workflow.

---

## 📌 Project Overview

The video-game industry generates large amounts of data across different dimensions such as:

- Game metadata
- User ratings
- Player engagement
- Platforms
- Genres
- Publishers
- Regional markets
- Global sales

This project analyzes two complementary datasets:

1. **Games Dataset** — game metadata, ratings, and engagement indicators.
2. **Video Game Sales Dataset** — historical sales by game, platform, genre, publisher, and region.

The project follows a complete data science pipeline:

```text
Raw Data
   ↓
Data Inspection
   ↓
Data Cleaning
   ↓
Data Normalization
   ↓
Title Matching
   ↓
SQLite Database
   ↓
SQL Analysis
   ↓
EDA Q1–Q30
   ↓
Anomaly Detection
   ↓
Sales Forecasting
   ↓
Interactive Dashboard
   ↓
Insights & Documentation
```

---

# 🎯 Objectives

The main objectives of the project are:

- Inspect and understand the source datasets.
- Identify missing and inconsistent values.
- Clean and standardize the datasets.
- Normalize game titles for controlled cross-dataset analysis.
- Build a relational SQLite database.
- Implement SQL analytical queries.
- Perform 30 exploratory data analysis questions.
- Analyze game sales and player engagement.
- Analyze platforms, genres, publishers, and regions.
- Identify unusual sales and engagement patterns.
- Evaluate basic sales forecasting approaches.
- Build an interactive Streamlit dashboard.
- Document analytical findings and limitations.

---

# 📊 Datasets

## 1. Games Dataset

The games dataset contains **1,512 records**.

Important fields include:

| Column | Description |
|---|---|
| Title | Game title |
| Release Date | Game release date |
| Team | Developer/team information |
| Rating | User rating |
| Times Listed | Number of times listed |
| Number of Reviews | Number of reviews |
| Genres | Game genre/categories |
| Summary | Game description |
| Reviews | Review information |
| Plays | Number of plays |
| Playing | Number of users currently playing |
| Backlogs | Number of users with the game in backlog |
| Wishlist | Number of wishlist entries |

---

## 2. Video Game Sales Dataset

The sales dataset contains **16,598 records**.

Important fields include:

| Column | Description |
|---|---|
| Rank | Sales rank |
| Name | Game name |
| Platform | Gaming platform |
| Year | Release year |
| Genre | Game genre |
| Publisher | Publisher |
| NA_Sales | North American sales |
| EU_Sales | European sales |
| JP_Sales | Japanese sales |
| Other_Sales | Other regional sales |
| Global_Sales | Global sales |

---

# 🧹 Data Cleaning

The project includes separate cleaning workflows for both datasets.

## Games Dataset

Cleaning operations include:

- Removing the unused index column.
- Trimming text values.
- Handling missing Team values.
- Handling missing Summary values.
- Converting release dates to datetime.
- Converting K notation into numeric values.
- Standardizing Genre values.
- Standardizing Team values.
- Creating normalized game titles.
- Extracting release year.
- Extracting release month.
- Creating month names.

Final cleaned dataset:

```text
1,512 rows × 17 columns
```

---

## Sales Dataset

Cleaning operations include:

- Converting Year into numeric format.
- Handling missing Year values.
- Handling missing Publisher values.
- Standardizing categorical values.
- Creating normalized game names.

Final cleaned dataset:

```text
16,598 rows × 12 columns
```

A sales consistency check was also performed by comparing regional sales with `Global_Sales`.

The maximum observed difference was:

```text
0.02 million
```

---

# 🔗 Cross-Dataset Title Matching

The two datasets use different title fields:

```text
Games Dataset  → Title
Sales Dataset  → Name
```

A normalized-title matching workflow was implemented.

The controlled title mapping produced:

```text
486 title mappings
```

Matching results included:

```text
Games records matched → 671
Sales records matched → 1,022
Title-level records available for engagement-sales analysis → 428
```

Ambiguous title matches were handled separately.

Controlled aggregation was used before selected joins to avoid many-to-many duplication.

---

# 🗄️ Database

The project uses **SQLite** as the relational database.

Database:

```text
database/video_game_analysis.db
```

Core tables:

```text
games
sales
title_mapping
```

Record counts:

| Table | Records |
|---|---:|
| games | 1,512 |
| sales | 16,598 |
| title_mapping | 486 |

Foreign-key relationships were implemented and validated.

---

# 🧮 SQL Analysis

The project contains SQL analytical queries covering:

- Total global sales
- Average global sales
- Platform performance
- Genre performance
- Publisher performance
- Yearly sales
- Regional sales
- Best-selling games
- Average genre sales
- Average platform sales
- Engagement and sales relationships

SQL queries are located at:

```text
sql/analytical_queries.sql
```

The Python SQL execution script is:

```text
src/run_sql_queries.py
```

---

# 🔍 Exploratory Data Analysis

The project implements **30 EDA questions**.

## Games & Engagement Analysis

Questions Q1–Q9 cover:

- Top-rated games
- Developer ratings
- Common genres
- Backlog vs wishlist
- Release trends
- Rating distribution
- Wishlist analysis
- Plays by genre
- Developer/studio analysis

## Sales Analysis

Questions Q10–Q20 cover:

- Regional sales
- Platform sales
- Sales trends
- Publisher sales
- Best-selling games
- Regional platform performance
- Platform evolution
- Regional genre preferences
- Yearly regional changes
- Publisher averages
- Top games per platform

## Combined Analysis

Questions Q21–Q30 cover:

- Genre sales
- Rating vs sales
- High-rated games by platform
- Release and sales trends
- Wishlist vs sales
- Engagement vs sales
- Listed interest vs ratings
- Engagement by genre
- Genre-platform combinations
- Regional genre sales

---

# 🚨 Anomaly Detection

Three major anomaly categories were analyzed.

## Global Sales Anomalies

IQR-based detection identified:

```text
Normal records       → 14,705
High-sales outliers  → 1,893
```

Upper IQR threshold:

```text
1.085 million
```

---

## Regional Concentration

Using a 75% dominant-region threshold:

```text
Concentrated records → 9,060
Normal records       → 7,538
```

---

## Engagement-Sales Anomalies

Among 428 matched title-level records:

```text
Normal                         → 415
High engagement / low sales    → 7
Low engagement / high sales    → 6
```

---

# 📈 Sales Forecasting

Historical sales were analyzed using the reliable period:

```text
1980–2016
```

The highest annual sales occurred in:

```text
2008 → 678.90 million
```

Three approaches were evaluated:

- Naive Baseline
- Linear Regression
- Holt Exponential Smoothing

Evaluation period:

```text
Training → 1980–2010
Testing  → 2011–2015
```

## Model Evaluation

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Naive Baseline | 69.03M | 85.59M | 19.24% |
| Linear Regression | 253.55M | 276.97M | 78.20% |
| Holt Exponential Smoothing | 291.31M | 310.68M | 88.69% |

The final future projection uses a simple dataset-based baseline because sales coverage becomes sparse after 2016.

---

# 📊 Dashboard

The project includes an interactive **Streamlit dashboard** called:

# GAMEPULSE

Dashboard file:

```text
app/dashboard.py
```

The dashboard contains six sections.

### 1. Overview

Provides:

- Total games
- Global sales
- Platforms
- Publishers
- Genres
- Sales trend
- Top platforms
- Genre performance
- Regional sales
- Top-selling games

### 2. Sales Analysis

Provides:

- Platform filters
- Genre filters
- Sales KPIs
- Platform analysis
- Publisher analysis
- Yearly sales
- Top-selling games

### 3. Game & Engagement

Provides:

- Average rating
- Median rating
- Rated games
- Rating distribution
- Wishlist analysis
- Engagement by genre

### 4. Regional Analysis

Provides:

- Regional KPIs
- Regional sales
- Regional sales share
- Regional genre performance

### 5. Forecasting

Provides:

- Historical sales
- Forecast model comparison
- Future baseline projection
- Forecast limitations

### 6. Anomaly Analysis

Provides:

- Anomaly summary
- Sales anomalies
- Regional concentration
- Engagement-sales anomalies

---

# 🛠️ Technology Stack

## Programming Language

```text
Python 3.12
```

## Data Analysis

```text
pandas
numpy
```

## Visualization

```text
matplotlib
seaborn
plotly
```

## Machine Learning & Forecasting

```text
scikit-learn
statsmodels
```

## Database

```text
SQLite
SQLAlchemy
```

## Application

```text
Streamlit
```

## Development

```text
Jupyter Notebook
```

---

# 📁 Project Structure

```text
video-game-analysis/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   │   ├── games.csv
│   │   └── vgsales.csv
│   │
│   └── processed/
│       ├── annual_sales_forecasting.csv
│       ├── anomaly_summary.csv
│       ├── engagement_sales_anomalies.csv
│       ├── forecast_model_comparison.csv
│       ├── future_sales_forecast.csv
│       ├── future_sales_forecast.png
│       ├── games_cleaned.csv
│       ├── historical_sales_trend.png
│       ├── regional_sales_anomalies.csv
│       ├── sales_anomalies.csv
│       └── vgsales_cleaned.csv
│
├── database/
│   └── video_game_analysis.db
│
├── documentation/
│   ├── insights.md
│   ├── project_report.md
│   └── screenshots/
│
├── notebooks/
│   └── 01_dataset_inspection.ipynb
│
├── sql/
│   └── analytical_queries.sql
│
├── src/
│   ├── add_eda_q1_q9.py
│   ├── add_eda_q10_q20.py
│   ├── add_eda_q21_q30.py
│   ├── anomaly_detection.py
│   ├── check_sales_consistency.py
│   ├── check_title_ambiguity.py
│   ├── clean_games.py
│   ├── clean_vgsales.py
│   ├── create_database.py
│   ├── cross_dataset_validation.py
│   ├── data_inspection.py
│   ├── run_eda_q1_q9.py
│   ├── run_eda_q10_q20.py
│   ├── run_eda_q21_q30.py
│   ├── run_sql_queries.py
│   ├── sales_forecasting.py
│   ├── title_matching.py
│   └── title_normalization.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🚀 Installation

## 1. Clone or copy the project

Open a terminal in the project directory:

```powershell
cd D:\guvi\video-game-analysis\video-game-analysis
```

---

## 2. Create a virtual environment

```powershell
python -m venv venv
```

---

## 3. Activate the virtual environment

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, Python can still be used directly from the environment.

---

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# ▶️ Running the Dashboard

From the project root:

```powershell
streamlit run app/dashboard.py
```

Streamlit will start the application and provide a local URL.

Usually:

```text
http://localhost:8501
```

Open the URL in a browser to access GAMEPULSE.

---

# 📓 Running the Notebook

The dataset inspection notebook is located at:

```text
notebooks/01_dataset_inspection.ipynb
```

Launch Jupyter:

```powershell
jupyter notebook
```

Then open the notebook from the Jupyter interface.

---

# 🗃️ Database

The SQLite database is already included:

```text
database/video_game_analysis.db
```

The database can be inspected using SQLite-compatible database tools.

The database contains the structured analytical tables used by the project.

---

# 📂 Important Output Files

### Cleaned Data

```text
data/processed/games_cleaned.csv
data/processed/vgsales_cleaned.csv
```

### Forecasting

```text
data/processed/annual_sales_forecasting.csv
data/processed/forecast_model_comparison.csv
data/processed/future_sales_forecast.csv
data/processed/historical_sales_trend.png
data/processed/future_sales_forecast.png
```

### Anomaly Detection

```text
data/processed/anomaly_summary.csv
data/processed/sales_anomalies.csv
data/processed/regional_sales_anomalies.csv
data/processed/engagement_sales_anomalies.csv
```

### Documentation

```text
documentation/insights.md
documentation/project_report.md
```

---

# 📌 Key Findings

Some of the major findings from the analysis are:

- Total recorded global sales: **8,920.44M**
- North American sales: **4,392.95M**
- PS2 global sales: **1,255.64M**
- Action genre global sales: **1,751.18M**
- Nintendo global sales: **1,786.56M**
- Wii Sports global sales: **82.74M**
- Peak annual sales: **678.90M in 2008**
- Rating vs global sales correlation: **0.0121**
- Wishlist vs global sales correlation: **-0.0691**
- Listed-interest vs rating correlation: **0.5082**

These figures describe patterns within the available datasets and should be interpreted alongside the documented limitations.

---

# ⚠️ Limitations

### Sparse Recent Sales Data

The sales dataset becomes sparse after 2016.

Therefore, later-year declines should not automatically be interpreted as a complete representation of the real-world video-game market.

### Cross-Dataset Matching

Only controlled title mappings were used when connecting the games and sales datasets.

### Multi-Genre Games

Games associated with multiple genres can contribute to multiple genre-level calculations.

### Publisher Averages

Average publisher sales can be affected by publishers with very small numbers of games.

### Correlation

Correlation measures association and does not establish causation.

### Forecasting

The forecasting results are dataset-based baseline projections and are not intended to represent a complete real-world market forecast.

---

# 📚 Documentation

Detailed project documentation is available in:

```text
documentation/project_report.md
```

Key analytical insights are summarized in:

```text
documentation/insights.md
```

---

# 👨‍💻 Project

**Project:** Video Game Sales and Engagement Analysis

**Application:** GAMEPULSE — Video Game Intelligence Platform

**Domain:** Data Science / Gaming Analytics

**Core Areas:**

```text
Data Cleaning
Data Analysis
SQL
Database Management
EDA
Visualization
Anomaly Detection
Forecasting
Dashboard Development
```

---

# 📄 License / Academic Use

This project was developed as an academic data science project for learning and analytical demonstration.

The datasets are used for analysis and educational purposes according to their respective source/distribution terms.