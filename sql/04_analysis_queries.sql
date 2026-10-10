-- ==============================================================================
-- 04_analysis_queries.sql
-- PwC Technology Consulting - Customer Churn & Revenue Retention Engagement
-- Database: SQLite (data/telco_churn.db)
-- Description: Core analytical queries directly addressing client objectives
--              and powering the executive reporting deliverables.
-- ==============================================================================

-- Query 1: Overall Churn Rate and Portfolio KPI Summary
SELECT 
    COUNT(*) AS total_customer_base,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_at_risk,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
FROM cleaned_customers;

-- Query 2: Churn Distribution and Rate by Contract Type
SELECT 
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / (SELECT COUNT(*) FROM cleaned_customers WHERE Churn = 'Yes'), 2) AS pct_of_total_churn
FROM cleaned_customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- Query 3: Churn Rate by Internet Service Architecture
SELECT 
    InternetService,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_bill,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
FROM cleaned_customers
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;

-- Query 4: Customer Lifecycle & Tenure Dynamics
SELECT 
    Churn,
    COUNT(*) AS customer_count,
    ROUND(AVG(tenure), 1) AS avg_tenure_months,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(TotalCharges), 2) AS avg_lifetime_spend
FROM cleaned_customers
GROUP BY Churn;

-- Query 5: Tenure Cohort Breakdown (0-12m Onboarding Vulnerability)
SELECT 
    tenure_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
FROM cleaned_customers
GROUP BY tenure_group
ORDER BY tenure_group ASC;

-- Query 6: Payment Channel Friction Analysis
SELECT 
    PaymentMethod,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
FROM cleaned_customers
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;

-- Query 7: Service Ecosystem Depth vs. Churn Rate
SELECT 
    total_services_count,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
FROM cleaned_customers
GROUP BY total_services_count
ORDER BY total_services_count ASC;

-- Query 8: Senior Citizen Demographic Risk Profile
SELECT 
    SeniorCitizen,
    Partner,
    Dependents,
    COUNT(*) AS total_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN annualized_revenue ELSE 0 END), 2) AS annual_revenue_at_risk
FROM cleaned_customers
GROUP BY SeniorCitizen, Partner, Dependents
ORDER BY churn_rate_pct DESC;

-- Query 9: Top 10 Highest-Value Lost Customers (Executive Loss Audit)
SELECT 
    customerID,
    gender,
    SeniorCitizen,
    Contract,
    tenure,
    InternetService,
    PaymentMethod,
    MonthlyCharges,
    annualized_revenue,
    TotalCharges
FROM cleaned_customers
WHERE Churn = 'Yes'
ORDER BY MonthlyCharges DESC
LIMIT 10;
