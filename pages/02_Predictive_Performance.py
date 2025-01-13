import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

st.title("Predictive Performance")

# Retrieve signal from session state
if "signal_type" in st.session_state:
    signal_type = st.session_state["signal_type"]
    st.write(f"Analyzing predictive performance based on the selected signal: **{signal_type}**")
else:
    st.error("No signal selected! Please go back to Step 1.")
    st.stop()

# Simulated Data Generation (for demonstration)
np.random.seed(42)
num_coins = 500
num_periods = 60  # Simulating monthly data for 5 years
data = pd.DataFrame({
    "coin_id": np.repeat([f"coin_{i}" for i in range(1, num_coins + 1)], num_periods),
    "date": pd.date_range("2015-01-01", periods=num_periods, freq="M").tolist() * num_coins,
    "signal": np.random.rand(num_coins * num_periods),
    "return": np.random.randn(num_coins * num_periods) / 100,
    "market_cap": np.random.randint(10, 1000, num_coins * num_periods)
})

# Portfolio construction
st.subheader("Portfolio Construction")
num_portfolios = st.selectbox("Number of Portfolios (Quintile or Decile Sorts)", [5, 10], index=0)
breakpoint_type = st.radio("Portfolio Breakpoints", ["Market Cap", "Equal"], index=0)
weighting_scheme = st.radio("Portfolio Weighting", ["Value-Weighted", "Equal-Weighted"], index=0)

# Portfolio sorting logic
if breakpoint_type == "Market Cap":
    data["portfolio"] = data.groupby("date")["market_cap"].transform(
        lambda x: pd.qcut(x, q=num_portfolios, labels=False, duplicates="drop")
    )
else:
    data["portfolio"] = data.groupby("date")["signal"].transform(
        lambda x: pd.qcut(x, q=num_portfolios, labels=False, duplicates="drop")
    )

# Portfolio returns calculation
st.subheader("Portfolio Returns")
if weighting_scheme == "Value-Weighted":
    data["weight"] = data["market_cap"]
else:
    data["weight"] = 1

portfolio_returns = (
    data.groupby(["date", "portfolio"])
    .apply(lambda x: np.average(x["return"], weights=x["weight"]))
    .unstack()
    .add_prefix("Portfolio_")
)

st.write("The following table shows portfolio returns:")
st.dataframe(portfolio_returns.head())
# Regression with Liu et al. (2021) factor models
st.subheader("Regression Analysis")
factor_models = [
    "Market-Size-Momentum (Liu et al., 2021)",
    "Market-Size-Reversal",
    "Market-Size-Momentum-Value"
]
selected_model = st.selectbox("Select Factor Model", factor_models)

# Simulated factors for demonstration
factors = pd.DataFrame({
    "CMKT": np.random.randn(num_periods),  # Market factor
    "CSMB": np.random.randn(num_periods),  # Size factor
    "CMOM": np.random.randn(num_periods),  # Momentum factor
    "CREV": np.random.randn(num_periods),  # Reversal factor
    "CHML": np.random.randn(num_periods),  # Value factor
    "date": pd.date_range("2015-01-01", periods=num_periods, freq="M")
}).set_index("date")


# Add factors to portfolio returns
portfolio_returns = portfolio_returns.join(factors, how="inner")

# Regression setup
def run_regression(portfolio, factors, model):
    if model == "Market-Size-Momentum (Liu et al., 2021)":
        X = factors[["CMKT", "CSMB", "CMOM"]]
    elif model == "Market-Size-Reversal":
        X = factors[["CMKT", "CSMB", "CREV"]]
    elif model == "Market-Size-Momentum-Value":
        X = factors[["CMKT", "CSMB", "CMOM", "CHML"]]
    X = sm.add_constant(X)
    y = portfolio
    regression = sm.OLS(y, X).fit()
    return regression

# Run regression for each portfolio
alphas = []
for portfolio in portfolio_returns.columns[:-len(factors.columns)]:
    reg = run_regression(portfolio_returns[portfolio], factors, selected_model)
    alphas.append(reg.params["const"])


# Display alphas
st.write("Portfolio Alphas:")
alpha_df = pd.DataFrame({"Portfolio": portfolio_returns.columns[:-len(factors.columns)], "Alpha": alphas})
st.dataframe(alpha_df)

# Plot alphas
st.subheader("Alpha Visualization")
fig, ax = plt.subplots()
alpha_df.set_index("Portfolio")["Alpha"].plot(kind="bar", ax=ax)
ax.set_title("Portfolio Alphas")
ax.set_ylabel("Alpha")
st.pyplot(fig)

# Add navigation
if st.button("Next Step"):
    st.success("Proceeding to the next step...")