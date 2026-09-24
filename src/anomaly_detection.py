import pandas as pd


# ============================================================
# VIDEO GAME SALES ANALYSIS
# Phase 6 — Final Anomaly Detection
# Step 6.4 — Consolidated Anomaly Summary
# ============================================================


# ------------------------------------------------------------
# 1. Load processed datasets
# ------------------------------------------------------------

sales_file = "data/processed/sales_anomalies.csv"
regional_file = "data/processed/regional_sales_anomalies.csv"
engagement_file = "data/processed/engagement_sales_anomalies.csv"

sales = pd.read_csv(sales_file)
regional = pd.read_csv(regional_file)
engagement = pd.read_csv(engagement_file)


print("=" * 60)
print("PHASE 6.4 — FINAL ANOMALY SUMMARY")
print("=" * 60)


# ------------------------------------------------------------
# 2. Global sales anomaly summary
# ------------------------------------------------------------

global_summary = (
    sales["Sales_Anomaly"]
    .value_counts()
)


print("\nGlobal Sales Anomalies")
print("-" * 40)

print(global_summary.to_string())


# ------------------------------------------------------------
# 3. Regional anomaly summary
# ------------------------------------------------------------

regional_summary = (
    regional["Regional_Anomaly"]
    .value_counts()
)


print("\nRegional Sales Anomalies")
print("-" * 40)

print(regional_summary.to_string())


# ------------------------------------------------------------
# 4. Engagement vs sales anomaly summary
# ------------------------------------------------------------

engagement_summary = (
    engagement["Engagement_Sales_Anomaly"]
    .value_counts()
)


print("\nEngagement vs Sales Anomalies")
print("-" * 40)

print(engagement_summary.to_string())


# ------------------------------------------------------------
# 5. Create consolidated summary table
# ------------------------------------------------------------

summary_data = []


# Global sales anomalies

for category, count in global_summary.items():

    summary_data.append(
        {
            "Anomaly_Type": "Global Sales",
            "Anomaly_Category": category,
            "Record_Count": count
        }
    )


# Regional anomalies

for category, count in regional_summary.items():

    summary_data.append(
        {
            "Anomaly_Type": "Regional Sales",
            "Anomaly_Category": category,
            "Record_Count": count
        }
    )


# Engagement vs sales anomalies

for category, count in engagement_summary.items():

    summary_data.append(
        {
            "Anomaly_Type": "Engagement vs Sales",
            "Anomaly_Category": category,
            "Record_Count": count
        }
    )


summary = pd.DataFrame(summary_data)


# ------------------------------------------------------------
# 6. Display consolidated summary
# ------------------------------------------------------------

print("\nConsolidated Anomaly Summary")
print("-" * 60)

print(
    summary.to_string(index=False)
)


# ------------------------------------------------------------
# 7. Save consolidated summary
# ------------------------------------------------------------

output_path = (
    "data/processed/"
    "anomaly_summary.csv"
)

summary.to_csv(
    output_path,
    index=False
)


print("\nConsolidated anomaly summary saved to:")
print(output_path)


# ------------------------------------------------------------
# 8. Display anomaly datasets
# ------------------------------------------------------------

print("\nProcessed anomaly files")
print("-" * 60)

print("1.", sales_file)
print("2.", regional_file)
print("3.", engagement_file)
print("4.", output_path)


print("\n" + "=" * 60)
print("PHASE 6 COMPLETED")
print("=" * 60)