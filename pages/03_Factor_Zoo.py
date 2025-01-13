import streamlit as st

st.title("Signal Performance Relative to the Factor Zoo")

st.write(r"""
This section considers the anomaly"s performance 
         in the context of the factor zoo. It does so by comparing 
         the proposed factor's performance to that of other anomalies 
         from the literature.

         """)


st.header("Distribution of Sharpe Ratios")

st.write(r"""
The figure puts the performance of the candidate anomaly in context,
showing the long/short strategy performance relative ot other strategies in the factor zoo.
It shows Sharpe ratio histograms, both for gross and net returns.
The vertical red line shows where the Sharpe ratio for the candidate strategy falls 
in the distribution. 
Panel A plots results for gross Sharpe ratios. Panel B plots results for net Sharpe ratios.
         """)

st.subheader("Panel A: Gross Sharpe Ratios")


st.subheader("Panel B: Net Sharpe Ratios")


st.header("Dollar Invested")

st.write(r"""
         The figure plots the growth of a 
         \$1 invested in these same anomalies trading strategies (gray lines),
         and compares those with the growth of a \$1 invested in the candidate anomaly strategy (red line).
         Panel A plots results for gross strategy returns. Panel B plots 
         results for net strategy returns.
         """)

st.subheader("Panel A: Gross Returns")


st.subheader("Panel B: Net Returns")


st.header("Anomaly Percentile Rank")

st.write(r"""
         The figure plots percentile ranks for the anomaly 
         trading strategies in terms of gross and Novy-Marx and Velikov (2016) net 
         generalized alphas with respect to Liu et al. (2021) factor models from 
         the first table, and indicates the ranking of the candidate anomaly relative to those.
         Panel A shows the percentile ranks for gross alphas.
            Panel B shows the percentile ranks for net generalized alphas.
            """)

st.subheader("Panel A: Gross Alpha Percentile Rank")

st.subheader("Panel B: Net Alpha Percentile Rank")