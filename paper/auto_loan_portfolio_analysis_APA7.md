# Default and Risk Analysis of an Auto Loan Portfolio

**Author:** Adrian  
**Affiliation:** Professional Data Analytics Portfolio  
**Date:** September 20, 2026

## Abstract

This project examines 233,154 auto loans to identify portfolio segments that require closer monitoring from a loan servicing and collections perspective. The overall default rate was 21.7%. Loans with an LTV between 80% and 90% reached 25.9%, customers with recent delinquency reached 27.1%, and the 301-600 credit-score group also recorded 27.1%. The analysis is descriptive because the dataset does not contain monthly payment history, days past due, cure rate, roll rate, charge-off events, or total-loss events.

*Keywords: auto loans, default, loan servicing, collections, business intelligence*

## Method

The analysis uses the *Vehicle Loan Default Prediction* dataset published on Kaggle (Paul, n.d.). The file contains 233,154 records and 41 fields. Columns were standardized and new segments were created for LTV, credit score, and recent delinquency. Python and SQL were used to calculate loan volume, disbursed amount, average LTV, and default rate.

## Results

| Segment | Loans | Default rate | Difference from portfolio |
|---|---:|---:|---:|
| Full portfolio | 233,154 | 21.7% | Baseline |
| 80%-90% LTV | 81,005 | 25.9% | +4.2 pp |
| Recent delinquency | 18,195 | 27.1% | +5.4 pp |
| 301-600 credit score | 18,716 | 27.1% | +5.4 pp |
| 751-900 credit score | 25,682 | 14.7% | -7.0 pp |
| State 13 | 17,884 | 30.7% | +9.0 pp |

### Loan to Value Ratio

Default increased from 13.9% among loans at or below 60% LTV to 25.9% in the 80%-90% band. The segment above 90% recorded 20.6%, but it contains only 883 loans. The 80%-90% band is more operationally relevant because it combines an elevated rate with 81,005 accounts.

### Credit Score

Customers scoring 301-600 recorded 27.1% default, compared with 14.7% among customers scoring 751-900. The no-score group contains 116,950 loans and recorded 23.1%, so it should not be treated only as missing data.

### Recent Delinquency

Customers with at least one delinquent account during the previous six months recorded 27.1% default, compared with 21.3% among customers without recent delinquency.

### Geographic Distribution

Among states with at least 1,000 loans, State 13 recorded the highest default rate at 30.7% across 17,884 accounts. This does not establish causation, but it identifies a concentration that deserves further review.

![Portfolio dashboard](../reports/figures/portfolio_dashboard.png)

## Discussion

An early-review queue could consider accounts that combine 80%-90% LTV, recent delinquency, and low or mid-range credit scores. A production analysis would require monthly payment and contact history to calculate roll rates, cure rate, promises to pay, recoveries, and movement toward charge-off.

## Limitations

The dataset does not include days past due, partial payments, customer contacts, repossession, total loss, recovered balances, or charge-off dates. It also does not identify the currency or provide state names. The findings represent associations within this portfolio, not causal relationships.

## Conclusion

The project identifies three practical monitoring signals and documents them at an appropriate level for an intermediate business intelligence portfolio. The repository includes the data source, processing steps, SQL queries, aggregated tables, dashboard, findings, and limitations.

## References

Paul, A. (n.d.). *Vehicle loan default prediction* [Data set]. Kaggle. https://www.kaggle.com/datasets/avikpaul4u/vehicle-loan-default-prediction
