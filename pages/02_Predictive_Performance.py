import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Page title
st.title("Predictive Performance")

st.write(r"""
This stage checks whether the signal reliably predicts cross-sectional differences
in average returns. 
         """)


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


st.header("Basic Sort")

st.write(r"""
This first table reports time-series regression results employing the value-weighted returns 
or the equal-weighted returns to portfolios constructed from a quintile sort on the candidate predictor (signal).
Univeriate sorts like these are the main technique in the anomaly literature to test whether a 
signal predicts returns in the cross-section of assets. 
         
A conservative choice would be to choose the value-weighting scheme, as a anomalies are usually strongest
amont micro-cap coins and thus geneerally look stronger when implemented using equal-weighted portfolio returns (Fama and French, 2008).
The default choice of value-weighting provides results that are closer to what 
an actual investor might be able to achieve in practice.
         """)


st.write(r"""
The table reports average excess returns and alphas for portfolios sorted on the signal.
At the end of each month, we sort stocks into five portfolios based on their signal.
Panel A reports average value-weighted quintile portfolio (L, 2, 3, 4, H) returns in excess of the risk-free rate, 
the long-short extreme quintile portfolio (H-L) return and alphas with respect to the Liu et al. (2021) three-factor model.
Panel B reports the factor loadings for the quintile portfolios and long-short extreme quintile portfolio in the Liu et al. (2021) three-factor model.
         """)
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

st.header("Robustnees to Sorting Methodology & Trading Costs")

st.write(r"""
The table reports results for various alternative construction methodologies.
It varies the number of portfolios (five or ten) and the weighting of 
individual coins within each portfolio (market capitalization-weighted or equal-weighted).
Panel B considers the impact of accounting for transaction costs. The trading cost 
calculation follows Detzel et al. (2022). The net-of-costs return on anomaly $g$ in month $y$ is:
         """)
st.latex(r"""
         \begin{equation}
         f_t^{net} = f_t^{gross} - TC_{Long,t} - TC_{Short,t}
            \end{equation}
            """)

st.write(r"""
         where:
         """)

st.latex(r"""
            \begin{equation}  
         TC_{j,t} = \sum_{i \in I_{j,t}} |w_{i,t} - \tilde{w}_{i,t-1}| \times c_{i,t}
            \end{equation}
            """)

st.write(r"""
         for j $\in {Long, Short}$ and $I_{j,t}$ indexes the coin in portfolio
         $j$ at time $t$. $c_{i,t}$ is the one-way trading cost of coin $i$ 
         at time $t$, measured as the high-frequency combination effective half-spreads from Chen and Velikov (2022);
         $w_{i,t}$ is the weight of coin $i$ in its portfolio at time $t$ after rebalancing 
         and $\tilde{w}_{i,t-1} = \frac{w_{i,t-1}(1 + r_{i,t})}{\sum_{k \in I_{j,t}} w_{k,t-1}(1 + r_{k,t})}$ is the
         weight of the coin in the portfolio before rebalancing.

         Panel B also report the Novy-Marx and Velikov (2016) generalized alphas that 
         account for trading costs. It reports these generalized alphas relative to the Liu et al. (2021) model.
         The alphas are estimated as:
         """)

st.latex(r"""
            \begin{equation}
         w^{-1}_{y, MVE_{\{X,y\}}} MVE_{\{X,y\}} = \alpha + \beta \cdot MVE_{\{X\}} + \epsilon
            \end{equation}
            """)

st.write(r"""
         where $MVE_{\{X\}}$ denotes the ex-post mean-variance efficient portfolio 
         of the assets $X$, where $X$ are the factors in the model and $w_{y, MVE_{\{X,y\}}}$ denotes the weights on 
         asset $y$ (the candidate factor) in $MVE_{\{X,y\}}$. Following Novy-Marx and Velikov (2016), $\alpha$ 
         is defined to equal 0 when $w_{y, MVE_{\{X,y\}}} = 0$.
            """)


# Trading cost assumption (0.1% per trade for simplicity)
trading_cost = 0.001

# Add alternative sorting methods to analyze robustness
sorting_methods = [
    {"Portfolios": "Quintile", "Weights": "Market Cap Weighted"},
    {"Portfolios": "Quintile", "Weights": "Equal Weighted"},
    {"Portfolios": "Decile", "Weights": "Market Cap Weighted"},
]
# Function to calculate returns, alphas, and net alphas
def analyze_portfolio(method, data, factors, trading_cost):
    # Determine number of portfolios
    num_portfolios = 5 if method["Portfolios"] == "Quintile" else 10

    # Portfolio sorting
    data["portfolio"] = data.groupby("date")["signal"].transform(
        lambda x: pd.qcut(x, q=num_portfolios, labels=range(1, num_portfolios + 1), duplicates="drop")
    )

    # Weighting scheme
    if method["Weights"] == "Market Cap Weighted":
        data["weight"] = data["market_cap"]
    else:
        data["weight"] = 1

    # Calculate portfolio returns
    portfolio_returns = (
        data.groupby(["date", "portfolio"])
        .apply(lambda x: np.average(x["return"], weights=x["weight"]))
        .unstack()
    )
    portfolio_returns["H-L"] = portfolio_returns.iloc[:, -1] - portfolio_returns.iloc[:, 0]

    # Merge factors with portfolio returns
    portfolio_returns = portfolio_returns.join(factors, how="inner")

    # Regression to compute alphas
    def run_regression(portfolio, factors):
        X = sm.add_constant(factors[["CMKT", "CSMB", "CMOM"]])
        y = portfolio
        reg = sm.OLS(y, X).fit()
        return reg.params, reg.tvalues

    # Compute alphas and t-stats
    alphas = {}
    for col in portfolio_returns.columns[:num_portfolios]:
        params, tvals = run_regression(portfolio_returns[col], portfolio_returns[["CMKT", "CSMB", "CMOM"]])
        alphas[col] = {"alpha": params["const"], "tval": tvals["const"]}

    # Compute trading costs
    turnover = data.groupby(["date", "portfolio"])["weight"].apply(lambda x: x.diff().abs().sum()).unstack().mean()
    net_alphas = {k: v["alpha"] - (turnover[k] * trading_cost) for k, v in alphas.items()}

    return portfolio_returns.mean(), alphas, net_alphas
# Analyze each sorting method
results = []
for method in sorting_methods:
    # Determine number of portfolios
    num_portfolios = 5 if method["Portfolios"] == "Quintile" else 10

    # Portfolio sorting
    data["portfolio"] = data.groupby("date")["signal"].transform(
        lambda x: pd.qcut(x, q=num_portfolios, labels=range(1, num_portfolios + 1), duplicates="drop")
    )

    # Weighting scheme
    if method["Weights"] == "Market Cap Weighted":
        data["weight"] = data["market_cap"]
    else:
        data["weight"] = 1

    # Calculate portfolio returns
    portfolio_returns = (
        data.groupby(["date", "portfolio"])
        .apply(lambda x: np.average(x["return"], weights=x["weight"]))
        .unstack()
    )
    portfolio_returns["H-L"] = portfolio_returns.iloc[:, -1] - portfolio_returns.iloc[:, 0]

    # Merge factors with portfolio returns
    portfolio_returns = portfolio_returns.join(factors, how="inner")

    # Regression to compute alphas
    def run_regression(portfolio, factors):
        X = sm.add_constant(factors[["CMKT", "CSMB", "CMOM"]])
        y = portfolio
        reg = sm.OLS(y, X).fit()
        return reg.params, reg.tvalues

    # Compute alphas and t-stats for each portfolio, including "H-L"
    alphas = {}
    for col in portfolio_returns.columns[:-len(factors.columns)]:  # Only portfolio columns
        params, tvals = run_regression(portfolio_returns[col], portfolio_returns[["CMKT", "CSMB", "CMOM"]])
        alphas[col] = {"alpha": params["const"], "tval": tvals["const"]}

    # Compute trading costs
    turnover = (
        data.groupby(["date", "portfolio"])["weight"]
        .apply(lambda x: x.diff().abs().sum())
        .unstack()
        .mean()
    )
    net_alphas = {k: v["alpha"] - (turnover.get(k, 0) * trading_cost) for k, v in alphas.items()}

    # Store results for the "H-L" portfolio
    results.append({
        "Portfolios": method["Portfolios"],
        "Weights": method["Weights"],
        "Gross Return (H-L)": portfolio_returns["H-L"].mean(),
        "Alpha (H-L)": alphas.get("H-L", {}).get("alpha", np.nan),
        "t(Alpha)": alphas.get("H-L", {}).get("tval", np.nan),
        "Net Alpha (H-L)": net_alphas.get("H-L", np.nan)
    })

# Panel A: Gross Returns and Alphas
st.subheader("Panel A: Gross Returns and Alphas")
panel_a = pd.DataFrame(results)
panel_a = panel_a[["Portfolios", "Weights", "Gross Return (H-L)", "Alpha (H-L)", "t(Alpha)"]]
st.table(panel_a)

# Panel B: Net Returns and Generalized Alphas
st.subheader("Panel B: Net Returns and Generalized Alphas")
panel_b = pd.DataFrame(results)
panel_b = panel_b[["Portfolios", "Weights", "Gross Return (H-L)", "Net Alpha (H-L)", "t(Alpha)"]]
st.table(panel_b)

# Notes
st.markdown("""
**Notes:**
1. Trading costs are applied as a 0.1% per trade assumption.
2. Factor models include CMKT (Market), CSMB (Size), and CMOM (Momentum).
3. Portfolio sorting and weighting schemes are dynamically adjusted for analysis.
4. Net alpha is computed as gross alpha minus trading cost adjustment.
""")

st.header("Conditional Sort on Size and Candidate Signal")

st.write(r"""
The table explicitly accounts for the role of coin size in the strength
         of the candidate anomaly's performance. It does so 
         by constructing strategies based on the candidate 
         cross-sectional returns prediction within size quintiles. 
         The table reports average portfolio returns, average number of coins 
         and average coin size, for twenty five portfolios constructed from a 
         conditional double sort on size and the candidate signal. 
         It also reports the average returns and alphas for long/short trading 
         strategies based on the signal within each size quintile. 

In each month, coins are first sorted into quintiles based on size breakpoints.
Then, within each size quintile, coins are further sorted based on the candidate signal.
Finally, they are grouped into twenty-five portfolios based on the intersection of the two sorts.
Panel A presents the average returns to the 25 portfolios, as well as strategies that go 
long stocks with high signal values and short stocks with low signal values within each size quintile.
Panel B documents the average coin size for each portfolio.
         """)
# Conditional Sort on Size and Signal
data["size_quintile"] = data.groupby("date")["market_cap"].transform(
    lambda x: pd.qcut(x, q=5, labels=["1", "2", "3", "4", "5"], duplicates="drop")
)
data["signal_quintile"] = data.groupby(["date", "size_quintile"])["signal"].transform(
    lambda x: pd.qcut(x, q=5, labels=["L", "2", "3", "4", "H"], duplicates="drop")
)

# Group by size and signal quintiles
portfolio_returns = (
    data.groupby(["date", "size_quintile", "signal_quintile"])["return"]
    .mean()
    .unstack(level=["size_quintile", "signal_quintile"])
)

# Calculate average returns and t-statistics
average_returns = portfolio_returns.mean()
t_stats = average_returns / (portfolio_returns.std() / np.sqrt(num_periods))

def run_regression(portfolio, factors):
    # Align indices between portfolio returns and factors
    portfolio = portfolio.dropna()  # Drop missing values
    factors = factors.loc[portfolio.index]  # Align factors with portfolio index
    
    X = sm.add_constant(factors[["CMKT", "CSMB", "CMOM"]])
    y = portfolio
    reg = sm.OLS(y, X).fit()
    return reg.params["const"], reg.tvalues["const"]

# Merge portfolio returns with factors
portfolio_returns = portfolio_returns.stack(["size_quintile", "signal_quintile"]).reset_index()
portfolio_returns = portfolio_returns.rename(columns={0: "return"})

# Merge with factors on 'date'
portfolio_returns = pd.merge(portfolio_returns, factors.reset_index(), on="date")

# Re-index portfolio returns
portfolio_returns = portfolio_returns.set_index(["date", "size_quintile", "signal_quintile"])

# Run regressions for all portfolios
alphas = {}
t_alphas = {}
for size in ["1", "2", "3", "4", "5"]:
    for signal in ["L", "2", "3", "4", "H"]:
        portfolio = portfolio_returns.loc[
            (slice(None), size, signal), "return"
        ]  # Select specific portfolio returns
        portfolio_factors = portfolio_returns.loc[
            (slice(None), size, signal), ["CMKT", "CSMB", "CMOM"]
        ]  # Select factors
        alpha, t_alpha = run_regression(portfolio, portfolio_factors)
        alphas[(size, signal)] = alpha
        t_alphas[(size, signal)] = t_alpha

# Create Panel A DataFrame
panel_a_data = []
for size in ["1", "2", "3", "4", "5"]:
    row = {"Size Quintile": size}
    for signal in ["L", "2", "3", "4", "H"]:
        key = (size, signal)
        row[f"{signal} Return"] = average_returns.get(key, np.nan)
        row[f"t({signal})"] = t_stats.get(key, np.nan)
        row[f"{signal} Alpha"] = alphas.get(key, np.nan)
        row[f"t(Alpha {signal})"] = t_alphas.get(key, np.nan)
    panel_a_data.append(row)

panel_a = pd.DataFrame(panel_a_data)

# Display Panel A
st.subheader("Panel A: Portfolio Average Returns and Time-Series Regression Results")
st.table(panel_a)

# Notes
st.markdown("""
**Notes:**
1. Average returns are based on monthly portfolio data, with portfolios sorted by size and signal quintiles.
2. Alphas are estimated using the Liu et al. (2021) three-factor model.
3. T-statistics are shown in brackets.
""")
