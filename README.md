# Exchange Rate Spillovers during the 2007–2008 Global Financial Crisis: An Applied Econometric Analysis

## Executive Summary
This repository presents an applied econometric framework for quantifying foreign 
exchange rate spillovers and volatility transmission during the 2007–2008 Global 
Financial Crisis. Using a Vector Autoregression (VAR) framework combined with 
GARCH-family volatility models, the project evaluates how systemic liquidity 
stress in major money markets propagated across international currency markets, 
and assesses the role of central bank interventions in mitigating this transmission.

## Key Research Questions
1. How did liquidity stress in major money markets transmit to foreign exchange 
   volatility between 2007 and 2008?
2. To what extent did central bank interest rate interventions (Federal Reserve, 
   ECB, Bank of England, and Bank of Japan) statistically dampen cross-market 
   currency volatility during the crisis window?

## Data
- **Currency Pairs:** EUR/USD, GBP/USD, JPY/USD — all expressed as the price of 
  USD in terms of the foreign currency, ensuring a consistent directional 
  interpretation (a positive return indicates USD appreciation) across the VAR 
  system. Series are transformed into log-returns to achieve stationarity.
- **Frequency:** Daily
- **Sample Period:** January 2006 – December 2009 (covering pre-crisis, acute 
  crisis, and post-crisis windows)
- **Sources:** Federal Reserve Economic Data (FRED); ECB Statistical Data 
  Warehouse (for policy rate series)

## Methodology
1. **Stationarity Testing:** Augmented Dickey-Fuller (ADF) and Phillips-Perron 
   (PP) tests to determine the order of integration of each series.
2. **Cointegration Analysis:** Johansen cointegration test to assess long-run 
   equilibrium relationships between currency pairs (where applicable).
3. **VAR / VECM Modeling:** Vector Autoregression (or Vector Error Correction 
   Model, if cointegration is confirmed) to capture bidirectional dynamic 
   linkages between exchange rate series.
4. **Volatility Modeling:** DCC-GARCH to estimate time-varying volatility and 
   conditional correlations across currency pairs, capturing short-run dynamic 
   co-movement in daily volatility.
5. **Spillover Quantification:** Diebold-Yilmaz spillover index to measure the 
   aggregate magnitude and net direction of volatility transmission across 
   markets, complementing the DCC-GARCH results with a comparable summary 
   measure across sub-periods.
6. **Structural Break Analysis:** Bai-Perron and Chow tests to identify 
   statistically significant breakpoints coinciding with key crisis events 
   (e.g., Lehman Brothers collapse on September 15, 2008).
7. **Event Study:** Dummy-variable regression around central bank intervention 
   dates (Fed, ECB, BoE, and BoJ rate decisions, including the coordinated 
   rate cuts of October 8, 2008) to assess statistical significance of policy 
   responses on volatility.
8. **Robustness Checks:** Sub-sample analysis (pre-crisis vs. crisis window) 
   and alternative lag-length specifications.

## Repository Structure
```text
├── data/              # Raw and processed daily exchange rate datasets (FRED)
├── figures/           # Impulse response plots, spillover indices, and break charts
├── scripts/           # Python scripts for VAR, DCC-GARCH, and Diebold-Yilmaz models
└── README.md          # Comprehensive econometric report
```
