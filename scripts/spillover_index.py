import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR


def compute_diebold_yilmaz_spillover(data_path, n_ahead=10):
    """
    Computes a simplified Diebold-Yilmaz Volatility Spillover Index
    based on Variance Decomposition from a fitted VAR model.
    """
    # 1. Load data and compute log-returns
    df = pd.read_csv(data_path, parse_dates=['Date'], index_col='Date').sort_index().ffill()
    log_returns = np.log(df / df.shift(1)).dropna()

    # 2. Fit VAR model
    model = VAR(log_returns)
    results = model.fit(maxlags=2, ic='aic')

    # 3. Forecast Error Variance Decomposition (FEVD)
    fevd = results.fevd(periods=n_ahead)
    fevd_matrices = fevd.decomp

    # Extract final horizon variance decomposition matrix
    vd_matrix = fevd_matrices[-1] * 100  # Convert to percentage

    # Normalize rows to sum to 100%
    vd_matrix = vd_matrix / vd_matrix.sum(axis=1)[:, np.newaxis] * 100

    # Build Spillover Table
    cols = log_returns.columns
    spillover_df = pd.DataFrame(vd_matrix, index=cols, columns=cols)

    # Calculate Directional Spillovers
    spillover_df['From Others'] = 100 - np.diag(spillover_df.values)

    # Compute Total Spillover Index
    total_spillover = spillover_df['From Others'].sum() / len(cols)

    print("\n--- Diebold-Yilmaz Volatility Spillover Table (%) ---")
    print(spillover_df.round(2))
    print(f"\nTotal Volatility Spillover Index: {total_spillover:.2f}%")

    return spillover_df, total_spillover


if __name__ == "__main__":
    try:
        compute_diebold_yilmaz_spillover('../data/exchange_rates.csv')
    except Exception as e:
        print(f"Execution Error: {e}")
