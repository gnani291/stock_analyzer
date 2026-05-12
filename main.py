import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Company name to stock symbol mapping
company_map = {
    "apple": "AAPL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "microsoft": "MSFT",
    "tesla": "TSLA",
    "amazon": "AMZN",
    "nvidia": "NVDA",
    "meta": "META",
    "netflix": "NFLX",
    "infosys": "INFY.NS",
    "tcs": "TCS.NS",
    "reliance": "RELIANCE.NS",
    "hdfc": "HDFCBANK.NS"
}

# Streamlit UI
st.title("📈 Stock Market Analyzer")
st.write("Analyze any company stock using NumPy and Python")

# User input
company = st.text_input("Enter Company Name")

if company:

    company = company.lower()

    # Get stock ticker
    ticker = company_map.get(company)

    # If company not found
    if not ticker:
        st.error("Company not found in database!")
    else:

        st.write(f"Stock Symbol: {ticker}")

        # Download stock data
        data = yf.download(ticker, period="6mo")

        if data.empty:
            st.error("No stock data found!")
        else:

            # Closing prices
            prices = data['Close'].values.flatten()

            # NumPy Analysis
            average_price = np.mean(prices)
            highest_price = np.max(prices)
            lowest_price = np.min(prices)

            daily_returns = np.diff(prices)

            moving_average = np.convolve(
                prices,
                np.ones(5)/5,
                mode='valid'
            )

            total_change = prices[-1] - prices[0]
            percentage_change = (
                total_change / prices[0]
            ) * 100

            # Display Results
            st.subheader("📊 Stock Analysis")

            st.write(f"Average Price: {average_price:.2f}")
            st.write(f"Highest Price: {highest_price:.2f}")
            st.write(f"Lowest Price: {lowest_price:.2f}")
            st.write(f"Total Change: {total_change:.2f}")
            st.write(
                f"Percentage Change: {percentage_change:.2f}%"
            )

            # Plot Graph
            fig, ax = plt.subplots(figsize=(10, 5))

            ax.plot(
                prices,
                label='Closing Prices'
            )

            ax.plot(
                range(4, len(prices)),
                moving_average,
                label='5-Day Moving Average'
            )

            ax.set_title(f"{ticker} Stock Analysis")
            ax.set_xlabel("Days")
            ax.set_ylabel("Price")
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)