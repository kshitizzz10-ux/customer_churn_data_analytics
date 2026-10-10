"""
src/data_preprocessing.py
PwC Technology Consulting - Customer Churn & Revenue Retention Strategy

This module provides enterprise-grade data loading, cleaning, validation,
and feature encoding capabilities for customer churn analytics.
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
from sklearn.preprocessing import StandardScaler


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Loads raw customer data from a CSV file.

    Parameters:
        filepath (str): File system path to the raw dataset CSV.

    Returns:
        pd.DataFrame: Loaded raw dataset.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw data file not found at: {filepath}")
    df = pd.read_csv(filepath)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw customer records:
    1. Handles blank strings in TotalCharges (imputing 0.0 for 0-tenure accounts).
    2. Converts TotalCharges to numeric float.
    3. Standardizes SeniorCitizen binary indicators to 'Yes'/'No'.
    4. Standardizes 'No internet service' and 'No phone service' to 'No' for add-on features.
    5. Strips redundant whitespace and validates uniqueness of customerID.

    Parameters:
        df (pd.DataFrame): Raw DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df_clean = df.copy()

    # Handle blank strings in TotalCharges
    if "TotalCharges" in df_clean.columns:
        df_clean["TotalCharges"] = df_clean["TotalCharges"].replace(r"^\s*$", np.nan, regex=True)
        # Tenure 0 customers have TotalCharges NaN -> impute 0.0
        df_clean["TotalCharges"] = df_clean["TotalCharges"].fillna(0.0).astype(float)

    # Standardize SeniorCitizen
    if "SeniorCitizen" in df_clean.columns:
        df_clean["SeniorCitizen"] = df_clean["SeniorCitizen"].map({1: "Yes", 0: "No"}).fillna("No")

    # Standardize secondary service values
    service_cols = [
        "MultipleLines", "OnlineSecurity", "OnlineBackup", 
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    for col in service_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].replace({
                "No internet service": "No",
                "No phone service": "No"
            })

    # Validate customerID duplicates
    if "customerID" in df_clean.columns:
        df_clean = df_clean.drop_duplicates(subset=["customerID"])

    return df_clean


def encode_features(
    df: pd.DataFrame, 
    drop_first: bool = True
) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """
    Prepares features for predictive modeling:
    - Target 'Churn' is mapped to binary 1 (Yes) / 0 (No).
    - Binary categorical variables are mapped to 1/0.
    - Multi-class categorical variables are one-hot encoded.
    - Non-predictive identifiers like 'customerID' and raw target are separated.

    Parameters:
        df (pd.DataFrame): Cleaned and feature-engineered DataFrame.
        drop_first (bool): Whether to drop first dummy category to prevent multicollinearity.

    Returns:
        Tuple[pd.DataFrame, pd.Series, List[str]]:
            - X: Encoded feature matrix.
            - y: Binary target series.
            - feature_names: List of resulting column names in X.
    """
    df_encoded = df.copy()

    # Extract target
    if "Churn" in df_encoded.columns:
        y = df_encoded["Churn"].map({"Yes": 1, "No": 0})
    else:
        y = None

    # Exclude non-feature columns
    cols_to_drop = [col for col in ["customerID", "Churn", "annualized_revenue"] if col in df_encoded.columns]
    df_features = df_encoded.drop(columns=cols_to_drop)

    # Binary columns mapping
    binary_cols = ["gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService", 
                   "MultipleLines", "OnlineSecurity", "OnlineBackup", "DeviceProtection", 
                   "TechSupport", "StreamingTV", "StreamingMovies", "PaperlessBilling", 
                   "has_premium_bundle"]
    
    for col in binary_cols:
        if col in df_features.columns:
            if set(df_features[col].dropna().unique()).issubset({"Yes", "No"}):
                df_features[col] = df_features[col].map({"Yes": 1, "No": 0})
            elif col == "gender":
                df_features[col] = df_features[col].map({"Female": 1, "Male": 0})

    # One-hot encode remaining categorical variables
    categorical_cols = df_features.select_dtypes(include=["object", "category"]).columns.tolist()
    if categorical_cols:
        df_features = pd.get_dummies(df_features, columns=categorical_cols, drop_first=drop_first, dtype=int)

    feature_names = df_features.columns.tolist()
    return df_features, y, feature_names


def scale_features(
    X_train: pd.DataFrame, 
    X_test: pd.DataFrame, 
    numerical_cols: List[str]
) -> Tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    Fits a StandardScaler on training numerical columns and transforms train and test sets.

    Parameters:
        X_train (pd.DataFrame): Training feature matrix.
        X_test (pd.DataFrame): Testing feature matrix.
        numerical_cols (List[str]): Numerical columns to scale.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
            - X_train_scaled
            - X_test_scaled
            - scaler
    """
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    valid_cols = [col for col in numerical_cols if col in X_train.columns]
    if valid_cols:
        X_train_scaled[valid_cols] = scaler.fit_transform(X_train[valid_cols])
        X_test_scaled[valid_cols] = scaler.transform(X_test[valid_cols])

    return X_train_scaled, X_test_scaled, scaler
