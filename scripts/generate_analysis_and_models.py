"""
scripts/generate_analysis_and_models.py
Generates full exploratory data analysis, trains and evaluates predictive models,
produces visualizations, and scores active customer accounts.
"""

import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath("."))

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

# Styling for PwC-quality consulting visualizations
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.labelweight"] = "bold"

OUTPUT_IMG_DIR = os.path.join("dashboard", "dashboard_screenshots")
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)
os.makedirs("models", exist_ok=True)

# 1. Load Data
df = pd.read_csv(os.path.join("data", "processed", "telco_churn_cleaned.csv"))
print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# ==============================================================================
# EDA CHARTS GENERATION
# ==============================================================================
print("[*] Generating EDA Visualizations...")

# 1. Churn Distribution
fig, ax = plt.subplots(figsize=(6, 4.5))
churn_counts = df["Churn"].value_counts()
colors = ["#2B6CB0", "#D04A02"]
bars = ax.bar(churn_counts.index, churn_counts.values, color=colors, width=0.55, edgecolor="none")
for bar in bars:
    yval = bar.get_height()
    pct = yval / len(df) * 100
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 50, f"{yval:,}\n({pct:.1f}%)", ha="center", va="bottom", fontweight="bold")
ax.set_title("Customer Churn Distribution (Baseline 26.5% Churn)", pad=15)
ax.set_ylabel("Customer Count")
ax.set_ylim(0, 6000)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "eda_churn_distribution.png"), dpi=300)
plt.close()

# 2. Churn by Contract Type
fig, ax = plt.subplots(figsize=(7, 4.5))
contract_churn = df.groupby("Contract")["Churn"].value_counts(normalize=True).unstack()["Yes"] * 100
contract_counts = df["Contract"].value_counts()[contract_churn.index]
bars = ax.bar(contract_churn.index, contract_churn.values, color="#D04A02", width=0.5)
for bar, total in zip(bars, contract_counts):
    val = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, val + 1, f"{val:.1f}%\n(N={total:,})", ha="center", va="bottom", fontweight="bold")
ax.set_title("Churn Rate by Contract Type (Month-to-Month at 42.7%)", pad=15)
ax.set_ylabel("Churn Rate (%)")
ax.set_ylim(0, 55)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "eda_churn_by_contract.png"), dpi=300)
plt.close()

# 3. Churn by Internet Service
fig, ax = plt.subplots(figsize=(7, 4.5))
inet_churn = df.groupby("InternetService")["Churn"].value_counts(normalize=True).unstack()["Yes"] * 100
bars = ax.bar(inet_churn.index, inet_churn.values, color=["#319795", "#D04A02", "#718096"], width=0.5)
for bar in bars:
    val = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, val + 1, f"{val:.1f}%", ha="center", va="bottom", fontweight="bold")
ax.set_title("Churn Rate by Internet Architecture (Fiber Optic at 41.9%)", pad=15)
ax.set_ylabel("Churn Rate (%)")
ax.set_ylim(0, 50)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "eda_churn_by_internet.png"), dpi=300)
plt.close()

# 4. Churn by Tenure Cohort
fig, ax = plt.subplots(figsize=(7.5, 4.5))
tenure_churn = df.groupby("tenure_group", observed=False)["Churn"].value_counts(normalize=True).unstack()["Yes"] * 100
ax.plot(tenure_churn.index, tenure_churn.values, marker="o", color="#D04A02", linewidth=2.5, markersize=8)
for i, txt in enumerate(tenure_churn.values):
    ax.annotate(f"{txt:.1f}%", (tenure_churn.index[i], txt + 1.5), ha="center", fontweight="bold")
ax.set_title("Customer Lifecycle Vulnerability: Churn Drops with Tenure", pad=15)
ax.set_xlabel("Tenure Cohort (Months)")
ax.set_ylabel("Churn Rate (%)")
ax.set_ylim(0, 55)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "eda_churn_by_tenure.png"), dpi=300)
plt.close()

# 5. Churn by Payment Method
fig, ax = plt.subplots(figsize=(8, 4.5))
pay_churn = df.groupby("PaymentMethod")["Churn"].value_counts(normalize=True).unstack()["Yes"].sort_values(ascending=False) * 100
colors = ["#D04A02" if "Electronic" in x else "#2B6CB0" for x in pay_churn.index]
bars = ax.barh(pay_churn.index, pay_churn.values, color=colors, height=0.55)
for bar in bars:
    val = bar.get_width()
    ax.text(val + 0.8, bar.get_y() + bar.get_height()/2.0, f"{val:.1f}%", va="center", fontweight="bold")
ax.set_title("Payment Friction: Electronic Check Churn Reaches 45.3%", pad=15)
ax.set_xlabel("Churn Rate (%)")
ax.set_xlim(0, 55)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "eda_churn_by_payment.png"), dpi=300)
plt.close()

# 6. Churn by Add-on Services Count
fig, ax = plt.subplots(figsize=(7.5, 4.5))
serv_churn = df.groupby("total_services_count")["Churn"].value_counts(normalize=True).unstack()["Yes"] * 100
bars = ax.bar(serv_churn.index.astype(str), serv_churn.values, color="#319795", width=0.55)
for bar in bars:
    val = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, val + 1, f"{val:.1f}%", ha="center", va="bottom", fontweight="bold")
ax.set_title("Service Depth Stickiness: 5+ Add-ons Drops Churn Under 13%", pad=15)
ax.set_xlabel("Number of Add-on Services Subscribed (0 to 6)")
ax.set_ylabel("Churn Rate (%)")
ax.set_ylim(0, 55)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "eda_churn_by_services_count.png"), dpi=300)
plt.close()

# 7. Correlation Heatmap
df_num_corr = df.copy()
df_num_corr["Churn_Binary"] = (df_num_corr["Churn"] == "Yes").astype(int)
df_num_corr["SeniorCitizen_Num"] = (df_num_corr["SeniorCitizen"] == "Yes").astype(int)
df_num_corr["Partner_Num"] = (df_num_corr["Partner"] == "Yes").astype(int)
df_num_corr["Dependents_Num"] = (df_num_corr["Dependents"] == "Yes").astype(int)
df_num_corr["Paperless_Num"] = (df_num_corr["PaperlessBilling"] == "Yes").astype(int)
df_num_corr["MonthToMonth_Num"] = (df_num_corr["Contract"] == "Month-to-month").astype(int)
df_num_corr["FiberOptic_Num"] = (df_num_corr["InternetService"] == "Fiber optic").astype(int)
df_num_corr["ElectronicCheck_Num"] = (df_num_corr["PaymentMethod"] == "Electronic check").astype(int)

corr_cols = [
    "Churn_Binary", "tenure", "MonthlyCharges", "TotalCharges", 
    "total_services_count", "MonthToMonth_Num", "FiberOptic_Num", 
    "ElectronicCheck_Num", "Paperless_Num", "SeniorCitizen_Num", "Partner_Num"
]
corr_matrix = df_num_corr[corr_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax, linewidths=0.5)
ax.set_title("Executive Correlation Matrix: Primary Drivers of Customer Churn", pad=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "eda_correlation_heatmap.png"), dpi=300)
plt.close()

# ==============================================================================
# MODEL TRAINING & EVALUATION
# ==============================================================================
print("[*] Preparing Modeling Pipeline & Encoding...")

from src.data_preprocessing import encode_features, scale_features

X, y, feature_names = encode_features(df)
print(f"Feature set size: {X.shape[1]} features")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "total_services_count", "avg_monthly_spend"]
X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test, num_cols)

print(f"Pre-SMOTE Training Distribution: Retained={sum(y_train==0)}, Churned={sum(y_train==1)}")
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)
print(f"Post-SMOTE Training Distribution: Retained={sum(y_train_res==0)}, Churned={sum(y_train_res==1)}")

# 1. Train Logistic Regression
print("[*] Training Logistic Regression...")
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_res, y_train_res)

# 2. Train Random Forest
print("[*] Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=12, min_samples_split=5)
rf_model.fit(X_train_res, y_train_res)

# Evaluate Models
def get_metrics(model, name, X_val, y_val):
    preds = model.predict(X_val)
    probas = model.predict_proba(X_val)[:, 1]
    return {
        "Model": name,
        "Accuracy": accuracy_score(y_val, preds),
        "Precision": precision_score(y_val, preds),
        "Recall": recall_score(y_val, preds),
        "F1-Score": f1_score(y_val, preds),
        "ROC-AUC": roc_auc_score(y_val, probas),
        "Confusion_Matrix": confusion_matrix(y_val, preds),
        "Report": classification_report(y_val, preds, target_names=["Retained", "Churned"])
    }

m_lr = get_metrics(lr_model, "Logistic Regression", X_test_scaled, y_test)
m_rf = get_metrics(rf_model, "Random Forest", X_test_scaled, y_test)

metrics_df = pd.DataFrame([
    {k: round(v, 4) if isinstance(v, float) else v for k, v in m_lr.items() if k not in ["Confusion_Matrix", "Report"]},
    {k: round(v, 4) if isinstance(v, float) else v for k, v in m_rf.items() if k not in ["Confusion_Matrix", "Report"]}
])
print("\n" + "="*60)
print("MODEL EVALUATION COMPARISON TABLE:")
print("="*60)
print(metrics_df.to_string(index=False))

# Plot ROC Curves
fig, ax = plt.subplots(figsize=(7, 6))
for m_name, model, col in [("Logistic Regression", lr_model, "#2B6CB0"), ("Random Forest", rf_model, "#D04A02")]:
    probas = model.predict_proba(X_test_scaled)[:, 1]
    auc_v = roc_auc_score(y_test, probas)
    fpr, tpr, _ = roc_curve(y_test, probas)
    ax.plot(fpr, tpr, label=f"{m_name} (AUC = {auc_v:.3f})", color=col, linewidth=2.5)

ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random Baseline (AUC = 0.500)")
ax.set_title("Comparative ROC Curves: Churn Prediction Models", pad=15)
ax.set_xlabel("False Positive Rate (1 - Specificity)")
ax.set_ylabel("True Positive Rate (Recall)")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "model_roc_comparison.png"), dpi=300)
plt.close()

# Plot Confusion Matrices
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for ax, (m_name, model, cmap) in zip(axes, [("Logistic Regression", lr_model, "Blues"), ("Random Forest", rf_model, "Oranges")]):
    cm = confusion_matrix(y_test, model.predict(X_test_scaled))
    sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, cbar=False, ax=ax,
                xticklabels=["Retained", "Churned"], yticklabels=["Retained", "Churned"],
                annot_kws={"size": 13, "weight": "bold"})
    ax.set_title(f"{m_name} Confusion Matrix", pad=12)
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("Actual Label")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "model_confusion_matrices.png"), dpi=300)
plt.close()

# Plot Feature Importance (Random Forest & Logistic Regression)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

rf_imp = pd.Series(rf_model.feature_importances_, index=feature_names).nlargest(12).sort_values(ascending=True)
rf_imp.plot(kind="barh", color="#D04A02", ax=ax1)
ax1.set_title("Top 12 Features (Random Forest Importance)", pad=12)
ax1.set_xlabel("Relative Importance")

lr_coef = pd.Series(lr_model.coef_[0], index=feature_names)
top_lr = lr_coef.abs().nlargest(12).index
lr_coef_sub = lr_coef[top_lr].sort_values(ascending=True)
lr_colors = ["#2B6CB0" if x > 0 else "#718096" for x in lr_coef_sub.values]
lr_coef_sub.plot(kind="barh", color=lr_colors, ax=ax2)
ax2.set_title("Top 12 Features (Logistic Regression Coefficients)", pad=12)
ax2.set_xlabel("Log-Odds Coefficient")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_IMG_DIR, "model_feature_importance.png"), dpi=300)
plt.close()

# Best Model Selection
# Business Decision: We prioritize Recall for the Churn class (identifying as many at-risk customers as possible)
# Logistic Regression achieved Recall: 79.9% / 80% with SMOTE, AUC: 0.844. Random Forest achieved AUC: 0.835, Recall: 74.3%.
best_model = lr_model  # Chosen for superior recall and direct interpretability
joblib.dump(best_model, os.path.join("models", "best_churn_model.joblib"))
joblib.dump(scaler, os.path.join("models", "scaler.joblib"))
joblib.dump(feature_names, os.path.join("models", "feature_names.joblib"))
joblib.dump(rf_model, os.path.join("models", "random_forest_model.joblib"))
print("[+] Models serialized into models/ directory.")

# ==============================================================================
# BATCH SCORING ACTIVE CUSTOMERS
# ==============================================================================
print("[*] Scoring Active Customers...")
from src.model_scoring import score_customers, export_scored_data, calculate_revenue_at_risk

# Filter to active accounts
active_df = df[df["Churn"] == "No"].copy()
print(f"Active accounts to score: {len(active_df)}")

scored_df = score_customers(best_model, active_df, feature_names, scaler)
scored_csv_path = os.path.join("data", "processed", "telco_churn_scored.csv")
export_scored_data(scored_df, scored_csv_path)

risk_summary = calculate_revenue_at_risk(scored_df)
print("\n" + "="*60)
print("ACTIVE CUSTOMER RISK SEGMENTATION SUMMARY:")
print("="*60)
print(risk_summary["summary_table"].to_string(index=False))

print(f"\nTotal Active Customer Annualized Revenue: ${risk_summary['total_annual_revenue']:,.2f}")
print(f"High-Risk Annualized Revenue at Risk:    ${risk_summary['high_risk_annual_revenue']:,.2f}")

# Top 10 High Risk Customers
top_risk = scored_df[scored_df["risk_tier"] == "High Risk"].sort_values("MonthlyCharges", ascending=False).head(10)
print("\nTop 10 High Risk Accounts by Monthly Spend:")
cols_to_show = ["customerID", "Contract", "tenure", "MonthlyCharges", "annualized_revenue", "churn_risk_score"]
print(top_risk[cols_to_show].to_string(index=False))

print("\n[+] Analysis, modeling, scoring, and visualizations complete!")
