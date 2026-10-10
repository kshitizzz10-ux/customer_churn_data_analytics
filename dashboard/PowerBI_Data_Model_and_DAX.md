# Power BI Data Model Architecture & DAX Measures Reference
## Client: TelcoMax Inc. | PwC Technology Consulting Engagement

This document details the exact semantic data model, table relationships, Power Query M-transformations, and certified DAX measures implemented in Power BI Desktop for the Customer Churn & Revenue Retention Solution.

---

## 1. Data Model Architecture (Star Schema)

The reporting data model follows an enterprise dimensional structure optimized for analytical drilldowns and cross-filtering:

```
                      ┌──────────────────────┐
                      │   d_Calendar / Date  │
                      └──────────┬───────────┘
                                 │ 1
                                 │
                                 │ *
┌─────────────────────┐       ┌──┴───────────────────┐       ┌──────────────────────┐
│  d_CustomerProfile  │ 1   * │  f_CustomerScoring   │ *   1 │   d_ContractBilling  │
│  (Demographics)     ├───────┤  (Central Fact)      ├───────┤   (Terms & Payment)  │
└─────────────────────┘       └──┬───────────────────┘       └──────────────────────┘
                                 │ *
                                 │
                                 │ 1
                      ┌──────────┴───────────┐
                      │   d_ServicesCatalog  │
                      │   (Add-ons & Fiber)  │
                      └──────────────────────┘
```

### Table Definitions & Primary Keys
1. **`f_CustomerScoring` (Central Fact Table)**
   - **Source:** `data/processed/telco_churn_scored.csv` (or `telco_churn_cleaned.csv`)
   - **Grain:** One row per customer subscription account
   - **Primary Key:** `customerID`
   - **Attributes:** `tenure`, `MonthlyCharges`, `TotalCharges`, `annualized_revenue`, `churn_risk_score`, `risk_tier`, `Churn`
2. **`d_CustomerProfile` (Dimension)**
   - `customerID` (PK), `gender`, `SeniorCitizen`, `Partner`, `Dependents`, `tenure_group`
3. **`d_ContractBilling` (Dimension)**
   - `customerID` (PK), `Contract`, `PaperlessBilling`, `PaymentMethod`, `monthly_charge_tier`
4. **`d_ServicesCatalog` (Dimension)**
   - `customerID` (PK), `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `total_services_count`, `has_premium_bundle`

---

## 2. Certified DAX Measures Catalog

Create a dedicated calculation table in Power BI named `_Measures` and insert the following certified DAX expressions:

### 2.1 Core Portfolio KPIs
```dax
// 1. Total Customer Portfolio
Total Customers = 
COUNTROWS(f_CustomerScoring)

// 2. Churned Customers Count
Churned Customers = 
CALCULATE(
    COUNTROWS(f_CustomerScoring),
    f_CustomerScoring[Churn] = "Yes"
)

// 3. Retained Customers Count
Retained Customers = 
CALCULATE(
    COUNTROWS(f_CustomerScoring),
    f_CustomerScoring[Churn] = "No"
)

// 4. Portfolio Churn Rate (%)
Churn Rate % = 
DIVIDE([Churned Customers], [Total Customers], 0)

// 5. Total Monthly Portfolio Recurring Revenue (MRR)
Total MRR = 
SUM(f_CustomerScoring[MonthlyCharges])

// 6. Annualized Recurring Revenue (ARR)
Total ARR = 
SUM(f_CustomerScoring[annualized_revenue])

// 7. Annualized Revenue Lost to Historical Churn
ARR Lost to Churn = 
CALCULATE(
    SUM(f_CustomerScoring[annualized_revenue]),
    f_CustomerScoring[Churn] = "Yes"
)

// 8. Average Customer Lifespan (Months)
Avg Customer Tenure = 
AVERAGE(f_CustomerScoring[tenure])
```

### 2.2 Forward Predictive Risk Exposure Measures
```dax
// 9. Active High-Risk Customers Count
High Risk Customers Count = 
CALCULATE(
    COUNTROWS(f_CustomerScoring),
    f_CustomerScoring[risk_tier] = "High Risk"
)

// 10. Forward ARR at Risk (High Risk Tier Only)
High Risk ARR Exposure = 
CALCULATE(
    SUM(f_CustomerScoring[annualized_revenue]),
    f_CustomerScoring[risk_tier] = "High Risk"
)

// 11. Forward ARR at Risk (Combined High + Medium Risk)
Total ARR at Immediate Risk = 
CALCULATE(
    SUM(f_CustomerScoring[annualized_revenue]),
    f_CustomerScoring[risk_tier] IN {"High Risk", "Medium Risk"}
)

// 12. Portfolio Average Churn Risk Score
Avg Churn Risk Probability = 
AVERAGE(f_CustomerScoring[churn_risk_score])

// 13. Dynamic Churn Rate Color Alert (For KPI Visual Formatting)
Churn KPI Alert Color = 
IF([Churn Rate %] > 0.20, "#D04A02", "#16A34A")
```

---

## 3. Visual Layout Specification (3 Executive Pages)

### Page 1: Executive Portfolio Overview
- **Header:** TelcoMax Inc. Executive Portfolio View (PwC Consulting Palette: `#1E293B`, Coral `#D04A02`)
- **Top Ribbon Cards:**
  - `[Total Customers]` = `7,043`
  - `[Churn Rate %]` = `26.54%` (Red callout)
  - `[ARR Lost to Churn]` = `$1,669,570`
  - `[Avg Customer Tenure]` = `32.4 Mos`
- **Visuals:**
  - Donut Chart: `Churn` status split (`Retained` 73.5% vs `Churned` 26.5%)
  - Clustered Bar: `[Churn Rate %]` by `Contract` (`Month-to-month` = 42.7%, `One year` = 11.3%, `Two year` = 2.8%)
  - Line Chart: `[Churn Rate %]` across `tenure_group` (`0-12m` = 47.4% down to `61-72m` = 6.6%)
  - Stacked Bar: `[Total Customers]` by `InternetService` with `Churn` legend
  - Top 10 Table: Highest-revenue lost subscribers

### Page 2: Predictive Risk Segmentation
- **Top Ribbon Cards:**
  - `[High Risk Customers Count]` = `434` accounts
  - `[High Risk ARR Exposure]` = `$406,543`
  - `[Total ARR at Immediate Risk]` = `$1,225,793`
  - `[Avg Churn Risk Probability]` = `80.3%` (High Tier)
- **Visuals:**
  - Horizontal Bar / Treemap: ARR by `risk_tier` (`High Risk` $406.5K, `Medium Risk` $819.3K, `Low Risk` $2.58M)
  - Scatter Plot: X = `MonthlyCharges`, Y = `churn_risk_score`, Legend = `Contract`
  - Bar Chart: Count of High-Risk Accounts by `PaymentMethod` (Electronic Check = 328 accounts)
  - Priority Action Table: Top 20 active accounts sorted by `MonthlyCharges` for immediate retention intervention

### Page 3: Demographics & Ecosystem Deep Dive
- **Visuals:**
  - Grouped Bar: Churn by `SeniorCitizen` x `gender`
  - Grouped Bar: Churn by `Partner` x `Dependents`
  - Matrix Heatmap: Churn across all 6 Add-on Services (`OnlineSecurity`, `TechSupport`, `DeviceProtection`, etc.)
  - Step Bar: Churn by `total_services_count` (0 through 6)
  - Slicer Panel: Interactive filters for `Contract`, `InternetService`, `risk_tier`, `tenure_group`
