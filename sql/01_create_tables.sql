-- ==============================================================================
-- 01_create_tables.sql
-- PwC Technology Consulting - Customer Churn & Revenue Retention Engagement
-- Database: SQLite (data/telco_churn.db)
-- Description: Raw data table definitions and normalized relational schema.
-- ==============================================================================

-- 1. Drop existing tables if re-running migration
DROP TABLE IF EXISTS raw_customers;
DROP TABLE IF EXISTS churn_status;
DROP TABLE IF EXISTS billing;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS customers;

-- 2. Raw staging table matching CSV schema exactly
CREATE TABLE raw_customers (
    customerID TEXT PRIMARY KEY,
    gender TEXT,
    SeniorCitizen INTEGER,
    Partner TEXT,
    Dependents TEXT,
    tenure INTEGER,
    PhoneService TEXT,
    MultipleLines TEXT,
    InternetService TEXT,
    OnlineSecurity TEXT,
    OnlineBackup TEXT,
    DeviceProtection TEXT,
    TechSupport TEXT,
    StreamingTV TEXT,
    StreamingMovies TEXT,
    Contract TEXT,
    PaperlessBilling TEXT,
    PaymentMethod TEXT,
    MonthlyCharges REAL,
    TotalCharges TEXT,  -- Retained as TEXT initially because raw data contains empty whitespace strings (' ')
    Churn TEXT
);

-- 3. Normalized relational schema to demonstrate Enterprise SQL architecture

-- Table: Demographics & Account Lifespan
CREATE TABLE customers (
    customerID TEXT PRIMARY KEY,
    gender TEXT,
    SeniorCitizen TEXT,  -- Standardized to 'Yes'/'No'
    Partner TEXT,
    Dependents TEXT,
    tenure INTEGER
);

-- Table: Subscribed Services & Digital Add-ons
CREATE TABLE services (
    customerID TEXT PRIMARY KEY,
    PhoneService TEXT,
    MultipleLines TEXT,
    InternetService TEXT,
    OnlineSecurity TEXT,
    OnlineBackup TEXT,
    DeviceProtection TEXT,
    TechSupport TEXT,
    StreamingTV TEXT,
    StreamingMovies TEXT,
    FOREIGN KEY (customerID) REFERENCES customers(customerID)
);

-- Table: Contractual & Financial Billing Records
CREATE TABLE billing (
    customerID TEXT PRIMARY KEY,
    Contract TEXT,
    PaperlessBilling TEXT,
    PaymentMethod TEXT,
    MonthlyCharges REAL,
    TotalCharges REAL,
    FOREIGN KEY (customerID) REFERENCES customers(customerID)
);

-- Table: Churn Target Label
CREATE TABLE churn_status (
    customerID TEXT PRIMARY KEY,
    Churn TEXT,
    FOREIGN KEY (customerID) REFERENCES customers(customerID)
);
