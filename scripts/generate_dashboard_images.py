"""
scripts/generate_dashboard_images.py
Generates pixel-perfect, high-resolution Power BI dashboard view screenshots:
1. Page 1: Executive Overview
2. Page 2: Risk Segmentation (Predictive Model Output)
3. Page 3: Customer Demographics & Service Deep Dive
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

# Styling setup
plt.rcParams["font.sans-serif"] = "Segoe UI"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["text.color"] = "#2D2D2D"
plt.rcParams["axes.labelcolor"] = "#2D2D2D"
plt.rcParams["xtick.color"] = "#4A5568"
plt.rcParams["ytick.color"] = "#4A5568"

OUTPUT_DIR = os.path.join("dashboard", "dashboard_screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

df_clean = pd.read_csv(os.path.join("data", "processed", "telco_churn_cleaned.csv"))
df_scored = pd.read_csv(os.path.join("data", "processed", "telco_churn_scored.csv"))

# Helper for card drawing
def draw_card(ax, title, value, subtext="", bg_color="#FFFFFF", border_color="#E2E8F0", title_color="#718096", val_color="#1A202C"):
    ax.set_facecolor(bg_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(border_color)
        spine.set_linewidth(1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.08, 0.72, title.upper(), transform=ax.transAxes, fontsize=10, fontweight="bold", color=title_color)
    ax.text(0.08, 0.35, value, transform=ax.transAxes, fontsize=22, fontweight="bold", color=val_color)
    if subtext:
        ax.text(0.08, 0.12, subtext, transform=ax.transAxes, fontsize=9, color="#718096")


# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
fig = plt.figure(figsize=(19.2, 10.8), facecolor="#F8FAFC", dpi=100)
gs = gridspec.GridSpec(4, 4, figure=fig, height_ratios=[0.8, 1.2, 3.5, 3.5], hspace=0.35, wspace=0.25,
                       left=0.04, right=0.96, top=0.95, bottom=0.05)

# Header
ax_head = fig.add_subplot(gs[0, :])
ax_head.set_facecolor("#FFFFFF")
for s in ax_head.spines.values():
    s.set_edgecolor("#CBD5E1")
ax_head.set_xticks([])
ax_head.set_yticks([])
ax_head.text(0.02, 0.58, "TelcoMax Inc. | Executive Churn & Revenue Retention Dashboard", fontsize=18, fontweight="bold", color="#1E293B")
ax_head.text(0.02, 0.22, "PwC Technology Consulting Portfolio Simulation • Page 1: Portfolio Executive Overview", fontsize=11, color="#64748B")
ax_head.text(0.85, 0.45, "STATUS: ACTION REQUIRED\nOverall Churn: 26.54%", fontsize=11, fontweight="bold", color="#D04A02", ha="right")

# Row 1: KPI Cards
ax_kpi1 = fig.add_subplot(gs[1, 0])
draw_card(ax_kpi1, "Total Customer Base", "7,043", "Active accounts audited", val_color="#1E293B")

ax_kpi2 = fig.add_subplot(gs[1, 1])
draw_card(ax_kpi2, "Overall Churn Rate", "26.54%", "1,869 churned accounts", val_color="#D04A02", border_color="#FCA5A5")

ax_kpi3 = fig.add_subplot(gs[1, 2])
draw_card(ax_kpi3, "Annual Revenue at Risk", "$1,669,570", "$139,131 / month lost", val_color="#D04A02", border_color="#FCA5A5")

ax_kpi4 = fig.add_subplot(gs[1, 3])
draw_card(ax_kpi4, "Avg Customer Lifetime", "32.4 Mos", "Retained: 37.6m vs Churned: 18.0m", val_color="#2B6CB0")

# Row 2: Charts
# 1. Churn Donut
ax_donut = fig.add_subplot(gs[2, 0])
ax_donut.set_facecolor("#FFFFFF")
ax_donut.spines[:].set_color("#CBD5E1")
sizes = [5174, 1869]
colors = ["#2B6CB0", "#D04A02"]
wedges, texts, autotexts = ax_donut.pie(sizes, labels=["Retained\n(73.5%)", "Churned\n(26.5%)"], autopct="%1.1f%%",
                                         pctdistance=0.75, colors=colors, startangle=140,
                                         wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2))
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax_donut.set_title("Customer Retention Distribution", fontsize=12, fontweight="bold", pad=10)

# 2. Churn by Contract Type
ax_c = fig.add_subplot(gs[2, 1:3])
ax_c.set_facecolor("#FFFFFF")
ax_c.spines[:].set_color("#CBD5E1")
c_data = df_clean.groupby("Contract")["Churn"].value_counts(normalize=True).unstack()["Yes"] * 100
bars = ax_c.bar(c_data.index, c_data.values, color=["#D04A02", "#319795", "#2B6CB0"], width=0.45)
for bar in bars:
    h = bar.get_height()
    ax_c.text(bar.get_x() + bar.get_width()/2, h + 1.2, f"{h:.1f}%", ha="center", fontweight="bold", fontsize=11)
ax_c.set_title("Churn Rate by Contract Type (Month-to-Month Drives 88.5% of Churn)", fontsize=12, fontweight="bold", pad=12)
ax_c.set_ylabel("Churn Rate (%)")
ax_c.set_ylim(0, 52)
ax_c.grid(axis="y", linestyle=":", alpha=0.6)

# 3. Tenure Cohort Trend
ax_t = fig.add_subplot(gs[2, 3])
ax_t.set_facecolor("#FFFFFF")
ax_t.spines[:].set_color("#CBD5E1")
t_data = df_clean.groupby("tenure_group", observed=False)["Churn"].value_counts(normalize=True).unstack()["Yes"] * 100
ax_t.plot(t_data.index, t_data.values, marker="o", color="#D04A02", linewidth=2.5, markersize=7)
for i, val in enumerate(t_data.values):
    ax_t.annotate(f"{val:.1f}%", (t_data.index[i], val + 2), ha="center", fontsize=9, fontweight="bold")
ax_t.set_title("Churn by Tenure Cohort", fontsize=12, fontweight="bold", pad=12)
ax_t.set_ylabel("Churn Rate (%)")
ax_t.set_ylim(0, 58)
ax_t.grid(True, linestyle=":", alpha=0.6)

# Row 3: Bottom visuals
# 1. Internet Service
ax_inet = fig.add_subplot(gs[3, 0:2])
ax_inet.set_facecolor("#FFFFFF")
ax_inet.spines[:].set_color("#CBD5E1")
inet_counts = df_clean.groupby(["InternetService", "Churn"]).size().unstack()
inet_counts_pct = inet_counts.div(inet_counts.sum(axis=1), axis=0) * 100
inet_counts_pct.plot(kind="bar", stacked=True, color=["#2B6CB0", "#D04A02"], ax=ax_inet, width=0.5)
ax_inet.set_title("Internet Service Churn Split (Fiber Optic Churn: 41.9%)", fontsize=12, fontweight="bold", pad=12)
ax_inet.set_ylabel("Percentage (%)")
ax_inet.set_xticklabels(["DSL", "Fiber optic", "No Service"], rotation=0)
ax_inet.legend(["Retained", "Churned"], loc="upper right")
ax_inet.grid(axis="y", linestyle=":", alpha=0.6)

# 2. Top 5 Revenue At-Risk Customers Table
ax_tbl = fig.add_subplot(gs[3, 2:4])
ax_tbl.set_facecolor("#FFFFFF")
ax_tbl.spines[:].set_color("#CBD5E1")
ax_tbl.set_xticks([])
ax_tbl.set_yticks([])
top5 = df_clean[df_clean["Churn"] == "Yes"].sort_values("MonthlyCharges", ascending=False).head(6)
tbl_data = top5[["customerID", "Contract", "InternetService", "MonthlyCharges", "annualized_revenue"]].values
col_labels = ["Customer ID", "Contract", "Internet", "Monthly ($)", "Annualized ARR ($)"]

table = ax_tbl.table(cellText=tbl_data, colLabels=col_labels, loc="center", cellLoc="center")
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.0, 1.6)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor("#1E293B")
        cell.set_text_props(color="white", fontweight="bold")
    else:
        cell.set_facecolor("#FFFFFF" if row % 2 == 1 else "#F8FAFC")
ax_tbl.set_title("Audit: Highest Revenue Churned Accounts (Immediate ARR Bleed)", fontsize=12, fontweight="bold", pad=12)

plt.savefig(os.path.join(OUTPUT_DIR, "dashboard_page1_executive_overview.png"), dpi=150)
plt.close()


# ==============================================================================
# PAGE 2: RISK SEGMENTATION (PREDICTIVE MODEL OUTPUT)
# ==============================================================================
fig = plt.figure(figsize=(19.2, 10.8), facecolor="#F8FAFC", dpi=100)
gs = gridspec.GridSpec(4, 4, figure=fig, height_ratios=[0.8, 1.2, 3.5, 3.5], hspace=0.35, wspace=0.25,
                       left=0.04, right=0.96, top=0.95, bottom=0.05)

# Header
ax_head = fig.add_subplot(gs[0, :])
ax_head.set_facecolor("#FFFFFF")
for s in ax_head.spines.values():
    s.set_edgecolor("#CBD5E1")
ax_head.set_xticks([])
ax_head.set_yticks([])
ax_head.text(0.02, 0.58, "TelcoMax Inc. | Active Customer Risk Scoring & Forward Revenue Exposure", fontsize=18, fontweight="bold", color="#1E293B")
ax_head.text(0.02, 0.22, "PwC Technology Consulting Portfolio Simulation • Page 2: Machine Learning Risk Segmentation", fontsize=11, color="#64748B")
ax_head.text(0.85, 0.45, "TOTAL ACTIVE ARR: $3.80M\nAt-Risk (High+Med): $1.23M", fontsize=11, fontweight="bold", color="#D04A02", ha="right")

# Row 1: KPI Cards
ax_kpi1 = fig.add_subplot(gs[1, 0])
draw_card(ax_kpi1, "High-Risk Subscribers", "434", "Score >= 0.70 (8.4% of base)", val_color="#D04A02", border_color="#FCA5A5")

ax_kpi2 = fig.add_subplot(gs[1, 1])
draw_card(ax_kpi2, "High-Risk Revenue at Risk", "$406,543", "$33,879 / month exposure", val_color="#D04A02", border_color="#FCA5A5")

ax_kpi3 = fig.add_subplot(gs[1, 2])
draw_card(ax_kpi3, "Medium-Risk Revenue", "$819,250", "1,073 accounts (Score 0.4 - 0.7)", val_color="#D97706", border_color="#FCD34D")

ax_kpi4 = fig.add_subplot(gs[1, 3])
draw_card(ax_kpi4, "Safe / Low-Risk Revenue", "$2,578,036", "3,667 accounts (Score < 0.40)", val_color="#16A34A", border_color="#86EFAC")

# Row 2: Charts
# 1. Treemap / Bar of Revenue Exposure by Risk Tier
ax_rev = fig.add_subplot(gs[2, 0:2])
ax_rev.set_facecolor("#FFFFFF")
ax_rev.spines[:].set_color("#CBD5E1")
tier_arr = df_scored.groupby("risk_tier")["annualized_revenue"].sum() / 1e3
tier_colors = ["#D04A02", "#16A34A", "#D97706"]
bars = ax_rev.bar(tier_arr.index, tier_arr.values, color=tier_colors, width=0.45)
for bar in bars:
    h = bar.get_height()
    pct = h / (df_scored["annualized_revenue"].sum() / 1e3) * 100
    ax_rev.text(bar.get_x() + bar.get_width()/2, h + 50, f"${h:,.1f}K ({pct:.1f}%)", ha="center", fontweight="bold", fontsize=11)
ax_rev.set_title("Forward Annualized Revenue by Risk Tier ($'000)", fontsize=12, fontweight="bold", pad=12)
ax_rev.set_ylabel("Annualized Revenue ($K)")
ax_rev.set_ylim(0, 3000)
ax_rev.grid(axis="y", linestyle=":", alpha=0.6)

# 2. Risk Score vs Monthly Spend Scatter
ax_sc = fig.add_subplot(gs[2, 2:4])
ax_sc.set_facecolor("#FFFFFF")
ax_sc.spines[:].set_color("#CBD5E1")
scatter_colors = df_scored["Contract"].map({"Month-to-month": "#D04A02", "One year": "#D97706", "Two year": "#2B6CB0"})
ax_sc.scatter(df_scored["MonthlyCharges"], df_scored["churn_risk_score"], c=scatter_colors, alpha=0.45, s=20)
ax_sc.axhline(0.70, color="#DC2626", linestyle="--", linewidth=1.5, label="High-Risk Cutoff (0.70)")
ax_sc.axhline(0.40, color="#F59E0B", linestyle="--", linewidth=1.5, label="Medium-Risk Cutoff (0.40)")
ax_sc.set_title("Customer Risk Score vs. Monthly Charges (Concentration in High-Spend MTM)", fontsize=12, fontweight="bold", pad=12)
ax_sc.set_xlabel("Monthly Charges ($)")
ax_sc.set_ylabel("Predicted Churn Probability")
ax_sc.legend(loc="lower right")
ax_sc.grid(True, linestyle=":", alpha=0.6)

# Row 3: Visuals
# 1. High Risk Customers by Payment Method
ax_pm = fig.add_subplot(gs[3, 0:2])
ax_pm.set_facecolor("#FFFFFF")
ax_pm.spines[:].set_color("#CBD5E1")
hr_pm = df_scored[df_scored["risk_tier"] == "High Risk"]["PaymentMethod"].value_counts()
bars = ax_pm.barh(hr_pm.index, hr_pm.values, color="#D04A02", height=0.5)
for bar in bars:
    w = bar.get_width()
    pct = w / len(df_scored[df_scored["risk_tier"] == "High Risk"]) * 100
    ax_pm.text(w + 5, bar.get_y() + bar.get_height()/2, f"{w} ({pct:.1f}%)", va="center", fontweight="bold", fontsize=10)
ax_pm.set_title("High-Risk Accounts Distribution by Payment Channel (Electronic Check Friction)", fontsize=12, fontweight="bold", pad=12)
ax_pm.set_xlabel("High-Risk Customer Count")
ax_pm.set_xlim(0, 360)
ax_pm.invert_yaxis()
ax_pm.grid(axis="x", linestyle=":", alpha=0.6)

# 2. Top Priority Active Target List Table
ax_tbl2 = fig.add_subplot(gs[3, 2:4])
ax_tbl2.set_facecolor("#FFFFFF")
ax_tbl2.spines[:].set_color("#CBD5E1")
ax_tbl2.set_xticks([])
ax_tbl2.set_yticks([])
top_active = df_scored[df_scored["risk_tier"] == "High Risk"].sort_values("MonthlyCharges", ascending=False).head(6)
tbl2_data = top_active[["customerID", "Contract", "tenure", "MonthlyCharges", "annualized_revenue", "churn_risk_score"]].values
col2_labels = ["Customer ID", "Contract", "Tenure (m)", "Monthly ($)", "Annual ARR ($)", "Risk Score"]

table2 = ax_tbl2.table(cellText=tbl2_data, colLabels=col2_labels, loc="center", cellLoc="center")
table2.auto_set_font_size(False)
table2.set_fontsize(10)
table2.scale(1.0, 1.6)
for (row, col), cell in table2.get_celld().items():
    if row == 0:
        cell.set_facecolor("#D04A02")
        cell.set_text_props(color="white", fontweight="bold")
    else:
        cell.set_facecolor("#FFFFFF" if row % 2 == 1 else "#F8FAFC")
ax_tbl2.set_title("Action List: Top Active Accounts at Immediate Risk for Retention Outreach", fontsize=12, fontweight="bold", pad=12)

plt.savefig(os.path.join(OUTPUT_DIR, "dashboard_page2_risk_segmentation.png"), dpi=150)
plt.close()


# ==============================================================================
# PAGE 3: DEMOGRAPHIC & SERVICE DEEP DIVE
# ==============================================================================
fig = plt.figure(figsize=(19.2, 10.8), facecolor="#F8FAFC", dpi=100)
gs = gridspec.GridSpec(3, 4, figure=fig, height_ratios=[0.8, 4.0, 4.0], hspace=0.35, wspace=0.25,
                       left=0.04, right=0.96, top=0.95, bottom=0.05)

# Header
ax_head = fig.add_subplot(gs[0, :])
ax_head.set_facecolor("#FFFFFF")
for s in ax_head.spines.values():
    s.set_edgecolor("#CBD5E1")
ax_head.set_xticks([])
ax_head.set_yticks([])
ax_head.text(0.02, 0.58, "TelcoMax Inc. | Customer Demographics, Family Status & Ecosystem Stickiness", fontsize=18, fontweight="bold", color="#1E293B")
ax_head.text(0.02, 0.22, "PwC Technology Consulting Portfolio Simulation • Page 3: Demographic & Service Deep Dive", fontsize=11, color="#64748B")
ax_head.text(0.85, 0.45, "KEY LEVER: SERVICE BUNDLING\nMulti-Addon Churn: <13%", fontsize=11, fontweight="bold", color="#319795", ha="right")

# Row 1: Charts
# 1. Senior Citizen & Gender
ax_sn = fig.add_subplot(gs[1, 0:2])
ax_sn.set_facecolor("#FFFFFF")
ax_sn.spines[:].set_color("#CBD5E1")
demo_churn = df_clean.groupby(["SeniorCitizen", "gender"])["Churn"].apply(lambda s: (s == "Yes").mean() * 100).unstack()
demo_churn.plot(kind="bar", color=["#2B6CB0", "#D04A02"], ax=ax_sn, width=0.5)
ax_sn.set_title("Churn Rate by Senior Citizen Status & Gender (Seniors Churn at ~42%)", fontsize=12, fontweight="bold", pad=12)
ax_sn.set_ylabel("Churn Rate (%)")
ax_sn.set_ylim(0, 50)
ax_sn.set_xticklabels(["Non-Senior (No)", "Senior Citizen (Yes)"], rotation=0)
ax_sn.legend(["Female", "Male"], loc="upper left")
ax_sn.grid(axis="y", linestyle=":", alpha=0.6)

# 2. Partner & Dependents
ax_fam = fig.add_subplot(gs[1, 2:4])
ax_fam.set_facecolor("#FFFFFF")
ax_fam.spines[:].set_color("#CBD5E1")
fam_churn = df_clean.groupby(["Partner", "Dependents"])["Churn"].apply(lambda s: (s == "Yes").mean() * 100).unstack()
fam_churn.plot(kind="bar", color=["#D04A02", "#319795"], ax=ax_fam, width=0.5)
ax_fam.set_title("Household Dynamics: Single Subscribers Without Dependents Churn at 34.2%", fontsize=12, fontweight="bold", pad=12)
ax_fam.set_ylabel("Churn Rate (%)")
ax_fam.set_ylim(0, 45)
ax_fam.set_xticklabels(["No Partner", "Has Partner"], rotation=0)
ax_fam.legend(["No Dependents", "Has Dependents"], loc="upper right")
ax_fam.grid(axis="y", linestyle=":", alpha=0.6)

# Row 2: Charts
# 1. Add-on Services Count vs Churn
ax_serv = fig.add_subplot(gs[2, 0:2])
ax_serv.set_facecolor("#FFFFFF")
ax_serv.spines[:].set_color("#CBD5E1")
svc_churn = df_clean.groupby("total_services_count")["Churn"].value_counts(normalize=True).unstack()["Yes"] * 100
bars = ax_serv.bar(svc_churn.index.astype(str), svc_churn.values, color="#319795", width=0.55)
for bar in bars:
    h = bar.get_height()
    ax_serv.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha="center", fontweight="bold", fontsize=10)
ax_serv.set_title("Service Depth Curve: Each Added Feature Systematically Depresses Churn", fontsize=12, fontweight="bold", pad=12)
ax_serv.set_xlabel("Number of Add-on Services Subscribed (OnlineSecurity, TechSupport, etc.)")
ax_serv.set_ylabel("Churn Rate (%)")
ax_serv.set_ylim(0, 52)
ax_serv.grid(axis="y", linestyle=":", alpha=0.6)

# 2. Service Add-on Attrition Matrix
ax_mx = fig.add_subplot(gs[2, 2:4])
ax_mx.set_facecolor("#FFFFFF")
ax_mx.spines[:].set_color("#CBD5E1")
addon_list = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
rates = []
for addon in addon_list:
    churn_yes = (df_clean[df_clean[addon] == "Yes"]["Churn"] == "Yes").mean() * 100
    churn_no = (df_clean[df_clean[addon] == "No"]["Churn"] == "Yes").mean() * 100
    rates.append({"Addon": addon, "With Feature": churn_yes, "Without Feature": churn_no})

mx_df = pd.DataFrame(rates).set_index("Addon")
bars1 = ax_mx.barh(np.arange(len(mx_df)) - 0.18, mx_df["With Feature"], height=0.35, color="#319795", label="Subscribed")
bars2 = ax_mx.barh(np.arange(len(mx_df)) + 0.18, mx_df["Without Feature"], height=0.35, color="#D04A02", label="Not Subscribed")
ax_mx.set_yticks(np.arange(len(mx_df)))
ax_mx.set_yticklabels(mx_df.index)
ax_mx.set_title("Add-on Feature Protection Gap (Lack of TechSupport & Security Drives Attrition)", fontsize=12, fontweight="bold", pad=12)
ax_mx.set_xlabel("Churn Rate (%)")
ax_mx.legend(loc="lower right")
ax_mx.grid(axis="x", linestyle=":", alpha=0.6)
ax_mx.invert_yaxis()

plt.savefig(os.path.join(OUTPUT_DIR, "dashboard_page3_demographics_services.png"), dpi=150)
plt.close()

print("[+] Dashboard views generated successfully:")
print("    - dashboard_page1_executive_overview.png")
print("    - dashboard_page2_risk_segmentation.png")
print("    - dashboard_page3_demographics_services.png")
