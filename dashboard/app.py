"""
dashboard/app.py
Interactive Executive Churn & Revenue Retention Dashboard
PwC Technology Consulting Portfolio Simulation
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="TelcoMax | Churn & Revenue Retention Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom PwC-inspired CSS theme
st.markdown("""
<style>
    .main-header {
        font-size: 26px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 14px;
        color: #64748B;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #D04A02;
    }
    .metric-title {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #1E293B;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 11px;
        color: #94A3B8;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Data loading
@st.cache_data
def load_datasets():
    clean_path = os.path.join("data", "processed", "telco_churn_cleaned.csv")
    scored_path = os.path.join("data", "processed", "telco_churn_scored.csv")
    
    if not os.path.exists(clean_path):
        clean_path = os.path.join("..", "data", "processed", "telco_churn_cleaned.csv")
        scored_path = os.path.join("..", "data", "processed", "telco_churn_scored.csv")
        
    df_c = pd.read_csv(clean_path)
    df_s = pd.read_csv(scored_path)
    return df_c, df_s

try:
    df_cleaned, df_scored = load_datasets()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

# Sidebar Interactive Slicers
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/PricewaterhouseCoopers_Logo.svg/320px-PricewaterhouseCoopers_Logo.svg.png", width=140)
st.sidebar.markdown("### Interactive Dashboard Filters")

contract_filter = st.sidebar.multiselect(
    "Contract Type",
    options=df_cleaned["Contract"].unique(),
    default=df_cleaned["Contract"].unique()
)

internet_filter = st.sidebar.multiselect(
    "Internet Service",
    options=df_cleaned["InternetService"].unique(),
    default=df_cleaned["InternetService"].unique()
)

tenure_filter = st.sidebar.multiselect(
    "Tenure Cohort",
    options=sorted(df_cleaned["tenure_group"].dropna().unique()),
    default=sorted(df_cleaned["tenure_group"].dropna().unique())
)

# Filter DataFrames
df_c_filtered = df_cleaned[
    (df_cleaned["Contract"].isin(contract_filter)) &
    (df_cleaned["InternetService"].isin(internet_filter)) &
    (df_cleaned["tenure_group"].isin(tenure_filter))
]

df_s_filtered = df_scored[
    (df_scored["Contract"].isin(contract_filter)) &
    (df_scored["InternetService"].isin(internet_filter)) &
    (df_scored["tenure_group"].isin(tenure_filter))
]

# Tabs for 3 Dashboard Pages
tab1, tab2, tab3 = st.tabs([
    "📈 Page 1: Executive Portfolio Overview",
    "🤖 Page 2: Predictive Risk Segmentation",
    "👥 Page 3: Demographics & Ecosystem Deep Dive"
])

# ==============================================================================
# TAB 1: EXECUTIVE PORTFOLIO OVERVIEW
# ==============================================================================
with tab1:
    st.markdown('<div class="main-header">Executive Portfolio Churn & Revenue Exposure</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Diagnostic analysis across 7,043 subscriber accounts | PwC Technology Consulting Engagement</div>', unsafe_allow_html=True)
    
    # KPI Ribbon
    c1, c2, c3, c4 = st.columns(4)
    total_cust = len(df_c_filtered)
    churn_count = (df_c_filtered["Churn"] == "Yes").sum()
    churn_rate = (churn_count / total_cust * 100) if total_cust > 0 else 0
    arr_lost = df_c_filtered[df_c_filtered["Churn"] == "Yes"]["annualized_revenue"].sum()
    avg_tenure = df_c_filtered["tenure"].mean()
    
    with c1:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #2B6CB0;">
            <div class="metric-title">Customer Base</div>
            <div class="metric-value">{total_cust:,}</div>
            <div class="metric-sub">Total audited accounts</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #D04A02;">
            <div class="metric-title">Overall Churn Rate</div>
            <div class="metric-value" style="color: #D04A02;">{churn_rate:.2f}%</div>
            <div class="metric-sub">{churn_count:,} accounts lost</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #D04A02;">
            <div class="metric-title">Annual Revenue at Risk</div>
            <div class="metric-value" style="color: #D04A02;">${arr_lost:,.0f}</div>
            <div class="metric-sub">${arr_lost/12:,.0f} / month bleed</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #319795;">
            <div class="metric-title">Avg Customer Lifetime</div>
            <div class="metric-value">{avg_tenure:.1f} Mos</div>
            <div class="metric-sub">Portfolio longevity average</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Charts Row 1
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        c_agg = df_c_filtered.groupby("Contract")["Churn"].value_counts(normalize=True).unstack().fillna(0)
        c_rates = (c_agg.get("Yes", pd.Series(0, index=c_agg.index)) * 100).reset_index(name="Churn_Rate")
        fig_c = px.bar(
            c_rates, x="Contract", y="Churn_Rate",
            title="<b>Churn Rate by Contract Type</b> (Month-to-Month Drives 88.5% of Churn)",
            color_discrete_sequence=["#D04A02"],
            text_auto=".1f"
        )
        fig_c.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="", template="plotly_white")
        st.plotly_chart(fig_c, use_container_width=True)
        
    with r1_col2:
        t_agg = df_c_filtered.groupby("tenure_group", observed=False)["Churn"].value_counts(normalize=True).unstack().fillna(0)
        t_rates = (t_agg.get("Yes", pd.Series(0, index=t_agg.index)) * 100).reset_index(name="Churn_Rate")
        fig_t = px.line(
            t_rates, x="tenure_group", y="Churn_Rate",
            title="<b>Customer Lifecycle Vulnerability</b> (The 0-12 Month Onboarding Cliff)",
            markers=True, color_discrete_sequence=["#D04A02"]
        )
        fig_t.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Tenure Cohort (Months)", template="plotly_white")
        st.plotly_chart(fig_t, use_container_width=True)

    # Charts Row 2
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        inet_agg = df_c_filtered.groupby(["InternetService", "Churn"]).size().reset_index(name="Count")
        fig_inet = px.bar(
            inet_agg, x="InternetService", y="Count", color="Churn",
            barmode="stack", title="<b>Internet Service Split</b> (Fiber Optic Churn: 41.9%)",
            color_discrete_map={"No": "#2B6CB0", "Yes": "#D04A02"}
        )
        fig_inet.update_layout(template="plotly_white")
        st.plotly_chart(fig_inet, use_container_width=True)
        
    with r2_col2:
        st.markdown("<b>Top Lost Revenue Accounts (Executive Audit)</b>", unsafe_allow_html=True)
        top_lost = df_c_filtered[df_c_filtered["Churn"] == "Yes"].sort_values("MonthlyCharges", ascending=False).head(5)
        st.dataframe(
            top_lost[["customerID", "Contract", "InternetService", "MonthlyCharges", "annualized_revenue", "tenure"]],
            column_config={
                "customerID": "Customer ID",
                "MonthlyCharges": st.column_config.NumberColumn("Monthly Spend", format="$%.2f"),
                "annualized_revenue": st.column_config.NumberColumn("ARR Lost", format="$%.2f"),
                "tenure": "Tenure (Mos)"
            },
            hide_index=True,
            use_container_width=True
        )

# ==============================================================================
# TAB 2: PREDICTIVE RISK SEGMENTATION
# ==============================================================================
with tab2:
    st.markdown('<div class="main-header">Predictive Churn Risk Scoring & Active Revenue Exposure</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Forward-looking machine learning scores assigned to 5,174 active subscribers</div>', unsafe_allow_html=True)
    
    # KPI Ribbon
    p2_c1, p2_c2, p2_c3, p2_c4 = st.columns(4)
    high_risk_cnt = (df_s_filtered["risk_tier"] == "High Risk").sum()
    high_risk_arr = df_s_filtered[df_s_filtered["risk_tier"] == "High Risk"]["annualized_revenue"].sum()
    med_risk_arr = df_s_filtered[df_s_filtered["risk_tier"] == "Medium Risk"]["annualized_revenue"].sum()
    avg_prob = df_s_filtered["churn_risk_score"].mean() * 100
    
    with p2_c1:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #D04A02;">
            <div class="metric-title">High-Risk Active Accounts</div>
            <div class="metric-value" style="color: #D04A02;">{high_risk_cnt:,}</div>
            <div class="metric-sub">Score &ge; 0.70</div>
        </div>
        """, unsafe_allow_html=True)
    with p2_c2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #D04A02;">
            <div class="metric-title">High-Risk ARR Exposure</div>
            <div class="metric-value" style="color: #D04A02;">${high_risk_arr:,.0f}</div>
            <div class="metric-sub">${high_risk_arr/12:,.0f} / month at risk</div>
        </div>
        """, unsafe_allow_html=True)
    with p2_c3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #D97706;">
            <div class="metric-title">Medium-Risk ARR Exposure</div>
            <div class="metric-value" style="color: #D97706;">${med_risk_arr:,.0f}</div>
            <div class="metric-sub">Score 0.40 - 0.70</div>
        </div>
        """, unsafe_allow_html=True)
    with p2_c4:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #2B6CB0;">
            <div class="metric-title">Avg Churn Probability</div>
            <div class="metric-value">{avg_prob:.1f}%</div>
            <div class="metric-sub">Portfolio model expectation</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    p2_r1, p2_r2 = st.columns(2)
    with p2_r1:
        fig_scatter = px.scatter(
            df_s_filtered, x="MonthlyCharges", y="churn_risk_score", color="Contract",
            title="<b>Churn Risk Score vs. Monthly Charges</b>",
            color_discrete_map={"Month-to-month": "#D04A02", "One year": "#D97706", "Two year": "#2B6CB0"},
            opacity=0.6,
            hover_data=["customerID", "tenure", "annualized_revenue"]
        )
        fig_scatter.add_hline(y=0.70, line_dash="dash", line_color="#DC2626", annotation_text="High Risk Threshold (0.70)")
        fig_scatter.update_layout(yaxis_title="Predicted Churn Probability", xaxis_title="Monthly Charges ($)", template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with p2_r2:
        tier_summary = df_s_filtered.groupby("risk_tier", observed=False)["annualized_revenue"].sum().reset_index()
        fig_tier = px.bar(
            tier_summary, x="risk_tier", y="annualized_revenue",
            title="<b>Forward Annualized Revenue by Risk Tier ($)</b>",
            color="risk_tier",
            color_discrete_map={"High Risk": "#D04A02", "Medium Risk": "#D97706", "Low Risk": "#16A34A"},
            text_auto="$,.0f"
        )
        fig_tier.update_layout(yaxis_title="Annualized Revenue ($)", xaxis_title="", template="plotly_white", showlegend=False)
        st.plotly_chart(fig_tier, use_container_width=True)

    st.markdown("<b>Immediate Commercial Outreach Target List (Top Active Accounts at Risk)</b>", unsafe_allow_html=True)
    top_active_risk = df_s_filtered[df_s_filtered["risk_tier"] == "High Risk"].sort_values("MonthlyCharges", ascending=False).head(10)
    st.dataframe(
        top_active_risk[["customerID", "Contract", "InternetService", "tenure", "MonthlyCharges", "annualized_revenue", "churn_risk_score"]],
        column_config={
            "customerID": "Customer ID",
            "MonthlyCharges": st.column_config.NumberColumn("Monthly Spend", format="$%.2f"),
            "annualized_revenue": st.column_config.NumberColumn("Annual ARR", format="$%.2f"),
            "churn_risk_score": st.column_config.ProgressColumn("Risk Probability", min_value=0.0, max_value=1.0, format="%.2f")
        },
        hide_index=True,
        use_container_width=True
    )

# ==============================================================================
# TAB 3: DEMOGRAPHICS & ECOSYSTEM DEEP DIVE
# ==============================================================================
with tab3:
    st.markdown('<div class="main-header">Demographics & Ecosystem Stickiness Deep Dive</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating multi-service stickiness, household composition, and payment channel friction</div>', unsafe_allow_html=True)
    
    d_c1, d_c2 = st.columns(2)
    with d_c1:
        serv_agg = df_c_filtered.groupby("total_services_count")["Churn"].value_counts(normalize=True).unstack().fillna(0)
        serv_rates = (serv_agg.get("Yes", pd.Series(0, index=serv_agg.index)) * 100).reset_index(name="Churn_Rate")
        fig_s = px.bar(
            serv_rates, x="total_services_count", y="Churn_Rate",
            title="<b>Add-on Service Depth Curve</b> (5+ Services Drops Churn Below 13%)",
            color_discrete_sequence=["#319795"],
            text_auto=".1f"
        )
        fig_s.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Add-on Services Subscribed (0 to 6)", template="plotly_white")
        st.plotly_chart(fig_s, use_container_width=True)
        
    with d_c2:
        pay_agg = df_c_filtered.groupby("PaymentMethod")["Churn"].value_counts(normalize=True).unstack().fillna(0)
        pay_rates = (pay_agg.get("Yes", pd.Series(0, index=pay_agg.index)) * 100).reset_index(name="Churn_Rate")
        fig_p = px.bar(
            pay_rates.sort_values("Churn_Rate", ascending=False), y="PaymentMethod", x="Churn_Rate",
            orientation="h",
            title="<b>Churn Rate by Payment Channel</b> (Electronic Check Friction at 45.3%)",
            color_discrete_sequence=["#D04A02"],
            text_auto=".1f"
        )
        fig_p.update_layout(xaxis_title="Churn Rate (%)", yaxis_title="", template="plotly_white")
        st.plotly_chart(fig_p, use_container_width=True)

    d_r2_c1, d_r2_c2 = st.columns(2)
    with d_r2_c1:
        sn_agg = df_c_filtered.groupby(["SeniorCitizen", "gender"])["Churn"].apply(lambda s: (s == "Yes").mean() * 100).reset_index(name="Churn_Rate")
        fig_sn = px.bar(
            sn_agg, x="SeniorCitizen", y="Churn_Rate", color="gender",
            barmode="group", title="<b>Churn by Senior Citizen Status & Gender</b>",
            color_discrete_map={"Female": "#2B6CB0", "Male": "#D04A02"}
        )
        fig_sn.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Senior Citizen", template="plotly_white")
        st.plotly_chart(fig_sn, use_container_width=True)
        
    with d_r2_c2:
        fam_agg = df_c_filtered.groupby(["Partner", "Dependents"])["Churn"].apply(lambda s: (s == "Yes").mean() * 100).reset_index(name="Churn_Rate")
        fig_fam = px.bar(
            fam_agg, x="Partner", y="Churn_Rate", color="Dependents",
            barmode="group", title="<b>Churn by Household Composition (Partner x Dependents)</b>",
            color_discrete_map={"No": "#D04A02", "Yes": "#319795"}
        )
        fig_fam.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Has Partner", template="plotly_white")
        st.plotly_chart(fig_fam, use_container_width=True)
