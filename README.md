
# Kota TPS – Generation, PLF, Outage & Coal Stock Analytics

## Project Overview

This project analyzes the operational performance of **Kota Super Thermal Power Station (Kota TPS), Rajasthan** using power-generation data for the period **06 June 2026 to 20 July 2026**.

The project focuses on generation performance, Plant Load Factor (PLF), unit-wise performance, outage patterns, estimated generation loss, and coal-stock trends.

The complete analytics workflow was developed using **Excel, SQL, Python, and Power BI**.

---

## Objectives

- Analyze daily and unit-wise power generation.
- Compare actual generation with programmed generation.
- Evaluate Plant Load Factor (PLF) across generating units.
- Analyze outage frequency and outage capacity.
- Identify units most affected by outages.
- Estimate generation loss associated with unit performance.
- Analyze coal-stock trends over the study period.
- Build an interactive Power BI dashboard for performance monitoring.

---

## Technology Stack

| Tool | Usage |
|---|---|
| Excel | Data cleaning, preparation and validation |
| SQL | Data preparation, querying and KPI analysis |
| Python | Data analysis and visualization |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Power BI | Interactive dashboard and KPI visualization |

---

## Dataset

The analysis covers **45 days**, from **06 June 2026 to 20 July 2026**.

Kota TPS consists of **7 generating units** with a total installed capacity of **1240 MW**:

- Unit 1 – 110 MW
- Unit 2 – 110 MW
- Unit 3 – 210 MW
- Unit 4 – 210 MW
- Unit 5 – 210 MW
- Unit 6 – 195 MW
- Unit 7 – 195 MW

The repository contains both the raw and cleaned datasets used during the project.

---

## Project Workflow

**1. Excel – Data Preparation**

Raw operational data was organized and cleaned to create analysis-ready station-level and unit-level datasets.

**2. SQL – Data Analysis**

SQL queries were used for data preparation, validation, aggregation and analysis of generation and operational KPIs.

**3. Python – Exploratory Data Analysis**

Python was used to analyze generation trends, PLF, coal stock and outage-related patterns using Pandas, NumPy and Matplotlib.

**4. Power BI – Interactive Dashboard**

A four-page Power BI dashboard was developed to present the final results interactively.

---

## Power BI Dashboard

The dashboard contains four analytical pages:

### 1. Plant Overview
Provides an overall view of plant generation, scheduled/program generation, PLF, coal stock and outage capacity.

### 2. Unit-Wise Performance Analysis
Compares the seven generating units using generation, PLF, variance and estimated generation-loss indicators.

### 3. Outage Analysis
Analyzes outage frequency, maximum unit outage capacity, affected units and outage categories.

### 4. Coal & Operational Trends
Shows coal-stock trends, daily coal-stock changes, generation trends and actual vs program generation.

> **Live Interactive Dashboard:** Link will be added after Power BI deployment.

---

## Key Dashboard Indicators

- Plant Capacity: **1240 MW**
- Total Generation: **916.97 MU**
- Program Generation: **817.25 MU**
- Average PLF: **68.47%**
- Total Outage Records: **35**
- Most Affected Unit: **Unit 4**
- Average Coal Stock: **12.31 Days**
- Minimum Coal Stock: **9 Days**
- Maximum Coal Stock: **16 Days**
- Average Daily Generation: **20.38 MU**

---

## Repository Structure

```text
Kota-TPS-Generation-Outage-Analytics/
│
├── DATA/
│   ├── Kota_TPS_Raw_Data.xlsx
│   ├── Kota_TPS_Cleaned_Workbook.xlsx
│   ├── station_daily.csv
│   └── unit_daily.csv
│
├── SQL/
│   ├── Kota_TPS_Data_Preparation.sql
│   └── Kota_TPS_Analysis.sql
│
├── PYTHON/
│   └── analysis.py
│
├── IMAGES/
│   ├── coal_stock_trend.png
│   ├── outage_pareto_analysis.png
│   ├── station_generation_trend.png
│   └── unit_wise_plf_comparison.png
│
├── POWERBI/
│   └── Kota_TPS_Dashboard.pbix
│
└── README.md

---

## Author

**Shelly Sharma**  

