import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Page title
st.title("Predictive Performance")

# Simulated Data
np.random.seed(42)
num_coins = 500
num_periods = 60  # Monthly data for 5 years
data = pd.DataFrame({
    "coin_id": np.repeat([f"coin_{i}" for i in range(1, num_coins + 1)], num_periods),
    "date": pd.date_range("2015-01-01", periods=num_periods, freq="M").tolist() * num_coins,
    "signal": np.random.rand(num_coins * num_periods),
    "return": np.random.randn(num_coins * num_periods) / 100,
    "market_cap": np.random.randint(10, 1000, num_coins * num_periods)
})

# User choice for weighting scheme
st.subheader("Portfolio Weighting Scheme")
weighting_scheme = st.radio(
    "Select Weighting Scheme",
    options=["Market Cap Weighted", "Equal Weighted"],
    index=0
)

# Assign weights based on the chosen scheme
if weighting_scheme == "Market Cap Weighted":
    data["weight"] = data["market_cap"]
else:
    data["weight"] = 1

# Portfolio construction
num_portfolios = 5  # Quintile sort
data["portfolio"] = data.groupby("date")["signal"].transform(
    lambda x: pd.qcut(x, q=num_portfolios, labels=["L", "2", "3", "4", "H"], duplicates="drop")
)

# Portfolio returns
portfolio_returns = (
    data.groupby(["date", "portfolio"])
    .apply(lambda x: np.average(x["return"], weights=x["weight"]))
    .unstack()
)

# Calculate Long-Short Portfolio (H-L)
portfolio_returns["H-L"] = portfolio_returns["H"] - portfolio_returns["L"]

# Factor Models (simulated for demonstration)
factors = pd.DataFrame({
    "CMKT": np.random.randn(num_periods),  # Market factor
    "CSMB": np.random.randn(num_periods),  # Size factor
    "CMOM": np.random.randn(num_periods),  # Momentum factor
    "date": pd.date_range("2015-01-01", periods=num_periods, freq="M")
}).set_index("date")

# Merge factors with portfolio returns
portfolio_returns = portfolio_returns.join(factors, how="inner")

# Regression function
def run_regression(portfolio, factors):
    X = sm.add_constant(factors[["CMKT", "CSMB", "CMOM"]])
    y = portfolio
    reg = sm.OLS(y, X).fit()
    return reg.params, reg.tvalues

# Run regressions for all portfolios
results = {}
for col in portfolio_returns.columns[:5]:  # Exclude factors and H-L for now
    params, tvals = run_regression(portfolio_returns[col], portfolio_returns[["CMKT", "CSMB", "CMOM"]])
    results[col] = {"params": params, "tvals": tvals}

# Run regression for Long-Short portfolio (H-L)
params, tvals = run_regression(portfolio_returns["H-L"], portfolio_returns[["CMKT", "CSMB", "CMOM"]])
results["H-L"] = {"params": params, "tvals": tvals}

# Panel A: Excess Returns and Alphas
st.subheader("Panel A: Excess Returns and Alphas")
panel_a_data = {
    "Metric": ["Excess Return", "t(Excess Return)", "Alpha (CMKT)", "t(Alpha)"],
    "L": [
        portfolio_returns["L"].mean(),
        portfolio_returns["L"].mean() / portfolio_returns["L"].std(),
        results["L"]["params"]["const"],
        results["L"]["tvals"]["const"],
    ],
    "2": [
        portfolio_returns["2"].mean(),
        portfolio_returns["2"].mean() / portfolio_returns["2"].std(),
        results["2"]["params"]["const"],
        results["2"]["tvals"]["const"],
    ],
    "3": [
        portfolio_returns["3"].mean(),
        portfolio_returns["3"].mean() / portfolio_returns["3"].std(),
        results["3"]["params"]["const"],
        results["3"]["tvals"]["const"],
    ],
    "4": [
        portfolio_returns["4"].mean(),
        portfolio_returns["4"].mean() / portfolio_returns["4"].std(),
        results["4"]["params"]["const"],
        results["4"]["tvals"]["const"],
    ],
    "H": [
        portfolio_returns["H"].mean(),
        portfolio_returns["H"].mean() / portfolio_returns["H"].std(),
        results["H"]["params"]["const"],
        results["H"]["tvals"]["const"],
    ],
    "H-L": [
        portfolio_returns["H-L"].mean(),
        portfolio_returns["H-L"].mean() / portfolio_returns["H-L"].std(),
        results["H-L"]["params"]["const"],
        results["H-L"]["tvals"]["const"],
    ],
}
panel_a = pd.DataFrame(panel_a_data)
st.table(panel_a)

# Panel B: Factor Loadings
st.subheader("Panel B: Factor Loadings")
panel_b_data = {
    "Metric": ["βCMKT", "t(βCMKT)", "βCSMB", "t(βCSMB)", "βCMOM", "t(βCMOM)"],
    "L": [
        results["L"]["params"]["CMKT"],
        results["L"]["tvals"]["CMKT"],
        results["L"]["params"]["CSMB"],
        results["L"]["tvals"]["CSMB"],
        results["L"]["params"]["CMOM"],
        results["L"]["tvals"]["CMOM"],
    ],
    "2": [
        results["2"]["params"]["CMKT"],
        results["2"]["tvals"]["CMKT"],
        results["2"]["params"]["CSMB"],
        results["2"]["tvals"]["CSMB"],
        results["2"]["params"]["CMOM"],
        results["2"]["tvals"]["CMOM"],
    ],
    "3": [
        results["3"]["params"]["CMKT"],
        results["3"]["tvals"]["CMKT"],
        results["3"]["params"]["CSMB"],
        results["3"]["tvals"]["CSMB"],
        results["3"]["params"]["CMOM"],
        results["3"]["tvals"]["CMOM"],
    ],
    "4": [
        results["4"]["params"]["CMKT"],
        results["4"]["tvals"]["CMKT"],
        results["4"]["params"]["CSMB"],
        results["4"]["tvals"]["CSMB"],
        results["4"]["params"]["CMOM"],
        results["4"]["tvals"]["CMOM"],
    ],
    "H": [
        results["H"]["params"]["CMKT"],
        results["H"]["tvals"]["CMKT"],
        results["H"]["params"]["CSMB"],
        results["H"]["tvals"]["CSMB"],
        results["H"]["params"]["CMOM"],
        results["H"]["tvals"]["CMOM"],
    ],
    "H-L": [
        results["H-L"]["params"]["CMKT"],
        results["H-L"]["tvals"]["CMKT"],
        results["H-L"]["params"]["CSMB"],
        results["H-L"]["tvals"]["CSMB"],
        results["H-L"]["params"]["CMOM"],
        results["H-L"]["tvals"]["CMOM"],
    ],
}
panel_b = pd.DataFrame(panel_b_data)
st.table(panel_b)

# Notes
st.markdown("""
**Notes:**
1. Excess returns and alphas are based on monthly portfolio data.
2. Factor models include CMKT (Market), CSMB (Size), and CMOM (Momentum).
3. T-statistics are shown in brackets.
""")
