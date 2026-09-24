# ============================================================
# VIDEO GAME SALES AND ENGAGEMENT ANALYSIS
# Sales Forecasting
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing


# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = "./data/processed/vgsales_cleaned.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("VIDEO GAME SALES FORECASTING")
print("=" * 70)

print()
print("Dataset shape:", df.shape)


# ============================================================
# 2. PREPARE DATA
# ============================================================

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Global_Sales"] = pd.to_numeric(
    df["Global_Sales"],
    errors="coerce"
)

df = df.dropna(subset=["Year", "Global_Sales"])

df["Year"] = df["Year"].astype(int)

# Use the reliable historical period
forecasting_df = df[
    (df["Year"] >= 1980) &
    (df["Year"] <= 2016)
].copy()


print()
print("Forecasting period:")
print("Start year:", forecasting_df["Year"].min())
print("End year:", forecasting_df["Year"].max())
print("Records:", len(forecasting_df))


# ============================================================
# 3. CREATE ANNUAL SALES SERIES
# ============================================================

annual_sales = (
    forecasting_df
    .groupby("Year")["Global_Sales"]
    .sum()
    .reset_index()
    .sort_values("Year")
)

print()
print("Annual sales:")
print(annual_sales.to_string(index=False))


# ============================================================
# 4. CHECK YEAR COVERAGE
# ============================================================

expected_years = set(
    range(
        annual_sales["Year"].min(),
        annual_sales["Year"].max() + 1
    )
)

actual_years = set(annual_sales["Year"])

missing_years = sorted(
    expected_years - actual_years
)

print()
print("Missing years in forecasting period:")
print(missing_years if missing_years else "None")


# ============================================================
# 5. BASIC HISTORICAL STATISTICS
# ============================================================

peak_row = annual_sales.loc[
    annual_sales["Global_Sales"].idxmax()
]

lowest_row = annual_sales.loc[
    annual_sales["Global_Sales"].idxmin()
]

print()
print("Peak annual sales:")
print(
    f"{int(peak_row['Year'])}: "
    f"{peak_row['Global_Sales']:.2f} million"
)

print()
print("Lowest annual sales:")
print(
    f"{int(lowest_row['Year'])}: "
    f"{lowest_row['Global_Sales']:.2f} million"
)


# ============================================================
# 6. SAVE ANNUAL SALES DATA
# ============================================================

annual_sales.to_csv(
    "./data/processed/annual_sales_forecasting.csv",
    index=False
)

print()
print("Saved:")
print("./data/processed/annual_sales_forecasting.csv")


# ============================================================
# 7. HISTORICAL SALES VISUALIZATION
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    annual_sales["Year"],
    annual_sales["Global_Sales"],
    marker="o"
)

plt.title("Annual Global Video Game Sales")
plt.xlabel("Year")
plt.ylabel("Global Sales (Million)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "./data/processed/historical_sales_trend.png",
    dpi=300
)

plt.close()

print()
print("Saved:")
print("./data/processed/historical_sales_trend.png")

print()
print("Historical sales preparation completed.")


# ============================================================
# 8. COMMON FORECASTING EVALUATION PERIOD
# ============================================================

print()
print("=" * 70)
print("COMMON FORECASTING EVALUATION PERIOD")
print("=" * 70)

train = annual_sales[
    annual_sales["Year"] <= 2010
].copy()

test = annual_sales[
    (annual_sales["Year"] >= 2011) &
    (annual_sales["Year"] <= 2015)
].copy()

print()
print("Training period:")
print("1980–2010")

print()
print("Testing period:")
print("2011–2015")


# ============================================================
# 9. EVALUATION FUNCTION
# ============================================================

def calculate_metrics(actual, predicted):

    actual = np.array(actual)
    predicted = np.array(predicted)

    mae = np.mean(
        np.abs(actual - predicted)
    )

    rmse = np.sqrt(
        np.mean(
            (actual - predicted) ** 2
        )
    )

    mape = np.mean(
        np.abs(
            (actual - predicted) / actual
        )
    ) * 100

    return mae, rmse, mape


# ============================================================
# 10. NAIVE FORECASTING BASELINE
# ============================================================

print()
print("=" * 70)
print("NAIVE FORECASTING BASELINE")
print("=" * 70)

naive_predictions = []

for year in test["Year"]:

    previous_year = year - 1

    previous_value = annual_sales.loc[
        annual_sales["Year"] == previous_year,
        "Global_Sales"
    ].iloc[0]

    naive_predictions.append(
        previous_value
    )

naive_results = test.copy()

naive_results["Naive_Forecast"] = naive_predictions

print()
print("Naive predictions:")
print(
    naive_results.to_string(index=False)
)

naive_mae, naive_rmse, naive_mape = calculate_metrics(
    test["Global_Sales"],
    naive_predictions
)

print()
print("Naive evaluation:")
print(f"MAE : {naive_mae:.2f} million")
print(f"RMSE: {naive_rmse:.2f} million")
print(f"MAPE: {naive_mape:.2f}%")

print()
print("Naive baseline completed.")


# ============================================================
# 11. LINEAR REGRESSION
# ============================================================

print()
print("=" * 70)
print("LINEAR REGRESSION FORECASTING MODEL")
print("=" * 70)

X_train = train[["Year"]]
y_train = train["Global_Sales"]

X_test = test[["Year"]]

linear_model = LinearRegression()

linear_model.fit(
    X_train,
    y_train
)

linear_predictions = linear_model.predict(
    X_test
)

linear_results = test.copy()

linear_results[
    "Linear_Regression_Forecast"
] = linear_predictions

print()
print("Linear Regression predictions:")
print(
    linear_results.to_string(index=False)
)

linear_mae, linear_rmse, linear_mape = calculate_metrics(
    test["Global_Sales"],
    linear_predictions
)

print()
print("Linear Regression evaluation:")
print(f"MAE : {linear_mae:.2f} million")
print(f"RMSE: {linear_rmse:.2f} million")
print(f"MAPE: {linear_mape:.2f}%")

print()
print("Linear Regression equation:")

print(
    f"Sales = "
    f"{linear_model.coef_[0]:.4f} × Year + "
    f"{linear_model.intercept_:.2f}"
)

print()
print("Linear Regression model completed.")


# ============================================================
# 12. HOLT EXPONENTIAL SMOOTHING
# ============================================================

print()
print("=" * 70)
print("HOLT EXPONENTIAL SMOOTHING MODEL")
print("=" * 70)

holt_train = train["Global_Sales"].reset_index(
    drop=True
)

holt_test = test["Global_Sales"].reset_index(
    drop=True
)

holt_model = ExponentialSmoothing(
    holt_train,
    trend="add",
    seasonal=None,
    initialization_method="estimated"
)

holt_fitted = holt_model.fit(
    optimized=True
)

holt_predictions = holt_fitted.forecast(
    len(holt_test)
)

holt_results = test.copy()

holt_results[
    "Holt_Forecast"
] = holt_predictions.values

print()
print("Holt predictions:")
print(
    holt_results.to_string(index=False)
)

holt_mae, holt_rmse, holt_mape = calculate_metrics(
    holt_test,
    holt_predictions
)

print()
print("Holt evaluation:")
print(f"MAE : {holt_mae:.2f} million")
print(f"RMSE: {holt_rmse:.2f} million")
print(f"MAPE: {holt_mape:.2f}%")

print()
print("Holt Exponential Smoothing model completed.")


# ============================================================
# 13. MODEL COMPARISON
# ============================================================

print()
print("=" * 70)
print("FORECASTING MODEL COMPARISON")
print("=" * 70)

comparison = pd.DataFrame({

    "Model": [
        "Naive Baseline",
        "Linear Regression",
        "Holt Exponential Smoothing"
    ],

    "MAE": [
        naive_mae,
        linear_mae,
        holt_mae
    ],

    "RMSE": [
        naive_rmse,
        linear_rmse,
        holt_rmse
    ],

    "MAPE": [
        naive_mape,
        linear_mape,
        holt_mape
    ]

})

print()
print("Evaluation period: 2011–2015")

print()
print("Model comparison:")

print(
    comparison.to_string(
        index=False,
        formatters={
            "MAE": "{:.2f}".format,
            "RMSE": "{:.2f}".format,
            "MAPE": "{:.2f}%".format
        }
    )
)

comparison.to_csv(
    "./data/processed/forecast_model_comparison.csv",
    index=False
)

print()
print("Saved:")
print("./data/processed/forecast_model_comparison.csv")


# ============================================================
# 14. FINAL FORECAST MODEL
# ============================================================

print()
print("=" * 70)
print("FINAL FORECAST")
print("=" * 70)

print()
print(
    "The validated baseline is used for the dataset-based "
    "future projection."
)

# ------------------------------------------------------------
# Naive forecasting approach:
# future year's forecast = latest observed annual sales
# ------------------------------------------------------------

last_year = annual_sales["Year"].max()

last_sales = annual_sales.loc[
    annual_sales["Year"] == last_year,
    "Global_Sales"
].iloc[0]

forecast_years = list(
    range(
        last_year + 1,
        last_year + 6
    )
)

future_forecast = pd.DataFrame({

    "Year": forecast_years,

    "Forecast_Global_Sales": [
        last_sales
        for _ in forecast_years
    ]

})

print()
print("Latest observed year:")
print(last_year)

print()
print("Latest observed annual sales:")
print(
    f"{last_sales:.2f} million"
)

print()
print("Future forecast:")
print(
    future_forecast.to_string(index=False)
)


# ============================================================
# 15. SAVE FUTURE FORECAST
# ============================================================

future_forecast.to_csv(
    "./data/processed/future_sales_forecast.csv",
    index=False
)

print()
print("Saved:")
print("./data/processed/future_sales_forecast.csv")


# ============================================================
# 16. HISTORICAL + FUTURE FORECAST VISUALIZATION
# ============================================================

plt.figure(figsize=(13, 7))

# Historical data
plt.plot(
    annual_sales["Year"],
    annual_sales["Global_Sales"],
    marker="o",
    label="Historical Sales"
)

# Forecast data
plt.plot(
    future_forecast["Year"],
    future_forecast["Forecast_Global_Sales"],
    marker="o",
    linestyle="--",
    label="Future Forecast"
)

# Forecast boundary
plt.axvline(
    x=last_year,
    linestyle=":"
)

plt.title(
    "Video Game Global Sales: Historical Trend and Future Forecast"
)

plt.xlabel("Year")

plt.ylabel(
    "Global Sales (Million)"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "./data/processed/future_sales_forecast.png",
    dpi=300
)

plt.close()

print()
print("Saved:")
print("./data/processed/future_sales_forecast.png")


# ============================================================
# 17. FORECASTING SUMMARY
# ============================================================

print()
print("=" * 70)
print("FORECASTING SUMMARY")
print("=" * 70)

print()
print("Historical data:")
print(
    f"{annual_sales['Year'].min()}–"
    f"{annual_sales['Year'].max()}"
)

print()
print("Model evaluation:")
print("2011–2015")

print()
print("Future projection:")
print(
    f"{forecast_years[0]}–"
    f"{forecast_years[-1]}"
)

print()
print(
    "Forecast assumption: future annual sales remain "
    "equal to the latest observed annual sales."
)

print()
print(
    "Important limitation: the dataset has sparse "
    "coverage after 2016, so this projection should "
    "be interpreted as a dataset-based baseline rather "
    "than a real-world market forecast."
)

print()
print("=" * 70)
print("FORECASTING PHASE COMPLETED")
print("=" * 70)