import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR


def generate_irf_plot(data_path, output_path):
    """
    Fits a VAR model on FX log-returns and generates Impulse Response Functions (IRFs).
    Saves the output visualization to the figures directory.
    """
    # 1. Load data and compute log-returns
    df = pd.read_csv(data_path, parse_dates=['Date'], index_col='Date').sort_index().ffill()
    log_returns = np.log(df / df.shift(1)).dropna()

    # 2. Fit VAR model
    model = VAR(log_returns)
    results = model.fit(maxlags=2, ic='aic')

    # 3. Compute Impulse Response Functions (10-period horizon)
    irf = results.irf(periods=10)

    # 4. Plot IRF
    fig = irf.plot(ortho=True)
    fig.suptitle('Impulse Response Functions (Structural Shocks)', fontsize=12, y=1.02)
    plt.tight_layout()

    # 5. Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"IRF plot successfully generated and saved to: {output_path}")


if __name__ == "__main__":
    generate_irf_plot('../data/exchange_rates.csv', '../figures/irf_plot.png')
