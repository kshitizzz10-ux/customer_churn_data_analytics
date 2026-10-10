"""
src/feature_engineering.py
PwC Technology Consulting - Customer Churn & Revenue Retention Strategy

This module provides business feature engineering functions that capture
customer lifecycle stages, service depth, and spending behavior.
"""

import pandas as pd
import numpy as np


def create_tenure_groups(df: pd.DataFrame) -> pd.DataFrame:
    """
    Buckets customer tenure into actionable lifecycle cohorts:
    '0-12', '13-24', '25-36', '37-48', '49-60', '61-72'.
    """
    df_out = df.copy()
    bins = [-1, 12, 24, 36, 48, 60, 72]
    labels = ["0-12", "13-24", "25-36", "37-48", "49-60", "61-72"]
    df_out["tenure_group"] = pd.cut(df_out["tenure"], bins=bins, labels=labels)
    return df_out


def create_charge_tiers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorizes monthly spend into strategic billing tiers:
    - Low: < $35
    - Medium: $35 - $70
    - High: > $70
    """
    df_out = df.copy()
    conditions = [
        (df_out["MonthlyCharges"] < 35.0),
        (df_out["MonthlyCharges"] >= 35.0) & (df_out["MonthlyCharges"] <= 70.0),
        (df_out["MonthlyCharges"] > 70.0)
    ]
    choices = ["Low", "Medium", "High"]
    df_out["monthly_charge_tier"] = np.select(conditions, choices, default="Medium")
    return df_out


def count_services(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates total count of subscribed value-added services (range 0 to 6):
    OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies.
    """
    df_out = df.copy()
    add_ons = [
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", 
        "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    present_add_ons = [col for col in add_ons if col in df_out.columns]
    df_out["total_services_count"] = (df_out[present_add_ons] == "Yes").sum(axis=1)
    return df_out


def calculate_avg_spend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates historical average monthly spend (TotalCharges / tenure).
    For tenure = 0 (new onboarding accounts), uses MonthlyCharges.
    """
    df_out = df.copy()
    df_out["avg_monthly_spend"] = np.where(
        df_out["tenure"] == 0,
        df_out["MonthlyCharges"],
        (df_out["TotalCharges"] / df_out["tenure"]).round(2)
    )
    return df_out


def flag_premium_bundle(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flags whether customer maintains a premium multi-service bundle (3+ add-on services).
    """
    df_out = df.copy()
    if "total_services_count" not in df_out.columns:
        df_out = count_services(df_out)
    df_out["has_premium_bundle"] = np.where(df_out["total_services_count"] >= 3, "Yes", "No")
    return df_out


def calculate_annualized_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes annualized recurring revenue (MonthlyCharges * 12).
    """
    df_out = df.copy()
    df_out["annualized_revenue"] = (df_out["MonthlyCharges"] * 12.0).round(2)
    return df_out


def engineer_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline execution helper applying all feature transformations in sequence.
    """
    df_out = df.copy()
    df_out = create_tenure_groups(df_out)
    df_out = create_charge_tiers(df_out)
    df_out = count_services(df_out)
    df_out = calculate_avg_spend(df_out)
    df_out = flag_premium_bundle(df_out)
    df_out = calculate_annualized_revenue(df_out)
    return df_out
