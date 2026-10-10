"""
src/model_training.py
PwC Technology Consulting - Customer Churn & Revenue Retention Strategy

This module handles train/test splitting, class imbalance handling (SMOTE),
model training (Logistic Regression & Random Forest), evaluation metrics,
and publication-quality visualization generation.
"""

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, Any, List, Optional
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)
from imblearn.over_sampling import SMOTE
from src.data_preprocessing import encode_features, scale_features


def prepare_train_test(
    df: pd.DataFrame, 
    test_size: float = 0.2, 
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, Any, List[str]]:
    """
    Splits dataset into stratified train and test sets, and scales numerical columns.
    """
    X, y, feature_names = encode_features(df)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "total_services_count", "avg_monthly_spend"]
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test, num_cols)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_names


def apply_smote(
    X_train: pd.DataFrame, 
    y_train: pd.Series, 
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Applies Synthetic Minority Over-sampling Technique (SMOTE) to the training set only.
    """
    smote = SMOTE(random_state=random_state)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    return pd.DataFrame(X_train_res, columns=X_train.columns), pd.Series(y_train_res, name=y_train.name)


def train_logistic_regression(
    X_train: pd.DataFrame, 
    y_train: pd.Series, 
    max_iter: int = 1000, 
    random_state: int = 42
) -> LogisticRegression:
    """
    Trains a Logistic Regression classifier for interpretable odds-ratio evaluation.
    """
    model = LogisticRegression(max_iter=max_iter, random_state=random_state)
    model.fit(X_train, y_train)
    return model


def train_random_forest(
    X_train: pd.DataFrame, 
    y_train: pd.Series, 
    n_estimators: int = 200, 
    random_state: int = 42
) -> RandomForestClassifier:
    """
    Trains an ensemble Random Forest classifier capturing non-linear interactions.
    """
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
    """
    Computes comprehensive evaluation metrics on test partition.
    """
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(y_test, y_pred, target_names=["Retained", "Churned"])
    }
    return metrics


def plot_confusion_matrix(
    model: Any, 
    X_test: pd.DataFrame, 
    y_test: pd.Series, 
    title: str = "Confusion Matrix", 
    save_path: Optional[str] = None
):
    """
    Plots and optionally saves a branded confusion matrix heatmap.
    """
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Oranges", cbar=False,
        xticklabels=["Retained (No)", "Churned (Yes)"],
        yticklabels=["Retained (No)", "Churned (Yes)"],
        annot_kws={"size": 14, "weight": "bold"}
    )
    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Predicted Class", fontsize=11, fontweight="bold")
    plt.ylabel("Actual Class", fontsize=11, fontweight="bold")
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    plt.close()


def plot_roc_curve(
    models_dict: Dict[str, Any], 
    X_test: pd.DataFrame, 
    y_test: pd.Series, 
    save_path: Optional[str] = None
):
    """
    Plots comparative ROC Curves across multiple candidate models.
    """
    fig, ax = plt.subplots(figsize=(7, 6))
    colors = ["#D04A02", "#2B6CB0", "#319795"]
    
    for (name, model), color in zip(models_dict.items(), colors):
        y_proba = model.predict_proba(X_test)[:, 1]
        auc_val = roc_auc_score(y_test, y_proba)
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        plt.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})", color=color, linewidth=2.5)

    plt.plot([0, 1], [0, 1], "k--", alpha=0.6, label="Random Benchmark (AUC = 0.500)")
    plt.title("Receiver Operating Characteristic (ROC) Curve", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=11, fontweight="bold")
    plt.ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11, fontweight="bold")
    plt.legend(loc="lower right", frameon=True, fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    plt.close()


def plot_feature_importance(
    model: Any, 
    feature_names: List[str], 
    top_n: int = 15, 
    model_type: str = "rf", 
    save_path: Optional[str] = None
):
    """
    Plots top feature drivers (coefficients for Logistic Regression or MDI importances for Random Forest).
    """
    if model_type == "rf":
        importances = model.feature_importances_
        title = f"Top {top_n} Predictive Drivers of Churn (Random Forest)"
        series = pd.Series(importances, index=feature_names).nlargest(top_n).sort_values(ascending=True)
        color = "#D04A02"
    else:
        importances = model.coef_[0]
        title = f"Top {top_n} Logistic Regression Coefficients"
        series = pd.Series(importances, index=feature_names)
        # Select highest absolute values
        top_indices = series.abs().nlargest(top_n).index
        series = series[top_indices].sort_values(ascending=True)
        color = ["#2B6CB0" if x > 0 else "#718096" for x in series.values]

    fig, ax = plt.subplots(figsize=(9, 6))
    series.plot(kind="barh", color=color, ax=ax)
    plt.title(title, fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Relative Importance / Impact Magnitude", fontsize=11, fontweight="bold")
    plt.ylabel("Engineered Feature", fontsize=11, fontweight="bold")
    plt.grid(axis="x", linestyle=":", alpha=0.6)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    plt.close()
