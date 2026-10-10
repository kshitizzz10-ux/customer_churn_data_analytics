# Technical Methodology & Analytical Appendix
## Client: TelcoMax Inc. | PwC Technology Consulting Engagement

This technical appendix provides mathematical specifications, data pipeline architecture, machine learning tuning details, and full statistical derivations supporting the **Customer Churn Prediction and Revenue Retention Dashboard**.

---

## 1. Enterprise SQL Pipeline & Normalization Architecture

The initial transformation ingested 7,043 raw customer records from `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` into a SQLite database (`data/telco_churn.db`). To demonstrate enterprise relational database best practices, the schema was normalized into third normal form (3NF) across four logical entities:

1. **`customers`** (Account Lifespan & Demographics):
   $$\text{PK: } \text{customerID}, \quad \text{gender}, \quad \text{SeniorCitizen}, \quad \text{Partner}, \quad \text{Dependents}, \quad \text{tenure}$$
2. **`services`** (Product Subscriptions & Add-ons):
   $$\text{PK: } \text{customerID}, \quad \text{PhoneService}, \quad \text{MultipleLines}, \quad \text{InternetService}, \quad \text{OnlineSecurity}, \dots$$
3. **`billing`** (Contract Terms & Charges):
   $$\text{PK: } \text{customerID}, \quad \text{Contract}, \quad \text{PaperlessBilling}, \quad \text{PaymentMethod}, \quad \text{MonthlyCharges}, \quad \text{TotalCharges}$$
4. **`churn_status`** (Target Outcome):
   $$\text{PK: } \text{customerID}, \quad \text{Churn} \in \{\text{'Yes'}, \text{'No'}\}$$

### Missing Value Treatment Rationale
During SQL cleaning (`sql/02_data_cleaning.sql`), exactly 11 customer records had empty strings for `TotalCharges`. All 11 records had $\text{tenure} = 0$, indicating new customer accounts created during the billing cycle that had not yet incurred their first month-end billing invoice. 
$$\text{Imputation Rule: } \text{TotalCharges} \leftarrow 0.00 \quad \text{for } \text{tenure} = 0$$
This preserves row integrity without dropping or distorting the customer base.

---

## 2. Feature Engineering Logic

Features engineered in `sql/03_feature_engineering.sql` and `src/feature_engineering.py`:

1. **Tenure Cohort Segmentation (`tenure_group`)**:
   $$\text{tenure\_group} = \begin{cases} 
   \text{'0-12'}, & \text{tenure} \in [0, 12] \\
   \text{'13-24'}, & \text{tenure} \in [13, 24] \\
   \text{'25-36'}, & \text{tenure} \in [25, 36] \\
   \text{'37-48'}, & \text{tenure} \in [37, 48] \\
   \text{'49-60'}, & \text{tenure} \in [49, 60] \\
   \text{'61-72'}, & \text{tenure} \in [61, 72] 
   \end{cases}$$

2. **Total Value-Added Services Count (`total_services_count`)**:
   $$\text{total\_services\_count} = \sum_{k \in \mathcal{S}} \mathbb{I}(s_k = \text{'Yes'}), \quad \mathcal{S} = \{\text{Security, Backup, Protection, TechSupport, StreamTV, StreamMovies}\}$$
   Range: $0 \le \text{total\_services\_count} \le 6$.

3. **Historical Average Spend (`avg_monthly_spend`)**:
   $$\text{avg\_monthly\_spend} = \begin{cases} 
   \text{MonthlyCharges}, & \text{tenure} = 0 \\
   \frac{\text{TotalCharges}}{\text{tenure}}, & \text{tenure} > 0 
   \end{cases}$$

4. **Annualized Recurring Revenue (`annualized_revenue`)**:
   $$\text{ARR} = \text{MonthlyCharges} \times 12.0$$

---

## 3. Machine Learning Modeling Formulation

### 3.1 Class Imbalance Mitigation (SMOTE)
The target distribution in the raw portfolio is imbalanced:
$$\text{Retained (Class 0)} = 5,174 \ (73.46\%), \quad \text{Churned (Class 1)} = 1,869 \ (26.54\%)$$

In the training split ($N = 5,634$), Class 0 represents 4,139 samples and Class 1 represents 1,495 samples. Training directly on imbalanced data causes standard estimators to optimize for overall accuracy at the expense of recall on churners. 

We applied **SMOTE (Synthetic Minority Over-sampling Technique)** strictly on $X_{\text{train}}$:
For each minority instance $x_i$, $k=5$ nearest minority neighbors are identified. Synthetic instances $x_{\text{new}}$ are synthesized along line segments:
$$x_{\text{new}} = x_i + \lambda (x_{zi} - x_i), \quad \lambda \sim U(0, 1)$$
This equalized the training set to 4,139 retained and 4,139 churned instances prior to model fitting.

### 3.2 Candidate Estimators

#### 1. Logistic Regression (L2 Regularized)
The posterior probability of customer churn is modeled as:
$$P(Y=1 \mid X) = \sigma(w^T X + b) = \frac{1}{1 + e^{-(w^T X + b)}}$$
Minimizing the cross-entropy loss with ridge regularization:
$$\mathcal{L}(w) = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \ln(\sigma(w^T x_i + b)) + (1 - y_i) \ln(1 - \sigma(w^T x_i + b)) \right] + \frac{\lambda}{2} \|w\|_2^2$$

#### 2. Random Forest Classifier
An ensemble of $B=200$ bootstrapped decision trees:
$$\hat{P}(Y=1 \mid X) = \frac{1}{B} \sum_{b=1}^B T_b(X)$$
Tree splits are selected by minimizing Gini impurity:
$$I_G(p) = 1 - \sum_{k=0}^1 p_k^2$$

---

## 4. Empirical Evaluation Matrix

Evaluation on held-out test partition ($N = 1,409$ accounts; Stratified 20%):

| Evaluation Metric | Logistic Regression (with SMOTE) | Random Forest (with SMOTE) | Business Implication |
|:------------------|:--------------------------------:|:--------------------------:|:---------------------|
| **Accuracy** | 75.87% | **76.44%** | Overall correct classification rate |
| **Precision (Churn)** | 53.54% | **54.23%** | Of those flagged as churners, ~54% actually churn |
| **Recall (Churn)** | 68.72% | **71.93%** | Captures ~72% of all actual churning accounts |
| **F1-Score (Churn)**| 60.19% | **61.84%** | Harmonic mean balancing precision and recall |
| **ROC-AUC** | 0.8319 | **0.8381** | Diagnostic discrimination ability across all cutoffs |

### Decision Boundary Selection
In customer retention strategy, a **False Negative** (a churner misclassified as safe who terminates service) incurs loss of the customer's full expected lifetime value ($> \$1,000$). Conversely, a **False Positive** (a loyal customer misclassified as at-risk) merely incurs the marginal marketing cost of a promotional offer ($< \$20$). 

Because Random Forest achieves higher Recall (71.93%) and higher ROC-AUC (0.8381), while Logistic Regression offers linear log-odds coefficients for executive presentations, both models are retained in the pipeline.

---

## 5. Active Account Scoring & Financial Exposure

Using the trained estimator, batch inference was executed across all 5,174 active accounts:
$$\text{churn\_risk\_score} = \hat{P}(\text{Churn} = \text{'Yes'} \mid X)$$

### Risk Tier Segmentation:
$$\text{risk\_tier} = \begin{cases} 
\text{High Risk}, & \text{score} \ge 0.70 \\
\text{Medium Risk}, & 0.40 \le \text{score} < 0.70 \\
\text{Low Risk}, & \text{score} < 0.40 
\end{cases}$$

### Active Customer Portfolio Distribution:
- **High Risk:** 434 accounts (8.39%) | Monthly Spend: $33,878.55 | Annualized ARR at Risk: **$406,542.60**
- **Medium Risk:** 1,073 accounts (20.74%) | Monthly Spend: $68,270.85 | Annualized ARR at Risk: **$819,250.20**
- **Low Risk:** 3,667 accounts (70.87%) | Monthly Spend: $214,836.35 | Protected Safe ARR: **$2,578,036.20**
- **Total Active Portfolio ARR:** **$3,803,829.00**
