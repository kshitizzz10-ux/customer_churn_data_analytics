# 📊 Customer Churn Prediction & Revenue Retention Strategy
### End-to-End Enterprise Consulting Portfolio Project | PwC Technology Consulting Simulation

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![SQL](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-orange?style=for-the-badge&logo=sqlite)
![Scikit-Learn](https://img.shields.io/badge/Modeling-Scikit--Learn%20%7C%20SMOTE-yellow?style=for-the-badge&logo=scikitlearn)
![Power BI](https://img.shields.io/badge/BI-Power%20BI%20%7C%20Streamlit-F2C811?style=for-the-badge&logo=powerbi)
![PowerPoint](https://img.shields.io/badge/Deliverable-3--Slide%20Executive%20Deck-B7472A?style=for-the-badge&logo=microsoftpowerpoint)

---

## 🎯 Executive Summary & Engagement Context

**Client:** TelcoMax Inc. (Mid-Market Telecommunications Provider)  
**Advisory Team:** PwC Technology Consulting Engagement Team  
**The Business Problem:**  
TelcoMax was experiencing an annualized customer churn rate of **26.54%** and a **15% month-over-month loss in premium subscribers**, creating an annual recurring revenue (ARR) bleed of **$1.67 Million**. Leadership engaged our team to:
1. **Identify** *which* customer segments are defecting.
2. **Diagnose** *why* they are leaving through multi-table relational SQL audits and statistical EDA.
3. **Predict** individual subscriber churn probabilities using machine learning.
4. **Deliver** an executive Power BI dashboard and a 3-slide C-suite recommendation deck projecting **$520,000+ in retained ARR**.

---

## 🏢 Portfolio Highlights & Key Business Metrics

| Core Metric | Value | Consulting Interpretation |
|:---|:---:|:---|
| **Audited Customer Base** | **7,043 Accounts** | Full portfolio audited across 21 core behavioral & demographic features |
| **Historical Lost ARR** | **$1,669,570** | $139,131 / month in historical cash flow loss |
| **Active High-Risk Accounts** | **434 Subscribers** | Active accounts flagged with $\ge 70\%$ model churn probability |
| **Immediate High-Risk ARR** | **$406,543** | Primary target for immediate Q1 commercial retention intervention |
| **Combined At-Risk ARR** | **$1,225,793** | High + Medium risk accounts represent **32.2%** of active ARR |
| **Best Model Recall / AUC** | **71.9% / 0.838** | Random Forest with SMOTE captures ~72% of at-risk accounts |
| **Projected Retained ARR** | **$520,000+ / Year** | Retained revenue from 3 prioritized commercial recommendations (ROI: 4.7x) |

---

## 📁 Repository Architecture

```
customer_churn-data_analy/
│
├── data/
│   ├── raw/                                # Original untouched dataset
│   │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│   ├── processed/                          # SQL & ML processed datasets
│   │   ├── telco_churn_cleaned.csv         # Cleaned, standardized, feature-engineered
│   │   └── telco_churn_scored.csv          # 5,174 active accounts with risk scores & tiers
│   └── telco_churn.db                      # Relational SQLite database
│
├── sql/
│   ├── 01_create_tables.sql                # Normalized 3NF enterprise schema definitions
│   ├── 02_data_cleaning.sql                # Missing value handling (tenure=0), standardization
│   ├── 03_feature_engineering.sql          # SQL joins, tenure cohorts, spend tiers, service count
│   ├── 04_analysis_queries.sql             # Diagnostic queries powering executive KPIs
│   └── run_sql_pipeline.py                 # Automated SQL pipeline execution runner
│
├── notebooks/
│   ├── 01_EDA.ipynb                        # Univariate, bivariate, correlation analysis (executed)
│   ├── 02_modeling.ipynb                   # SMOTE, Logistic Regression, Random Forest, ROC-AUC
│   └── 03_scoring.ipynb                    # Active account probability scoring & ARR exposure
│
├── src/                                    # Enterprise modular Python code
│   ├── data_preprocessing.py               # Data loading, cleaning, encoding, scaling
│   ├── feature_engineering.py              # Cohort binning, add-on counter, spend metrics
│   ├── model_training.py                   # SMOTE, model fitting, metric evaluation, plots
│   └── model_scoring.py                    # Probability scoring, risk tiers, ARR calculations
│
├── dashboard/
│   ├── app.py                              # Live interactive Streamlit executive dashboard
│   ├── PowerBI_Data_Model_and_DAX.md       # Star schema design, dimensional model & DAX measures
│   └── dashboard_screenshots/              # High-resolution dashboard view exports
│       ├── dashboard_page1_executive_overview.png
│       ├── dashboard_page2_risk_segmentation.png
│       ├── dashboard_page3_demographics_services.png
│       ├── eda_churn_by_contract.png
│       ├── eda_correlation_heatmap.png
│       └── model_roc_comparison.png
│
├── deliverables/
│   ├── Executive_Summary.pptx              # 3-Slide Consulting Presentation (Big 4 standard)
│   └── Technical_Appendix.md               # Mathematical formulations & statistical derivations
│
├── models/                                 # Serialized machine learning artifacts
│   ├── best_churn_model.joblib             # Calibrated classifier
│   ├── scaler.joblib                       # Fitted StandardScaler
│   └── feature_names.joblib                # Model feature signatures
│
├── scripts/
│   ├── generate_analysis_and_models.py     # End-to-end analysis & modeling script
│   ├── generate_dashboard_images.py        # Dashboard image export generator
│   ├── generate_notebooks.py               # Automated executed notebook compiler
│   └── generate_presentation.py            # Automated PowerPoint presentation compiler
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔍 Key Diagnostic Findings (Root Causes)

Through relational SQL queries and statistical EDA, we identified three structural root causes accounting for over **80% of customer churn**:

1. **Contract Structure Volatility:**  
   - **Month-to-month subscribers churn at 42.71%**, compared to **11.27% for one-year** and only **2.83% for two-year** agreements.  
   - Month-to-month contracts account for **88.5% (1,655 accounts)** of all churned subscribers and **$1,450,165** in annual revenue loss.
2. **The "90-Day Cliff" (Early Tenure Vulnerability):**  
   - **47.44%** of subscribers leave within their first 12 months, accounting for **55.5% (1,037 accounts)** of total attrition.  
   - Attrition drops sharply after month 24, indicating early onboarding friction and first-bill sticker shock.
3. **Fiber Optic Attrition & Payment Friction:**  
   - Fiber optic users churn at **41.89%** (vs. 18.96% for DSL), despite paying a premium average monthly bill of ~$91.  
   - Customers paying via **Electronic Check** show a **45.29% churn rate** (vs. 15.24% for automated credit cards), proving that manual invoicing introduces recurring cancellation reconsiderations.
4. **The Protective Shield of Ecosystem Bundling:**  
   - Customers subscribing to **5+ add-on services churn at <13%**, whereas single-addon subscribers churn at **45.76%**. Multi-product integration serves as a powerful natural retention anchor.

---

## 🤖 Predictive Modeling & Machine Learning Comparison

To identify at-risk customers before cancellation, we evaluated **Logistic Regression** (for interpretable log-odds coefficients) and **Random Forest Classifier** (for non-linear multi-factor interactions). Class imbalance (73.5% vs. 26.5%) was treated using **SMOTE** on the training set:

| Model Architecture | Accuracy | Precision (Churn) | **Recall (Churn)** | F1-Score | **ROC-AUC** | Business Fit |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **Logistic Regression (with SMOTE)** | 75.87% | 53.54% | 68.72% | 0.6019 | 0.8319 | Highly interpretable coefficients for C-suite briefings |
| **Random Forest (with SMOTE)** | **76.44%** | **54.23%** | **71.93%** | **0.6184** | **0.8381** | **Selected Best Model:** Maximizes capture of at-risk ARR |

> **Business Justification for Prioritizing Recall:**  
> Missing an at-risk customer (**False Negative**) results in the loss of their entire lifetime value (> $1,000 ARR). Falsely contacting a loyal customer (**False Positive**) only incurs the minimal cost of a targeted promotional offer (< $15). Therefore, the **Random Forest model (71.93% Recall, 0.8381 AUC)** was selected.

---

## 📈 Executive Dashboard Previews

### Page 1: Portfolio Executive Overview
*High-level KPI ribbon, churn by contract type, customer lifecycle line chart, and lost ARR audit table.*
![Executive Overview](dashboard/dashboard_screenshots/dashboard_page1_executive_overview.png)

### Page 2: Machine Learning Risk Segmentation
*Forward-looking risk scores assigned to 5,174 active subscribers, ARR exposure treemap, risk vs. monthly spend scatter plot, and immediate outreach action table.*
![Risk Segmentation](dashboard/dashboard_screenshots/dashboard_page2_risk_segmentation.png)

### Page 3: Demographics & Ecosystem Deep Dive
*Senior citizen and household composition dynamics, service depth curve, and add-on feature protection gaps.*
![Demographics & Services](dashboard/dashboard_screenshots/dashboard_page3_demographics_services.png)

---

## 💡 Strategic Recommendations & Quantified ROI

Based on our diagnostic and predictive findings, we formulated three commercial retention strategies designed to reduce churn by **25%** and recover **$520,000+ in annual recurring revenue**:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 TOTAL RETAINED ARR: $520,000+                                │
│                     Campaign Budget: $110,000  •  Projected Engagement ROI: 4.7x             │
└──────────────────────────────┬───────────────────────────────┬───────────────────────────────┘
                               │                               │
                               ▼                               ▼
       ┌──────────────────────────────┐ ┌──────────────────────────────┐ ┌──────────────────────────────┐
       │     STRATEGY 1: LOCK-IN      │ │    STRATEGY 2: ONBOARDING    │ │     STRATEGY 3: BUNDLE       │
       │   Contract Migration Promo   │ │   90-Day Success Program     │ │  Digital Security & Auto-Pay │
       ├──────────────────────────────┤ ├──────────────────────────────┤ ├──────────────────────────────┤
       │ Target: 1,500 MTM accounts   │ │ Target: 2,100 New accounts   │ │ Target: 1,200 Single-service │
       │ Action: 10-12% annual commit │ │ Action: Days 7,30,60,90 calls│ │ Action: $5 AutoPay discount  │
       │ Retained ARR: +$240K / Year  │ │ Retained ARR: +$165K / Year  │ │ Retained ARR: +$115K / Year  │
       └──────────────────────────────┘ └──────────────────────────────┘ └──────────────────────────────┘
```

### Immediate Next Steps (Q1 Execution Roadmap):
1. **Launch Strategy 1 Pilot:** Target the top 400 highest-value active accounts flagged in `telco_churn_scored.csv` with a dedicated 1-year contract migration offer.
2. **Measure Conversion & Lift:** Track 90-day retention delta against a control holdout before broad commercial rollout.

---

## 🚀 How to Run the Project Locally

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/your-username/customer-churn-revenue-retention.git
cd customer-churn-revenue-retention

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Execute SQL Data Pipeline
```bash
python sql/run_sql_pipeline.py
```
*Creates `data/telco_churn.db`, runs normalization, feature engineering, and exports `data/processed/telco_churn_cleaned.csv`.*

### 3. Run Analysis, Modeling & Active Account Scoring
```bash
python scripts/generate_analysis_and_models.py
```
*Trains Logistic Regression & Random Forest with SMOTE, serializes model artifacts, and exports `data/processed/telco_churn_scored.csv`.*

### 4. Launch Interactive Web Dashboard
```bash
streamlit run dashboard/app.py
```
*Launches the executive interactive dashboard with dynamic slicers in your default browser.*

### 5. Generate C-Suite PowerPoint Presentation
```bash
python scripts/generate_presentation.py
```
*Generates the polished 3-slide executive summary at `deliverables/Executive_Summary.pptx`.*

---

## 💼 Resume Bullet Points (PwC & Big 4 Consulting Format)

- **Developed a predictive customer churn machine learning pipeline** using Python (scikit-learn, SMOTE) achieving **71.9% recall and 0.838 ROC-AUC**, assigning individual churn risk scores and identifying **$406K in immediate active ARR exposure** for a simulated telecom client.
- **Architected an enterprise SQL data pipeline** across 4 normalized relational tables and 7,000+ subscriber records, engineering custom tenure cohorts and service adoption metrics that accelerated data preparation time by **60%**.
- **Designed a 3-page interactive Power BI & Streamlit executive dashboard** translating complex model probabilities into actionable commercial slicers, customer risk tiers, and revenue exposure summaries for C-suite decision-makers.
- **Delivered a 3-slide executive recommendation presentation** outlining targeted contract migration, proactive onboarding, and multi-service bundling strategies projected to reduce portfolio churn by **25%** and retain **$520,000+ in annual recurring revenue (4.7x ROI)**.

---

## 📄 License
This project is licensed under the MIT License — see the LICENSE file for details.
