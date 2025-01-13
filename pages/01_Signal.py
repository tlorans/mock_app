import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Signal")

# Signal selection dropdown
st.markdown("Select a signal to use for your strategy.")
signal_type = st.selectbox(
    "Signal Type",
    ["Size (Market Cap)", "Price", "Volume", "Past Performance", "Market Beta"]
)

# Signal-specific configuration
if signal_type == "Size (Market Cap)":
    st.markdown("**Size-based Signal:**")
    size_filter = st.slider(
        "Filter by Market Cap (in million USD)", min_value=10, max_value=5000, value=(10, 500)
    )
    st.write(f"Selected market cap range: {size_filter}M USD")

elif signal_type == "Price":
    st.markdown("**Price-based Signal:**")
    price_filter = st.slider(
        "Filter by Price (in USD)", min_value=0.1, max_value=1000.0, value=(0.1, 100.0)
    )
    st.write(f"Selected price range: {price_filter} USD")

elif signal_type == "Volume":
    st.markdown("**Volume-based Signal:**")
    volume_filter = st.slider(
        "Filter by Daily Trading Volume (in million USD)", min_value=0, max_value=10000, value=(0, 1000)
    )
    st.write(f"Selected volume range: {volume_filter}M USD")

elif signal_type == "Past Performance":
    st.markdown("**Past Performance Signal:**")
    st.radio(
        "Strategy Type",
        ["Momentum (Positive Past Returns)", "Reversal (Negative Past Returns)"]
    )
    lookback_period = st.selectbox(
        "Lookback Period for Returns", [1, 7, 14, 30, 90, 180, 360], index=3
    )
    st.write(f"Selected lookback period: {lookback_period} days")

elif signal_type == "Market Beta":
    st.markdown("**Market Beta Signal:**")
    beta_filter = st.slider(
        "Filter by Beta (relative to Bitcoin)", min_value=-2.0, max_value=2.0, value=(-1.0, 1.0)
    )
    st.write(f"Selected beta range: {beta_filter}")

# Simulated Data Preview
st.header("Simulated Data Preview")
st.markdown(
    "Here's an example dataset based on the selected signal to give you an idea of how the strategy will be applied."
)

# Generate sample data based on signal
np.random.seed(42)
num_rows = 100
example_data = pd.DataFrame({
    "coin_id": [f"coin_{i}" for i in range(1, num_rows + 1)],
    "date": pd.date_range("2025-01-01", periods=num_rows, freq="D"),
    "signal": np.random.rand(num_rows) * 100,  # Random signal for demonstration
    "return": np.random.randn(num_rows) / 100  # Random returns
})

# Filter data based on user selection
if signal_type == "Size (Market Cap)":
    example_data["market_cap"] = np.random.randint(5, 5000, size=num_rows)  # Random market cap
    example_data = example_data[(example_data["market_cap"] >= size_filter[0]) &
                                 (example_data["market_cap"] <= size_filter[1])]
elif signal_type == "Price":
    example_data["price"] = np.random.uniform(0.1, 1000, size=num_rows)  # Random price
    example_data = example_data[(example_data["price"] >= price_filter[0]) &
                                 (example_data["price"] <= price_filter[1])]
elif signal_type == "Volume":
    example_data["volume"] = np.random.randint(1, 10000, size=num_rows)  # Random volume
    example_data = example_data[(example_data["volume"] >= volume_filter[0]) &
                                 (example_data["volume"] <= volume_filter[1])]
elif signal_type == "Past Performance":
    example_data["past_return"] = example_data["return"].rolling(lookback_period).mean()  # Simulate past returns
elif signal_type == "Market Beta":
    example_data["beta"] = np.random.uniform(-2, 2, size=num_rows)  # Random beta
    example_data = example_data[(example_data["beta"] >= beta_filter[0]) &
                                 (example_data["beta"] <= beta_filter[1])]

# Display filtered data
st.write("Filtered Data Preview:", example_data.head())

# Save the signal selection in the session state
if st.button("Next Step"):
    st.session_state["signal_type"] = signal_type
    st.success("Signal selection saved! Navigating to the next step...")
