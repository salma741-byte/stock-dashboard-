import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# -------- LOAD DATA --------
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -------- SIDEBAR --------
st.sidebar.title("📊 Stock Market Dashboard")

ticker_list = df["Ticker"].unique()
selected_ticker = st.sidebar.selectbox("Select Company", ticker_list)

filtered_df = df[df["Ticker"] == selected_ticker].sort_values("Date")

# -------- MAIN TITLE --------
st.title(f"{selected_ticker} Stock Analysis")

# -------- PRICE CHART --------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=filtered_df["Date"],
    y=filtered_df["Prix_Actuel"],
    mode='lines',
    name='Close Price'
))

fig.update_layout(
    title="Close Price Over Time",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# -------- CANDLESTICK --------
st.subheader("Candlestick Chart")

fig2 = go.Figure(data=[go.Candlestick(
    x=filtered_df['Date'],
    open=filtered_df['Ouverture'],
    high=filtered_df['Plus_Haut'],
    low=filtered_df['Plus_Bas'],
    close=filtered_df['Prix_Actuel']
)])

fig2.update_layout(template="plotly_dark")

st.plotly_chart(fig2, use_container_width=True)

# -------- SUMMARY TABLE --------
st.subheader("Latest Data")

latest_data = filtered_df.iloc[-1]
st.dataframe(latest_data)
