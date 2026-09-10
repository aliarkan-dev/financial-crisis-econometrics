import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import VAR


def load_and_preprocess_data(filepath):
    """
    Load foreign exchange rate data, handle missing values from market holidays,
    and calculate daily log returns.

    Parameters
    ----------
    filepath : str
        Path to the CSV dataset.

    Returns
    -------
    pandas.DataFrame
        Daily log returns for stationary VAR modeling.
    """
    df = pd.read_csv(
        filepath,
        parse_dates=["Date"],
        index_col="Date"
    )

    # Ensure chronological sorting
    df = df.sort_index()

    # Forward-fill missing values due to non-overlapping financial holidays
    df = df.ffill()

    # Validate exchange-rate values
    if (df <= 0).any().any():
        raise ValueError(
            "Exchange-rate data must contain strictly positive values."
        )

    # Calculate daily log returns
    log_returns = np.log(df / df.shift(1))

    # Drop the first row created by lag differencing
    log_returns = log_returns.dropna()

    return log_returns


def test_stationarity(df):
    """
    Run the Augmented Dickey-Fuller test for each currency pair log-return.
    """
    results = []

    for column in df.columns:
        series = df[column].dropna()
        adf_result = adfuller(series, autolag="AIC")

        results.append({
            "Currency Pair": column,
            "ADF Statistic": adf_result[0],
            "p-value": adf_result[1],
            "Used Lags": adf_result[2],
            "Observations": adf_result[3],
            "Stationary": adf_result[1] < 0.05
        })

    results_df = pd.DataFrame(results)

    print("\n--- Augmented Dickey-Fuller (ADF) Stationarity Test ---")
    print(results_df.to_string(index=False))

    return results_df


def estimate_var_model(df, maxlags=5):
    """
    Estimate a VAR model and select the optimal lag order
    using the Akaike Information Criterion (AIC).
    """
    model = VAR(df)

    results = model.fit(
        maxlags=maxlags,
        ic="aic"
    )

    print("\n--- Vector Autoregression (VAR) Model Summary ---")
    print(results.summary())

    return results


if __name__ == "__main__":
    data_path = "../data/exchange_rates.csv"

    try:
        data = load_and_preprocess_data(data_path)

        print("Dataset successfully loaded and preprocessed.")
        print(f"Observations: {len(data)}")
        print(f"Variables: {len(data.columns)}")

        stationarity_results = test_stationarity(data)
        model_results = estimate_var_model(data)

    except FileNotFoundError:
        print(
            f"Error: Dataset not found at '{data_path}'. "
            "Please verify the repository directory structure."
        )

    except ValueError as error:
        print(f"Data validation error: {error}")
