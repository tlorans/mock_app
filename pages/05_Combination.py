import streamlit as st

st.title("Does the Signal Add Relative to the Whole Zoo?")

st.write(r"""
This section quantifies the extent to which the test signal 
         increases the investment frontier beyond that spanned by the entire factor zoo.kwargs=
            """)


st.header("Combination Strategy Performance")

st.write(r"""
         The figures below plot the growth of a 
         1\$ invested in trading strategies that combine 
         multiple anomalies following Chen and Velikov (2022).
         We combine signals using a linear model of expected returns:
            """)

st.latex(r"""
            \begin{equation}
         \mathbb{E}(r_{i,t+1}) = \beta_0 + \sum^J_{j=1} \beta_j x_{i,j,t}
            \end{equation}
            """)

st.write(r"""
         where $r_{i,t+1}$ is the gross return of coin $i$ in month $t+1$,
         $J$ is the total number of predictors, $\beta_j$ is the slope coefficient
         on predictor $j$ and $x_{i,j,t}$ is the standardized $jth$ anomaly characteristic for 
         coin $i$ in month $t$.
            """)

st.write(r"""
         The figure shows result using six different methods for combining anomalies. 
         The methods used are average rank (i.e., $\hat{\beta}_j = 1/J$),
         weighted-average rank (i.e., $\hat{\beta}_j = \propto \bar{r}^j$),
         Fama-MacBeth regression following Lewellen (2015), Partial Least 
         Squares (PLS) filter following Light et al. (2017), 
         Instrumented Principal Component Analysis (IPCA) following Kelly et al. (2019),
         and the Least Absolute Shrinkage and Selection Operator (LASSO), as implemented 
         in Chen and Velikov (2022).

         The figure compares the performance of combinations made using the broad 
         cross-section of known anomalies, and the extent to which performance is improved by 
         also including the proposed candidate signal.
         """)

st.subheader("Panel A: Average Rank")

st.subheader("Panel B: Weighted-Average Rank")

st.subheader("Panel C: Fama-MacBeth")

st.subheader("Panel D: Partial Least Squares")

st.subheader("Panel E: IPCA")

st.subheader("Panel F: LASSO")