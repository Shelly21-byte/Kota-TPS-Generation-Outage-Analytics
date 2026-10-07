print("Kota TPS Python Analysis Started")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Excel workbook
file_path = "Kota_TPS_Cleaned_Workbook.xlsx"

# Load both sheets
station_df = pd.read_excel(file_path, sheet_name="Station_Daily")
unit_df = pd.read_excel(file_path, sheet_name="Unit_Daily")

# Check whether data loaded correctly
print("\nStation Daily Shape:")
print(station_df.shape)

print("\nUnit Daily Shape:")
print(unit_df.shape)

print("\nStation Daily Columns:")
print(station_df.columns.tolist())

print("\nUnit Daily Columns:")
print(unit_df.columns.tolist())
print("\nStation Daily Shape:")
print(station_df.shape)

print("\nUnit Daily Shape:")
print(unit_df.shape)

print("\nStation Daily Columns:")
print(station_df.columns.tolist())

print("\nUnit Daily Columns:")
print(unit_df.columns.tolist())
# ============================================================
# STEP 3.2 - RECALCULATE KPIs USING PYTHON
# ============================================================

# Daily Variance
unit_df["Python_Variance_MU"] = (
    unit_df["Actual_MU"] - unit_df["Program_MU"]
)

# Program Achievement %
unit_df["Python_Achievement"] = np.where(
    unit_df["Program_MU"] > 0,
    (unit_df["Actual_MU"] / unit_df["Program_MU"]) * 100,
    np.nan
)

# Daily PLF %
unit_df["Python_PLF"] = (
    (unit_df["Actual_MU"] * 1000) /
    (unit_df["Capacity_MW"] * 24)
) * 100

print("\n--- Python KPI Check ---")

print(
    unit_df[
        [
            "Date",
            "Unit_Label",
            "Capacity_MW",
            "Program_MU",
            "Actual_MU",
            "Python_Variance_MU",
            "Python_Achievement",
            "Python_PLF"
        ]
    ].head(10)
)
# ============================================================
# STEP 3.3 - CROSS CHECK PYTHON KPIs WITH EXCEL KPIs
# ============================================================

unit_df["PLF_Difference"] = (
    unit_df["Python_PLF"] - unit_df["PLF"]
).abs()

unit_df["Variance_Difference"] = (
    unit_df["Python_Variance_MU"] - unit_df["Variance_MU"]
).abs()

unit_df["Achievement_Difference"] = (
    unit_df["Python_Achievement"] - unit_df["Achievement"]
).abs()

print("\n--- KPI Cross Validation ---")

print("Maximum PLF Difference:")
print(unit_df["PLF_Difference"].max())

print("\nMaximum Variance Difference:")
print(unit_df["Variance_Difference"].max())

print("\nMaximum Achievement Difference:")
print(unit_df["Achievement_Difference"].max())
# ============================================================
# STEP 3.3A - INSPECT EXCEL VS PYTHON KPI VALUES
# ============================================================

print("\n--- Excel vs Python KPI Sample ---")

print(
    unit_df[
        [
            "Date",
            "Unit_Label",
            "PLF",
            "Python_PLF",
            "Achievement",
            "Python_Achievement",
            "Variance_MU",
            "Python_Variance_MU"
        ]
    ].head(10).to_string(index=False)
)
# ============================================================
# STEP 3.3B - CORRECT KPI CROSS VALIDATION
# Excel stores PLF and Achievement as decimals (0-1)
# Python calculations are percentages (0-100)
# ============================================================

unit_df["PLF_Difference_Corrected"] = (
    unit_df["Python_PLF"] - (unit_df["PLF"] * 100)
).abs()

unit_df["Achievement_Difference_Corrected"] = (
    unit_df["Python_Achievement"] - (unit_df["Achievement"] * 100)
).abs()

unit_df["Variance_Difference_Corrected"] = (
    unit_df["Python_Variance_MU"] - unit_df["Variance_MU"]
).abs()

print("\n--- Corrected KPI Cross Validation ---")

print(
    "Maximum PLF Difference:",
    unit_df["PLF_Difference_Corrected"].max()
)

print(
    "Maximum Achievement Difference:",
    unit_df["Achievement_Difference_Corrected"].max()
)

print(
    "Maximum Variance Difference:",
    unit_df["Variance_Difference_Corrected"].max()
)
# ============================================================
# STEP 3.4 - STATION PROGRAM VS ACTUAL GENERATION TREND
# ============================================================

# Make sure Date is treated as a date
station_df["Date"] = pd.to_datetime(station_df["Date"])

# Sort data by date
station_df = station_df.sort_values("Date")

# Create chart
plt.figure(figsize=(12, 6))

plt.plot(
    station_df["Date"],
    station_df["Program_MU"],
    marker="o",
    label="Program Generation"
)

plt.plot(
    station_df["Date"],
    station_df["Actual_MU"],
    marker="o",
    label="Actual Generation"
)

plt.title("Kota TPS - Program vs Actual Generation (45 Days)")
plt.xlabel("Date")
plt.ylabel("Generation (MU)")

plt.xticks(rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Save chart in project folder
plt.savefig("station_generation_trend.png", dpi=300)

plt.show()
# ============================================================
# STEP 3.5 - UNIT-WISE PLF COMPARISON
# ============================================================

# Calculate PLF for the complete 45-day period for each unit
unit_plf = (
    unit_df.groupby(
        ["Unit", "Unit_Label", "Capacity_MW"],
        as_index=False
    )
    .agg(
        Total_Actual_MU=("Actual_MU", "sum"),
        Total_Days=("Date", "count")
    )
)

# Calculate 45-day PLF
unit_plf["PLF_Percent"] = (
    (unit_plf["Total_Actual_MU"] * 1000) /
    (unit_plf["Capacity_MW"] * unit_plf["Total_Days"] * 24)
) * 100

# Sort from highest PLF to lowest
unit_plf = unit_plf.sort_values(
    "PLF_Percent",
    ascending=False
)

print("\n--- Unit-wise 45-Day PLF ---")
print(
    unit_plf[
        ["Unit_Label", "Capacity_MW", "Total_Actual_MU", "PLF_Percent"]
    ].to_string(index=False)
)

# Create bar chart
plt.figure(figsize=(10, 6))

bars = plt.bar(
    unit_plf["Unit_Label"],
    unit_plf["PLF_Percent"]
)

# Add PLF value above each bar
for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f"{height:.2f}%",
        ha="center"
    )

plt.title("Kota TPS - Unit-wise PLF Comparison (45 Days)")
plt.xlabel("Generating Unit")
plt.ylabel("PLF (%)")

plt.ylim(0, 100)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "unit_wise_plf_comparison.png",
    dpi=300
)

plt.show()
# ============================================================
# STEP 3.4 - OUTAGE PARETO ANALYSIS
# ============================================================

print("\n--- Outage Pareto Analysis ---")

# Keep only rows where an outage category exists
outage_df = unit_df[
    unit_df["Outage_Category"].notna()
].copy()

# Total estimated generation loss by outage category
pareto_df = (
    outage_df.groupby("Outage_Category")["Est_Loss_MU"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Calculate cumulative percentage
total_loss = pareto_df["Est_Loss_MU"].sum()

pareto_df["Cumulative_Percent"] = (
    pareto_df["Est_Loss_MU"].cumsum()
    / total_loss
    * 100
)

print(pareto_df)

# Create Pareto chart
fig, ax1 = plt.subplots(figsize=(10, 6))

bars = ax1.bar(
    pareto_df["Outage_Category"],
    pareto_df["Est_Loss_MU"]
)

ax1.set_xlabel("Outage Category")
ax1.set_ylabel("Estimated Generation Loss (MU)")
ax1.set_title("Kota TPS - Outage Loss Pareto Analysis (45 Days)")
ax1.grid(axis="y", alpha=0.3)

# Second axis for cumulative percentage
ax2 = ax1.twinx()

ax2.plot(
    pareto_df["Outage_Category"],
    pareto_df["Cumulative_Percent"],
    marker="o"
)

ax2.set_ylabel("Cumulative Percentage (%)")
ax2.set_ylim(0, 110)

# 80% reference line
ax2.axhline(
    y=80,
    linestyle="--",
    alpha=0.7
)

plt.tight_layout()

# Save chart
plt.savefig(
    "outage_pareto_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# ============================================================
# STEP 3.5 - COAL STOCK TREND
# ============================================================

# Make sure Date is in datetime format
station_df["Date"] = pd.to_datetime(station_df["Date"])

# Sort data by date
coal_data = station_df.sort_values("Date")

# Create chart
plt.figure(figsize=(12, 6))

plt.plot(
    coal_data["Date"],
    coal_data["Coal_Stock_Days"],
    marker="o",
    linewidth=2
)

plt.title("Kota TPS - Coal Stock Trend (45 Days)")
plt.xlabel("Date")
plt.ylabel("Coal Stock (Days)")

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save chart
plt.savefig(
    "coal_stock_trend.png",
    dpi=300
)
plt.show()
# ============================================================
# STEP 3.6 - FINAL ANALYSIS SUMMARY
# ============================================================

print("\n========== KOTA TPS PYTHON ANALYSIS SUMMARY ==========")

# Station generation
print("\n1. STATION GENERATION")
print("Total Program Generation:",
      round(station_df["Program_MU"].sum(), 2), "MU")
print("Total Actual Generation:",
      round(station_df["Actual_MU"].sum(), 2), "MU")

print("Overall Generation Variance:",
      round(
          station_df["Actual_MU"].sum()
          - station_df["Program_MU"].sum(), 2
      ), "MU")

# Coal stock
print("\n2. COAL STOCK")
print("Minimum Coal Stock:",
      station_df["Coal_Stock_Days"].min(), "Days")
print("Maximum Coal Stock:",
      station_df["Coal_Stock_Days"].max(), "Days")

# Best and worst units
print("\n3. UNIT PERFORMANCE")

print("Highest PLF Unit:",
      unit_plf.iloc[0]["Unit_Label"],
      "-",
      round(unit_plf.iloc[0]["PLF_Percent"], 2), "%")

print("Lowest PLF Unit:",
      unit_plf.iloc[-1]["Unit_Label"],
      "-",
      round(unit_plf.iloc[-1]["PLF_Percent"], 2), "%")

# Outage loss
print("\n4. OUTAGE ANALYSIS")

print("Largest Estimated Loss Category:",
      pareto_df.iloc[0]["Outage_Category"])

print("Estimated Loss:",
      round(pareto_df.iloc[0]["Est_Loss_MU"], 2),
      "MU")

print("\n======================================================")
# ============================================================
# KEY FINDINGS
# ============================================================

# 1. Unit 6 recorded the highest 45-day PLF at approximately 82.35%.
# 2. Unit 1 recorded the lowest 45-day PLF at approximately 44.77%.
# 3. Turbine-related outages were the largest estimated source of
#    generation loss, contributing approximately 51.93 MU.
# 4. Coal stock declined to a minimum of 9 days before recovering
#    to a maximum of 16 days during the analysis period.
# 5. The analysis highlights significant differences in performance
#    across generating units and identifies outage-related losses
#    as an important area for performance improvement.