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

st.subheader("Panel A: T-stats from Fama-MacBeths")

st.subheader("Panel B: T-stats from spanning tests")

st.subheader("Panel C: T-stats from conditional sorts")


st.header("Fama-MacBeths Controlling for Most Closely Related Anomalies")

st.header("Spanning Tests Controlling for Most Closely Related Anomalies")