-- ==============================================================================
-- 02_data_cleaning.sql
-- PwC Technology Consulting - Customer Churn & Revenue Retention Engagement
-- Database: SQLite (data/telco_churn.db)
-- Description: Data cleaning, type transformations, standardization, and normalization.
-- ==============================================================================

-- 1. Integrity Verification: Confirm zero duplicate customer IDs
-- (Expected result: 0 rows returned)
SELECT customerID, COUNT(*) AS occurrences
FROM raw_customers
GROUP BY customerID
HAVING COUNT(*) > 1;

-- 2. Populate normalized `customers` table with standardized SeniorCitizen values
INSERT INTO customers (customerID, gender, SeniorCitizen, Partner, Dependents, tenure)
SELECT 
    customerID,
    gender,
    CASE 
        WHEN SeniorCitizen = 1 THEN 'Yes'
        ELSE 'No'
    END AS SeniorCitizen,
    Partner,
    Dependents,
    CAST(tenure AS INTEGER) AS tenure
FROM raw_customers;

-- 3. Populate normalized `services` table with standardized binary flags
-- Rationale: 'No internet service' and 'No phone service' represent absence of the specific add-on feature.
-- Standardizing to 'No' eliminates redundant cardinality while retaining primary carrier status in PhoneService/InternetService.
INSERT INTO services (
    customerID, 
    PhoneService, 
    MultipleLines, 
    InternetService, 
    OnlineSecurity, 
    OnlineBackup, 
    DeviceProtection, 
    TechSupport, 
    StreamingTV, 
    StreamingMovies
)
SELECT 
    customerID,
    PhoneService,
    CASE WHEN MultipleLines = 'No phone service' THEN 'No' ELSE MultipleLines END AS MultipleLines,
    InternetService,
    CASE WHEN OnlineSecurity = 'No internet service' THEN 'No' ELSE OnlineSecurity END AS OnlineSecurity,
    CASE WHEN OnlineBackup = 'No internet service' THEN 'No' ELSE OnlineBackup END AS OnlineBackup,
    CASE WHEN DeviceProtection = 'No internet service' THEN 'No' ELSE DeviceProtection END AS DeviceProtection,
    CASE WHEN TechSupport = 'No internet service' THEN 'No' ELSE TechSupport END AS TechSupport,
    CASE WHEN StreamingTV = 'No internet service' THEN 'No' ELSE StreamingTV END AS StreamingTV,
    CASE WHEN StreamingMovies = 'No internet service' THEN 'No' ELSE StreamingMovies END AS StreamingMovies
FROM raw_customers;

-- 4. Populate normalized `billing` table handling empty TotalCharges strings
-- Rationale: The 11 customers with blank TotalCharges have tenure = 0 (brand-new accounts).
-- Setting TotalCharges = 0.0 accurately reflects zero historical billing rather than dropping rows.
INSERT INTO billing (
    customerID,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    TotalCharges
)
SELECT 
    customerID,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    CAST(MonthlyCharges AS REAL) AS MonthlyCharges,
    CASE 
        WHEN TRIM(TotalCharges) = '' OR TotalCharges IS NULL THEN 0.0
        ELSE CAST(TotalCharges AS REAL)
    END AS TotalCharges
FROM raw_customers;

-- 5. Populate normalized `churn_status` table
INSERT INTO churn_status (customerID, Churn)
SELECT 
    customerID,
    Churn
FROM raw_customers;

-- 6. Verification counts across all relational tables (should all match raw count of 7,043)
SELECT 'raw_customers' AS table_name, COUNT(*) AS record_count FROM raw_customers
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'services', COUNT(*) FROM services
UNION ALL
SELECT 'billing', COUNT(*) FROM billing
UNION ALL
SELECT 'churn_status', COUNT(*) FROM churn_status;
