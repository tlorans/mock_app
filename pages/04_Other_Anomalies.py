import streamlit as st 

st.title("Candidate Signal and Related Anomalies")

st.write(r"""
Even if a candidate strategy has strong performance relative to most 
of the factors in the zoo, it may still not add significantly to the factor zoo. For example, a slight variation on one of the strongest 
known anomalies will itself have strong performance, but will not be 
a significant addition ot the zoo already containing the strategy 
on which it is a variation. This section accounts for this, by 
checking if the test signal adds information beyond that provided 
to the most closely related known anomalies.
 """)


st.header("Distribution of Correlations")

st.write(r"""
The figure plots a name histogram of the panel correlations 
of the test signal with the anomaly signals from the factor zoo.
         """)

st.subheader("Panel A: Pearson Correlations")

st.subheader("Panel B: Spearman Correlations")


st.header("Agglomerative Hierarchical Cluster Plot")

st.write(r"""
The figure shows an agglomerative hierarchical cluster plot using 
Ward's minimum method and a maximum of 10 clusters.""")

st.header("Distribution of t-stats on Conditioning Strategies")

st.write(r"""
         The figure below shows how much 
         the candidate signal adds relative to each 
         individual member in the factor zoo.
         It plots histograms of t-statistics for predictability tests,
         which test the power of the test signal controlling for other individual known anomaly
         signals. Panel A reports t-statistics on the loading on the test signal,
         $t(\beta_{S})$ from Fama-MacBeth regression of the form:
         """)

st.latex(r"""
         \begin{equation}
         r_{i,t} = \alpha + \beta_{S}S_{i,t} + \beta_X X_{i,t} + \epsilon_{i,t}
         \end{equation}
         """)

st.write(r"""
         where $X$ stands for one of the anomaly signals at a time, 
         and $S$ stands for the test signal.
         Panel B plots tèstatistics on $\alpha$ from spanning tests of the form:
         """)

st.latex(r"""
            \begin{equation}
         r_{S,t} = \alpha + \beta r_{X,t} + \epsilon_{t}
            \end{equation}
            """)

st.write(r"""
         where $r_{S,t}$ is the return on the test signal, $r_{X,t}$ is the return
            on one of the anomaly signals at a time, and $\alpha$ is the intercept.
         The strategies employed in the spanning tests are constructed using quintile sorts and value-weigthting.
         """)

st.write(r"""
         Panel C plots t-statistics on the average returns to strategies 
         constructed by conditional double sorts.
         In each month, we sort stocks into quintiles based on one 
         of the anomaly signals at a time. Then, within each 
         quintile, we sort stocks into quintiles based on the test signal.
         Stocks are finally grouped into five test-signal portfolios by combining stocks 
         within each anomaly sorting portfolio.
         The panel plots the t-statistics on the average returns of these conditional 
         double-sorted trading strategies of the test signal conditioneed on each of the anomalies.
         """)

st.subheader("Panel A: T-stats from Fama-MacBeths")

st.subheader("Panel B: T-stats from spanning tests")

st.subheader("Panel C: T-stats from conditional sorts")

st.write(r"""
The tables below control for the six most-closely related anomalies.
To find the most closely related anomalies, we rank all anomalies based on:
""")

st.latex(r"""
\begin{equation}
\text{rank}(|\rho_{i,s}|) + \text{rank}(R^2_{r_t^i = \alpha + \beta r_t^s + \epsilon_t})
\end{equation}
""")

st.write(r"""
where $\rho_{i,s}$ is the panel correlation of the underlying signal for anomaly $i$ 
and the test signal $s$ and $R^2_{r_t^i = \alpha + \beta r_t^s + \epsilon_t}$ is the $R^2$ 
from the spanning test of regressing the returns to the testing 
strategy exploiting anomaly $i$ on the test signal $s$.
""")

st.write(r"""
The first stable reports Fama-MacBeth cross-sectional regression of returns 
on the test signal controlling for the six most closely-related anomalies, 
both individually and jointly.
The second table reports spanning tests results from time-series regressions 
of the returns to the test signal trading strategy onto the returns 
of trading strategies exploiting the six most closely-related anomalies 
and the Liu et al. (2021) three factors.
""")

st.header("Fama-MacBeths Controlling for Most Closely Related Anomalies")

st.header("Spanning Tests Controlling for Most Closely Related Anomalies")