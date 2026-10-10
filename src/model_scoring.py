"""
src/model_scoring.py
PwC Technology Consulting - Customer Churn & Revenue Retention Strategy

This module provides batch scoring capabilities to assign churn probabilities,
risk tiers, and revenue exposure metrics to active accounts.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List
from src.data_preprocessing import encode_features, scale_features


def load_model(filepath: str) -> Any:
    """
    Loads serialized machine learning model artifact.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found at: {filepath}")
    return joblib.load(filepath)


def score_customers(
    model: Any, 
    df: pd.DataFrame, 
    feature_names: List[str], 
    scaler: Any
) -> pd.DataFrame:
    """
    Scores customer records with predicted churn probability and risk tier.

    Risk Tiers:
    - High Risk: score >= 0.70
    - Medium Risk: 0.40 <= score < 0.70
    - Low Risk: score < 0.40

    Parameters:
        model: Trained classifier supporting predict_proba.
        df (pd.DataFrame): Dataset of customers (typically active subscribers).
        feature_names (List[str]): Expected model feature columns.
        scaler: Fitted StandardScaler instance.

    Returns:
        pd.DataFrame: Original DataFrame augmented with scoring columns.
    """
    df_scored = df.copy()

    # Encode features matching training schema
    X_enc, _, _ = encode_features(df_scored)

    # Ensure all required features are present
    for col in feature_names:
        if col not in X_enc.columns:
            X_enc[col] = 0
    X_enc = X_enc[feature_names]

    # Scale numerical columns
    num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "total_services_count", "avg_monthly_spend"]
    valid_cols = [c for c in num_cols if c in X_enc.columns]
    if valid_cols and scaler is not None:
        X_enc[valid_cols] = scaler.transform(X_enc[valid_cols])

    # Predict churn probability
    probabilities = model.predict_proba(X_enc)[:, 1]
    df_scored["churn_risk_score"] = probabilities.round(4)

    # Assign risk tier
    conditions = [
        (df_scored["churn_risk_score"] >= 0.70),
        (df_scored["churn_risk_score"] >= 0.40) & (df_scored["churn_risk_score"] < 0.70),
        (df_scored["churn_risk_score"] < 0.40)
    ]
    tiers = ["High Risk", "Medium Risk", "Low Risk"]
    df_scored["risk_tier"] = np.select(conditions, tiers, default="Low Risk")

    # Annualized Revenue
    df_scored["annualized_revenue"] = (df_scored["MonthlyCharges"] * 12.0).round(2)

    return df_scored


def calculate_revenue_at_risk(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Aggregates financial exposure metrics by risk tier.
    """
    tier_summary = df.groupby("risk_tier", observed=False).agg(
        customer_count=("customerID", "count"),
        total_monthly_spend=("MonthlyCharges", "sum"),
        total_annual_revenue=("annualized_revenue", "sum"),
        avg_churn_risk=("churn_risk_score", "mean")
    ).reset_index()

    tier_summary["pct_of_customers"] = (
        tier_summary["customer_count"] * 100.0 / len(df)
    ).round(2)
    tier_summary["pct_of_revenue"] = (
        tier_summary["total_annual_revenue"] * 100.0 / df["annualized_revenue"].sum()
    ).round(2)

    return {
        "summary_table": tier_summary,
        "total_annual_revenue": df["annualized_revenue"].sum(),
        "high_risk_annual_revenue": df[df["risk_tier"] == "High Risk"]["annualized_revenue"].sum()
    }


def export_scored_data(df: pd.DataFrame, filepath: str):
    """
    Exports scored customer dataset to CSV.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
