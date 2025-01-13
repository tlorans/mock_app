import streamlit as st
from PIL import Image

# Page Title
st.title("Backtesting Strategy Workflow")

# Introduction
st.write("""
Backtesting a strategy involves several stages, each designed to evaluate and refine 
the strategy's performance using historical data. This application walks through all 
the necessary stages to develop, test, and analyze a trading strategy effectively.
""")

# Stages Overview
st.header("Stages of Backtesting")

st.write("""
The backtesting workflow includes the following stages:
1. **Signal Selection**: Choose the signal or indicator that drives your strategy (e.g., size, price, volume, beta).
2. **Data Preparation**: Gather historical data and clean it for analysis.
3. **Portfolio Construction**: Construct portfolios based on the selected signal (e.g., quintile or decile sorts).
4. **Performance Evaluation**: Analyze portfolio returns and calculate performance metrics like Sharpe ratios and alphas.
5. **Trading Costs Adjustment**: Incorporate transaction costs into the analysis to evaluate net returns.
6. **Comparison Against Factor Zoo**: Compare the strategy's performance relative to other known anomalies.
7. **Robustness Tests**: Test the strategy's sensitivity to different methodologies and sorting methods.
8. **Combination with Other Factors**: Evaluate how the signal interacts with or adds value to existing factors.
""")
