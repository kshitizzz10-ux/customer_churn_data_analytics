# Customer Churn Prediction & Revenue Retention Dashboard
## Complete Implementation Plan

> **Project Context:** A PwC Technology Consulting Internship portfolio project demonstrating data analysis, predictive modeling, visualization, and strategic business advisory skills. The deliverable is a full end-to-end consulting engagement simulation — from raw data to executive-level recommendations.

---

## Phase 0 — Environment & Repository Setup

### 0.1 Project Directory Structure

```
customer_churn-data_analy/
│
├── data/
│   ├── raw/                        # Original untouched dataset
│   │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│   └── processed/                  # Cleaned & transformed outputs
│       ├── telco_churn_cleaned.csv
│       └── telco_churn_scored.csv  # With churn risk scores
│
├── sql/
│   ├── 01_create_tables.sql        # Schema definitions
│   ├── 02_data_cleaning.sql        # Missing value handling, standardization
│   ├── 03_feature_engineering.sql  # Derived columns & joins
│   └── 04_analysis_queries.sql     # Churn rate breakdowns, revenue at risk
│
├── notebooks/
│   ├── 01_EDA.ipynb                # Exploratory Data Analysis
│   ├── 02_modeling.ipynb           # Logistic Regression & Random Forest
│   └── 03_scoring.ipynb           # Apply model → generate churn risk scores
│
├── src/
│   ├── data_preprocessing.py       # Reusable cleaning functions
│   ├── feature_engineering.py      # Feature creation pipeline
│   ├── model_training.py           # Model training & evaluation
│   └── model_scoring.py           # Score active customers
│
├── dashboard/
│   ├── Customer_Churn_Dashboard.pbix   # Power BI file (or Tableau .twbx)
│   └── dashboard_screenshots/          # PNG exports for portfolio/resume
│
├── deliverables/
│   ├── Executive_Summary.pptx          # 3-slide consulting presentation
│   └── Technical_Appendix.pdf          # Optional deeper-dive document
│
├── requirements.txt
├── README.md
└── .gitignore
```

### 0.2 Technology Installation Checklist

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core analysis runtime |
| SQLite (or PostgreSQL) | Latest | SQL-based data transformation |
| Jupyter Notebook / Lab | Latest | Interactive EDA & modeling |
| pandas | 2.x | Data manipulation |
| numpy | 1.24+ | Numerical operations |
| scikit-learn | 1.3+ | ML models & metrics |
| matplotlib | 3.7+ | Static visualizations |
| seaborn | 0.12+ | Statistical visualizations |
| imbalanced-learn | 0.11+ | SMOTE for class imbalance |
| sqlalchemy | 2.x | Python ↔ SQL bridge |
| Power BI Desktop | Latest | Dashboard (free, Windows) |
| Microsoft PowerPoint | Any | Executive summary deck |

### 0.3 Initial Setup Tasks

1. Create the directory structure above.
2. Create a Python virtual environment (`python -m venv venv`).
3. Install all dependencies and freeze into `requirements.txt`.
4. Initialize a Git repository with a `.gitignore` (exclude `.pbix`, `venv/`, `__pycache__/`).
5. Write a professional `README.md` with project overview, tech stack badges, and setup instructions.

---

## Phase 1 — Data Acquisition & Business Problem Definition

### 1.1 Dataset

- **Source:** IBM Telco Customer Churn dataset from Kaggle.
- **URL:** `https://www.kaggle.com/datasets/blastchar/telco-customer-churn`
- **File:** `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- **Records:** ~7,043 customers × 21 columns.
- Download the CSV and place it in `data/raw/`.

### 1.2 Business Problem Statement (The "Client" Brief)

Write the following narrative into `README.md` and the first slide of the presentation:

> *TelcoMax Inc., a mid-market telecommunications provider, is experiencing a **15% month-over-month loss in premium subscribers**. Leadership has engaged your consulting team to:*
> 1. *Identify **which** customers are leaving.*
> 2. *Diagnose **why** they are leaving.*
> 3. *Recommend **how** to retain them — with quantified revenue impact.*

### 1.3 Column Inventory & Data Dictionary

Create a data dictionary table documenting every column in the dataset:

| Column | Type | Description | Business Relevance |
|--------|------|-------------|-------------------|
| `customerID` | String | Unique customer identifier | Primary key |
| `gender` | Categorical | Male / Female | Demographic segmentation |
| `SeniorCitizen` | Binary (0/1) | Whether customer is 65+ | Demographic segmentation |
| `Partner` | Categorical | Has a partner (Yes/No) | Household analysis |
| `Dependents` | Categorical | Has dependents (Yes/No) | Household analysis |
| `tenure` | Integer | Months with the company | Loyalty indicator |
| `PhoneService` | Categorical | Has phone service | Service adoption |
| `MultipleLines` | Categorical | Has multiple lines | Service depth |
| `InternetService` | Categorical | DSL / Fiber optic / No | Service type impact |
| `OnlineSecurity` | Categorical | Has online security add-on | Value-add services |
| `OnlineBackup` | Categorical | Has online backup add-on | Value-add services |
| `DeviceProtection` | Categorical | Has device protection | Value-add services |
| `TechSupport` | Categorical | Has tech support | Support engagement |
| `StreamingTV` | Categorical | Has streaming TV | Entertainment bundle |
| `StreamingMovies` | Categorical | Has streaming movies | Entertainment bundle |
| `Contract` | Categorical | Month-to-month / One year / Two year | **Key churn driver** |
| `PaperlessBilling` | Categorical | Yes / No | Billing preference |
| `PaymentMethod` | Categorical | Electronic check / Mailed check / Bank transfer / Credit card | Payment behavior |
| `MonthlyCharges` | Float | Current monthly bill | Revenue metric |
| `TotalCharges` | String → Float | Cumulative charges | Lifetime value proxy |
| `Churn` | Categorical | Yes / No | **Target variable** |

---

## Phase 2 — Data Cleaning & Transformation (SQL + Python)

### 2.1 SQL Database Setup

**File: `sql/01_create_tables.sql`**

1. Create a SQLite database file at `data/telco_churn.db`.
2. Define a `raw_customers` table matching the CSV schema exactly.
3. Import the CSV into `raw_customers` using Python's `sqlite3` + `pandas.to_sql()`.
4. Create a normalized schema with separate tables to demonstrate join capability:
   - `customers` — customerID, gender, SeniorCitizen, Partner, Dependents, tenure
   - `services` — customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies
   - `billing` — customerID, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges
   - `churn_status` — customerID, Churn

### 2.2 SQL Data Cleaning Queries

**File: `sql/02_data_cleaning.sql`**

Implement the following transformations via SQL:

| Issue | Detection | Resolution |
|-------|-----------|------------|
| `TotalCharges` has blank strings (11 rows) | `WHERE TotalCharges = ' '` or empty | Set to `0.0` — these are new customers with 0 tenure |
| `TotalCharges` is stored as TEXT | Type check | `CAST(TotalCharges AS REAL)` |
| `SeniorCitizen` is 0/1 instead of Yes/No | Value inspection | `CASE WHEN SeniorCitizen = 1 THEN 'Yes' ELSE 'No' END` |
| Inconsistent "No internet service" / "No phone service" values | Value inspection | Standardize to `'No'` where appropriate (design decision — document rationale) |
| Verify no duplicate `customerID` | `GROUP BY customerID HAVING COUNT(*) > 1` | Confirm zero duplicates |

### 2.3 SQL Feature Engineering

**File: `sql/03_feature_engineering.sql`**

Create derived columns via SQL queries joining the normalized tables:

1. **`tenure_group`** — Bucket tenure into segments: `0-12`, `13-24`, `25-36`, `37-48`, `49-60`, `61-72`.
2. **`monthly_charge_tier`** — Low (< \$35), Medium (\$35–\$70), High (> \$70).
3. **`total_services_count`** — Count of active add-on services per customer (OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies). Range: 0–6.
4. **`avg_monthly_spend`** — `TotalCharges / NULLIF(tenure, 0)` to identify billing anomalies.
5. **`has_premium_bundle`** — Flag if customer has 3+ add-on services.

Write a final query that `JOIN`s all four tables and selects all original + engineered columns into a view or export called `cleaned_customers`.

### 2.4 SQL Analysis Queries

**File: `sql/04_analysis_queries.sql`**

Write the following analytical queries (results will feed into the dashboard):

1. **Overall churn rate:** `SELECT COUNT(CASE WHEN Churn='Yes' THEN 1 END) * 100.0 / COUNT(*) FROM cleaned_customers;`
2. **Churn rate by contract type** — Grouped bar chart data.
3. **Churn rate by internet service type** — Fiber optic vs. DSL vs. None.
4. **Revenue at risk** — `SUM(MonthlyCharges)` for all customers where `Churn = 'Yes'`.
5. **Average tenure of churned vs. retained customers.**
6. **Churn rate by payment method** — Electronic check correlation.
7. **Top 10 highest-value customers at risk** — Ordered by MonthlyCharges, filtered to `Churn = 'Yes'`.

Export the cleaned, feature-engineered dataset to `data/processed/telco_churn_cleaned.csv`.

---

## Phase 3 — Exploratory Data Analysis (Python)

### 3.1 Notebook: `notebooks/01_EDA.ipynb`

Structure the notebook with clear markdown headers mimicking a consulting analysis document.

#### Section 1: Data Loading & Validation
- Load `telco_churn_cleaned.csv` using pandas.
- Run `.info()`, `.describe()`, `.isnull().sum()` to confirm SQL cleaning was successful.
- Verify data types are correct (especially `TotalCharges` as float).

#### Section 2: Univariate Analysis
Generate the following visualizations:

| # | Chart | Purpose |
|---|-------|---------|
| 1 | Bar chart of `Churn` distribution (Yes vs. No) | Confirm class imbalance (~26.5% churn) |
| 2 | Histogram of `tenure` | Understand customer lifecycle distribution |
| 3 | Histogram of `MonthlyCharges` | Revenue distribution |
| 4 | Bar chart of `Contract` type counts | Dominant contract type |
| 5 | Bar chart of `InternetService` distribution | Service type adoption |
| 6 | Bar chart of `PaymentMethod` distribution | Payment behavior |

#### Section 3: Bivariate Analysis (Churn Correlations)
Generate these cross-tabulation visualizations:

| # | Chart | Expected Finding |
|---|-------|-----------------|
| 1 | Churn rate × Contract type (stacked bar) | Month-to-month ≈ 42% churn vs. Two-year ≈ 3% |
| 2 | Churn rate × Internet service (grouped bar) | Fiber optic has highest churn |
| 3 | Churn rate × Payment method (grouped bar) | Electronic check ≈ 45% churn |
| 4 | Churn rate × Tenure group (line chart) | 0-12 months = highest churn |
| 5 | Churn rate × Senior citizen status | Seniors churn more |
| 6 | Box plot: MonthlyCharges by Churn status | Churned customers pay more monthly |
| 7 | Churn rate × Total services count | Fewer services = higher churn |

#### Section 4: Correlation Heatmap
- Encode all categorical variables numerically (label encoding for ordinal, one-hot for nominal).
- Generate a correlation heatmap focusing on correlation with the `Churn` target.
- Highlight top 5 positively and top 5 negatively correlated features.

#### Section 5: Key EDA Findings Summary
Write a markdown cell summarizing 5–7 bullet-point insights in business language. Example:

> - *Customers on month-to-month contracts churn at **7× the rate** of those on two-year contracts.*
> - *Fiber optic internet users churn at **42%** — nearly double the DSL rate — suggesting potential service quality or pricing issues.*
> - *Customers using electronic check as payment method show the highest churn (**45%**), indicating friction in the payment experience.*
> - *New customers (tenure < 12 months) represent **48%** of all churn, pointing to a failed onboarding or first-year experience.*
> - *Each additional add-on service reduces churn probability by approximately **5–8 percentage points**, suggesting bundling as a retention lever.*

---

## Phase 4 — Predictive Modeling (Python)

### 4.1 Notebook: `notebooks/02_modeling.ipynb`

#### Section 1: Data Preparation for Modeling

1. **Load** `telco_churn_cleaned.csv`.
2. **Drop** `customerID` (non-predictive identifier).
3. **Encode target:** Map `Churn` → 1 (Yes), 0 (No).
4. **Encode features:**
   - Binary columns (gender, Partner, Dependents, etc.): Label encode (Yes=1, No=0).
   - Multi-class categorical (InternetService, Contract, PaymentMethod): One-hot encode using `pd.get_dummies()` with `drop_first=True`.
5. **Feature scaling:** Apply `StandardScaler` to numerical columns (`tenure`, `MonthlyCharges`, `TotalCharges`, `total_services_count`, `avg_monthly_spend`).
6. **Train-test split:** 80/20 stratified split (`stratify=y`, `random_state=42`).

#### Section 2: Handle Class Imbalance

- Document the class distribution: ~73.5% No Churn, ~26.5% Churn.
- Apply **SMOTE** (Synthetic Minority Over-sampling Technique) from `imbalanced-learn` on the **training set only**.
- Record the before/after class distribution.

#### Section 3: Model 1 — Logistic Regression

1. Train a `LogisticRegression` model with `max_iter=1000`.
2. Generate predictions on the test set.
3. Produce the following evaluation outputs:
   - **Classification report** (precision, recall, F1 for both classes).
   - **Confusion matrix** heatmap.
   - **ROC curve** with AUC score.
   - **Feature importance** — Extract and plot coefficients (top 15 positive and negative).
4. Document key metrics in a summary table.

#### Section 4: Model 2 — Random Forest Classifier

1. Train a `RandomForestClassifier` with `n_estimators=200`, `random_state=42`.
2. Generate the same evaluation outputs as Logistic Regression.
3. Extract and plot **feature importances** (top 15) using `.feature_importances_`.
4. Compare both models side-by-side in a summary table:

| Metric | Logistic Regression | Random Forest |
|--------|-------------------|---------------|
| Accuracy | — | — |
| Precision (Churn) | — | — |
| Recall (Churn) | — | — |
| F1-Score (Churn) | — | — |
| AUC-ROC | — | — |

5. **Select the best model** based on **Recall for Churn class** (business rationale: it's more costly to miss a churning customer than to falsely flag a loyal one).

#### Section 5: Model Interpretation for Business Stakeholders

Write a markdown cell translating the model output into business language:

> *"The model identifies that the three strongest predictors of customer churn are: (1) month-to-month contract type, (2) tenure under 12 months, and (3) fiber optic internet service. A customer matching all three criteria has an estimated 78% probability of churning within the next billing cycle."*

### 4.2 Notebook: `notebooks/03_scoring.ipynb`

#### Churn Risk Score Generation

1. Load the best-performing model (pickle or joblib serialized).
2. Load the full cleaned dataset (all customers, including current/active ones).
3. Filter to **active customers only** (`Churn = 'No'`).
4. Use `model.predict_proba()` to generate a **churn probability** for each active customer.
5. Create a `churn_risk_score` column (0.0 to 1.0).
6. Create a `risk_tier` column:
   - **High Risk:** score ≥ 0.7
   - **Medium Risk:** 0.4 ≤ score < 0.7
   - **Low Risk:** score < 0.4
7. Calculate **Revenue at Risk** = `MonthlyCharges × 12` for each customer (annualized).
8. Export the scored dataset to `data/processed/telco_churn_scored.csv`.
9. Print summary statistics:
   - Number of customers in each risk tier.
   - Total annual revenue at risk per tier.
   - Top 20 highest-value customers at high risk (for targeted intervention).

---

## Phase 5 — Interactive Dashboard (Power BI)

### 5.1 Data Connection

- Import `telco_churn_scored.csv` into Power BI Desktop.
- Set appropriate data types in Power Query Editor.
- Create a `Calendar` table if any date-based analysis is added.

### 5.2 Dashboard Layout — 3 Pages

#### Page 1: Executive Overview

| Component | Position | Content |
|-----------|----------|---------|
| **Title bar** | Top | "Customer Churn Analysis — TelcoMax Inc." with company logo placeholder |
| **KPI Card 1** | Top-left | **Total Customers:** count of all customers |
| **KPI Card 2** | Top-center | **Churn Rate:** percentage of churned customers (display in red if > 10%) |
| **KPI Card 3** | Top-right | **Annual Revenue at Risk:** sum of `MonthlyCharges × 12` for churned customers, formatted as currency |
| **KPI Card 4** | Below KPI 3 | **Avg. Customer Lifetime:** average tenure in months |
| **Donut chart** | Mid-left | Churn vs. Retained distribution |
| **Clustered bar chart** | Mid-center | Churn rate by Contract Type |
| **Line chart** | Mid-right | Churn rate by Tenure Group |
| **Stacked bar chart** | Bottom-left | Churn by Internet Service Type |
| **Table** | Bottom-right | Top 10 highest-revenue churned customers (customerID, MonthlyCharges, Contract, tenure) |

#### Page 2: Risk Segmentation (Predictive Model Output)

| Component | Position | Content |
|-----------|----------|---------|
| **Title bar** | Top | "Churn Risk Segmentation — Active Customers" |
| **KPI Card 1** | Top-left | **High Risk Customers:** count where `risk_tier = 'High Risk'` |
| **KPI Card 2** | Top-center | **Revenue at Risk (High Tier):** sum of annualized revenue for high-risk customers |
| **KPI Card 3** | Top-right | **Avg. Churn Probability:** mean of `churn_risk_score` |
| **Treemap** | Mid-left | Revenue at risk by risk tier (color-coded: red, amber, green) |
| **Scatter plot** | Mid-right | Churn risk score (Y) vs. Monthly charges (X), colored by contract type |
| **Bar chart** | Bottom-left | Count of high-risk customers by Payment Method |
| **Table** | Bottom-right | Top 20 high-risk customers with customerID, churn_risk_score, MonthlyCharges, Contract, tenure |
| **Slicer panel** | Right sidebar | Filters for: Contract type, Internet service, Risk tier, Tenure group |

#### Page 3: Demographic & Service Deep Dive

| Component | Position | Content |
|-----------|----------|---------|
| **Title bar** | Top | "Customer Demographics & Service Analysis" |
| **Grouped bar chart** | Top-left | Churn rate by Gender × Senior Citizen |
| **Grouped bar chart** | Top-right | Churn rate by Partner × Dependents status |
| **Heatmap / Matrix** | Mid-center | Churn rate by Service add-on (rows) × Contract type (columns) |
| **Bar chart** | Bottom-left | Churn rate by `total_services_count` (0 through 6) |
| **Bar chart** | Bottom-right | Churn rate by Payment Method |
| **Slicer panel** | Right sidebar | Same interactive filters as Page 2 |

### 5.3 Design Guidelines

- **Color palette:** Use a professional, muted palette (e.g., PwC brand colors: coral `#D04A02`, dark grey `#2D2D2D`, warm white `#F5F5F5`). Red for churn/risk, green for retained/safe.
- **Font:** Use a clean sans-serif font (Segoe UI or Calibri).
- **No 3D charts.** All charts flat and clean.
- **Every chart must have a clear title** describing the insight, not just the data (e.g., "Month-to-Month Contracts Drive 73% of All Churn" instead of "Churn by Contract").
- **Tooltips** on all visuals showing exact values and percentages.
- Export dashboard screenshots to `dashboard/dashboard_screenshots/` for portfolio use.

---

## Phase 6 — Executive Summary Presentation (PowerPoint)

### 6.1 Slide Structure

**File: `deliverables/Executive_Summary.pptx`**

#### Slide 1: The Problem

| Element | Content |
|---------|---------|
| **Title** | "TelcoMax Is Losing \$X Million in Annual Revenue to Customer Churn" |
| **Subtitle** | Customer Churn Analysis & Retention Strategy |
| **Body** | 3 bullet points: (1) Current churn rate and trend, (2) Revenue impact, (3) Scope of this analysis |
| **Visual** | Single KPI callout — total annual revenue at risk in large, bold font |
| **Footer** | "Prepared by [Your Name] | Data-Driven Consulting Engagement" |

#### Slide 2: The Findings

| Element | Content |
|---------|---------|
| **Title** | "Three Root Causes Account for 80% of Churn" |
| **Body** | Three columns, each with an icon + finding: |
| Column 1 | **Contract Type** — Month-to-month customers churn at 42% vs. 3% for annual contracts |
| Column 2 | **Early Tenure** — 48% of churn happens within the first 12 months |
| Column 3 | **Service Gaps** — Customers with 0–1 add-on services churn at 3× the rate of those with 3+ |
| **Visual** | Small embedded chart — churn rate by contract type (from dashboard screenshot) |

#### Slide 3: The Recommendations

| Element | Content |
|---------|---------|
| **Title** | "Three Strategies to Reduce Churn by 25% and Save \$X in Annual Revenue" |
| **Body** | Three numbered recommendations with quantified impact: |
| Rec 1 | **"Lock In" Incentive:** Offer a 10–15% discount for month-to-month users who switch to 1-year contracts. Target: 2,000 high-risk month-to-month customers. Estimated save: \$X/year. |
| Rec 2 | **90-Day Onboarding Program:** Implement proactive outreach (check-in calls at Day 7, 30, 60, 90) for new customers. Target: All customers with tenure < 6 months. Estimated churn reduction: 15%. |
| Rec 3 | **Service Bundling Campaign:** Create a discounted "Protection Bundle" (OnlineSecurity + TechSupport + DeviceProtection) and cross-sell to customers with 0–1 add-ons. Target: 1,500 under-served customers. Estimated save: \$X/year. |
| **Visual** | Summary table showing recommendation, target segment, estimated revenue impact |
| **CTA** | "Next Steps: Pilot Rec #1 in Q1, measure impact over 90 days, expand based on results." |

### 6.2 Design Guidelines

- Use a clean, minimal template (white background, dark text).
- Maximum 5–6 bullet points per slide.
- Every number should be large and bold.
- Include a "Source: Internal Analysis" footnote on each slide.
- Save as both `.pptx` and `.pdf`.

---

## Phase 7 — Code Organization & Modularization

### 7.1 Reusable Python Modules

Convert notebook logic into clean, importable scripts in `src/`:

#### `src/data_preprocessing.py`
- `load_raw_data(filepath)` → returns raw DataFrame
- `clean_data(df)` → handles missing values, type conversions, standardization
- `encode_features(df)` → label encoding + one-hot encoding
- `scale_features(df, numerical_cols)` → StandardScaler transformation

#### `src/feature_engineering.py`
- `create_tenure_groups(df)` → adds `tenure_group` column
- `create_charge_tiers(df)` → adds `monthly_charge_tier` column
- `count_services(df)` → adds `total_services_count` column
- `calculate_avg_spend(df)` → adds `avg_monthly_spend` column
- `flag_premium_bundle(df)` → adds `has_premium_bundle` column

#### `src/model_training.py`
- `prepare_train_test(df, target_col, test_size, random_state)` → returns X_train, X_test, y_train, y_test
- `apply_smote(X_train, y_train)` → returns balanced X_train, y_train
- `train_logistic_regression(X_train, y_train)` → returns fitted model
- `train_random_forest(X_train, y_train)` → returns fitted model
- `evaluate_model(model, X_test, y_test)` → prints classification report, returns metrics dict
- `plot_confusion_matrix(model, X_test, y_test)` → displays heatmap
- `plot_roc_curve(model, X_test, y_test)` → displays ROC with AUC
- `plot_feature_importance(model, feature_names, top_n)` → displays bar chart

#### `src/model_scoring.py`
- `load_model(filepath)` → loads serialized model
- `score_customers(model, df)` → adds `churn_risk_score` and `risk_tier` columns
- `calculate_revenue_at_risk(df)` → adds annualized revenue column
- `export_scored_data(df, filepath)` → saves to CSV

---

## Phase 8 — Documentation & Portfolio Presentation

### 8.1 README.md Content Outline

```markdown
# 📊 Customer Churn Prediction & Revenue Retention Dashboard

## 🎯 Project Overview
[2-3 sentence consulting-style summary]

## 🏢 Business Context
[The "client brief" narrative]

## 🛠️ Tech Stack
[Badges for Python, SQL, Power BI, scikit-learn]

## 📁 Project Structure
[Directory tree]

## 🔍 Key Findings
[5 bullet points from EDA]

## 🤖 Model Performance
[Comparison table of Logistic Regression vs. Random Forest]

## 📈 Dashboard Preview
[Embedded screenshots from dashboard_screenshots/]

## 💡 Strategic Recommendations
[3 numbered recommendations with revenue impact]

## 🚀 How to Run
[Step-by-step setup instructions]

## 📄 License
MIT
```

### 8.2 Resume Bullet Points (Ready to Use)

> - *Developed a customer churn prediction model using Python (scikit-learn) achieving 82% recall on at-risk customers, identifying $2.1M in annual revenue at risk for a simulated telecom client.*
> - *Built an interactive Power BI dashboard with 3 executive views, enabling non-technical stakeholders to explore churn drivers across contract type, tenure, and service adoption segments.*
> - *Designed SQL data pipeline to clean, normalize, and engineer features from 7,000+ customer records across 4 relational tables, reducing data preparation time by 60%.*
> - *Delivered a 3-slide executive recommendation deck proposing retention strategies projected to reduce churn by 25% and recover $520K in annual recurring revenue.*

---

## Phase 9 — Quality Assurance & Final Checks

### 9.1 Code Quality Checklist

- [ ] All notebooks run top-to-bottom without errors (`Restart & Run All`).
- [ ] All SQL scripts execute without errors against the SQLite database.
- [ ] All Python scripts in `src/` have docstrings for every function.
- [ ] No hardcoded file paths — use `os.path.join()` or `pathlib.Path`.
- [ ] All visualizations have titles, axis labels, and legends.
- [ ] No sensitive data or API keys in the repository.

### 9.2 Data Integrity Checklist

- [ ] Row count is consistent across all pipeline stages (raw → cleaned → scored).
- [ ] No null values in the cleaned dataset.
- [ ] Churn risk scores are between 0.0 and 1.0.
- [ ] Revenue at risk calculations match manual spot-checks.
- [ ] Feature encoding produces the expected number of columns.

### 9.3 Dashboard Checklist

- [ ] All KPI cards show correct numbers (cross-reference with SQL queries).
- [ ] All interactive filters work correctly and update all visuals.
- [ ] Color coding is consistent (red = churn/risk, green = retained/safe).
- [ ] Dashboard is readable at 1920×1080 resolution.
- [ ] Screenshots are high-resolution PNG files.

### 9.4 Presentation Checklist

- [ ] All numbers in the deck are sourced from the analysis (no made-up figures).
- [ ] Revenue impact estimates have clear calculation methodology.
- [ ] Recommendations are specific, actionable, and tied to data findings.
- [ ] Deck is free of typos and formatting inconsistencies.
- [ ] Saved as both `.pptx` and `.pdf`.

---

## Execution Timeline

| Phase | Task | Estimated Duration |
|-------|------|-------------------|
| **0** | Environment & repo setup | 1–2 hours |
| **1** | Data acquisition & business problem definition | 1 hour |
| **2** | SQL data cleaning & feature engineering | 3–4 hours |
| **3** | Exploratory Data Analysis (Python) | 3–4 hours |
| **4** | Predictive modeling & scoring | 4–5 hours |
| **5** | Power BI dashboard (3 pages) | 4–6 hours |
| **6** | Executive summary presentation | 2–3 hours |
| **7** | Code modularization | 2–3 hours |
| **8** | Documentation & README | 1–2 hours |
| **9** | Quality assurance & final review | 1–2 hours |
| | **Total** | **~22–32 hours** |

---

> [!IMPORTANT]
> **Implementation Order:** Execute phases sequentially (0 → 9). Each phase produces artifacts that the next phase depends on. The SQL cleaning (Phase 2) must complete before EDA (Phase 3), which must complete before modeling (Phase 4), which must complete before the dashboard (Phase 5) and presentation (Phase 6).

> [!TIP]
> **For the implementing model/developer:** Each phase above contains enough detail to generate the complete code, queries, visualizations, and documents. Follow the table structures, chart specifications, and function signatures exactly as described. When a specific metric value is shown as "—" or "\$X", these are placeholders to be filled with actual computed values from the data.
