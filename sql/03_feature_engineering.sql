-- ==============================================================================
-- 03_feature_engineering.sql
-- PwC Technology Consulting - Customer Churn & Revenue Retention Engagement
-- Database: SQLite (data/telco_churn.db)
-- Description: Relational joins and creation of the `cleaned_customers` table/view
--              incorporating strategic business features.
-- ==============================================================================

DROP VIEW IF EXISTS v_cleaned_customers;
DROP TABLE IF EXISTS cleaned_customers;

CREATE TABLE cleaned_customers AS
SELECT 
    -- 1. Base Demographics
    c.customerID,
    c.gender,
    c.SeniorCitizen,
    c.Partner,
    c.Dependents,
    c.tenure,

    -- 2. Service Subscriptions
    s.PhoneService,
    s.MultipleLines,
    s.InternetService,
    s.OnlineSecurity,
    s.OnlineBackup,
    s.DeviceProtection,
    s.TechSupport,
    s.StreamingTV,
    s.StreamingMovies,

    -- 3. Billing & Financials
    b.Contract,
    b.PaperlessBilling,
    b.PaymentMethod,
    b.MonthlyCharges,
    b.TotalCharges,

    -- 4. Target Variable
    cs.Churn,

    -- 5. Engineered Feature 1: Tenure Group Segment
    CASE 
        WHEN c.tenure <= 12 THEN '0-12'
        WHEN c.tenure <= 24 THEN '13-24'
        WHEN c.tenure <= 36 THEN '25-36'
        WHEN c.tenure <= 48 THEN '37-48'
        WHEN c.tenure <= 60 THEN '49-60'
        ELSE '61-72'
    END AS tenure_group,

    -- 6. Engineered Feature 2: Monthly Spend Tier
    CASE 
        WHEN b.MonthlyCharges < 35.0 THEN 'Low'
        WHEN b.MonthlyCharges <= 70.0 THEN 'Medium'
        ELSE 'High'
    END AS monthly_charge_tier,

    -- 7. Engineered Feature 3: Total Value-Add Services Count (0 to 6)
    (
        (CASE WHEN s.OnlineSecurity = 'Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN s.OnlineBackup = 'Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN s.DeviceProtection = 'Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN s.TechSupport = 'Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN s.StreamingTV = 'Yes' THEN 1 ELSE 0 END) +
        (CASE WHEN s.StreamingMovies = 'Yes' THEN 1 ELSE 0 END)
    ) AS total_services_count,

    -- 8. Engineered Feature 4: Historical Average Monthly Spend
    ROUND(
        CASE 
            WHEN c.tenure = 0 THEN b.MonthlyCharges
            ELSE b.TotalCharges / c.tenure
        END, 2
    ) AS avg_monthly_spend,

    -- 9. Engineered Feature 5: Premium Value-Add Bundle Adoption
    CASE 
        WHEN (
            (CASE WHEN s.OnlineSecurity = 'Yes' THEN 1 ELSE 0 END) +
            (CASE WHEN s.OnlineBackup = 'Yes' THEN 1 ELSE 0 END) +
            (CASE WHEN s.DeviceProtection = 'Yes' THEN 1 ELSE 0 END) +
            (CASE WHEN s.TechSupport = 'Yes' THEN 1 ELSE 0 END) +
            (CASE WHEN s.StreamingTV = 'Yes' THEN 1 ELSE 0 END) +
            (CASE WHEN s.StreamingMovies = 'Yes' THEN 1 ELSE 0 END)
        ) >= 3 THEN 'Yes'
        ELSE 'No'
    END AS has_premium_bundle,

    -- 10. Annualized Revenue (MonthlyCharges * 12)
    ROUND(b.MonthlyCharges * 12.0, 2) AS annualized_revenue

FROM customers c
INNER JOIN services s ON c.customerID = s.customerID
INNER JOIN billing b ON c.customerID = b.customerID
INNER JOIN churn_status cs ON c.customerID = cs.customerID;

-- Create an indexed view on cleaned_customers for high-performance reporting
CREATE VIEW v_cleaned_customers AS
SELECT * FROM cleaned_customers;
