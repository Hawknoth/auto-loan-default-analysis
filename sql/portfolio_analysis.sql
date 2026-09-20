-- Auto Loan Portfolio: Default & Risk Analysis
-- Compatible with SQLite after importing train.csv as vehicle_loans.

-- 1. Portfolio overview
SELECT
    COUNT(*) AS total_loans,
    ROUND(SUM(disbursed_amount), 2) AS total_disbursed,
    ROUND(AVG(disbursed_amount), 2) AS average_loan_amount,
    ROUND(AVG(ltv), 2) AS average_ltv,
    ROUND(100.0 * AVG(loan_default), 2) AS default_rate_pct
FROM vehicle_loans;

-- 2. Default rate by LTV band
WITH segmented AS (
    SELECT *,
        CASE
            WHEN ltv <= 60 THEN '<=60%'
            WHEN ltv <= 70 THEN '60-70%'
            WHEN ltv <= 80 THEN '70-80%'
            WHEN ltv <= 90 THEN '80-90%'
            ELSE '>90%'
        END AS ltv_band
    FROM vehicle_loans
)
SELECT
    ltv_band,
    COUNT(*) AS loans,
    ROUND(AVG(ltv), 2) AS average_ltv,
    ROUND(100.0 * AVG(loan_default), 2) AS default_rate_pct
FROM segmented
GROUP BY ltv_band
ORDER BY default_rate_pct DESC;

-- 3. Prior delinquency and default
SELECT
    CASE WHEN delinquent_accts_in_last_six_months > 0 THEN 'Yes' ELSE 'No' END AS prior_delinquency,
    COUNT(*) AS loans,
    ROUND(100.0 * AVG(loan_default), 2) AS default_rate_pct
FROM vehicle_loans
GROUP BY prior_delinquency;

-- 4. Credit score risk segments
SELECT
    CASE
        WHEN perform_cns_score = 0 THEN 'No score'
        WHEN perform_cns_score <= 300 THEN '1-300'
        WHEN perform_cns_score <= 600 THEN '301-600'
        WHEN perform_cns_score <= 750 THEN '601-750'
        ELSE '751-900'
    END AS score_band,
    COUNT(*) AS loans,
    ROUND(100.0 * AVG(loan_default), 2) AS default_rate_pct
FROM vehicle_loans
GROUP BY score_band
ORDER BY default_rate_pct DESC;

-- 5. States requiring closer portfolio monitoring
SELECT
    state_id,
    COUNT(*) AS loans,
    ROUND(SUM(disbursed_amount), 2) AS disbursed_amount,
    ROUND(100.0 * AVG(loan_default), 2) AS default_rate_pct
FROM vehicle_loans
GROUP BY state_id
HAVING COUNT(*) >= 1000
ORDER BY default_rate_pct DESC;

