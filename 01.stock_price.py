import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from PIL import Image


# Define the color palette
PRIMARY_COLOR = "#780303"
SECONDARY_COLOR = "#0e75a1"
BACKGROUND_COLOR = "#f7f7f7"


image = Image.open('trading.png')

st.image(image, width=250)



# Set the color of the page title and subtitle
st.markdown(f"""<h1 style='color:{PRIMARY_COLOR};font-size:48px;'>Stock Price App</h1>""" ,unsafe_allow_html=True)
st.write("""
* **Python libraries:** pandas, streamlit, yfinance, plotly, PIL
Shown are the stock **closing price** , ***volume***, ***SMA*** and ***Correlation Analysis*** of Google, Tesla and Apple!
""")

# Add a container for the sidebar
sidebar = st.sidebar.container()

# Add a container for the main content
main = st.container()

# Add a container for the footer
footer = st.container()

with sidebar:
    st.sidebar.subheader("Select a date range")
    start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2022-2-28"))
    end_date = st.sidebar.date_input("End date", value=pd.to_datetime("2023-2-28"))
    st.sidebar.subheader("Select a ticker symbol")
    tickerSymbol = st.sidebar.selectbox("Select a ticker symbol", ["TSLA", "AAPL", "GOOGL"])
    st.sidebar.subheader("Correlation Analysis")
    tickerSymbol2 = st.sidebar.selectbox("Select a second ticker symbol", ["AAPL", "GOOGL"])

 

# Get the data for the first ticker symbol
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date).reset_index()

# Get the data for the second ticker symbol
tickerData2 = yf.Ticker(tickerSymbol2)
tickerDf2 = tickerData2.history(period='1d', start=start_date, end=end_date).reset_index()

# Calculate the daily returns for both ticker symbols
returns = pd.concat([tickerDf['Close'].pct_change(), tickerDf2['Close'].pct_change()], axis=1)
returns.columns = [tickerSymbol, tickerSymbol2]



# Calculate the correlation between the two stocks
correlation = returns.corr()


# Modify the column width
correlation = correlation.style.set_properties(**{'width': '800px'})

# Display the correlation matrix
st.write('### Correlation Matrix')
st.write(correlation)




st.sidebar.markdown(
    """
    <div class="footer">
    Data provided by Yahoo Finance<br>
    Developed by Wioletta Koczor
    </div>
    """,
    unsafe_allow_html=True,
)



# Create Candlestick
fig = go.Figure(data=[go.Candlestick(
    x=tickerDf['Date'],
    open=tickerDf['Open'],
    high=tickerDf['High'],
    low=tickerDf['Low'],
    close=tickerDf['Close']
)])

# Set the layout for the candlestick chart
fig.update_layout(
    title=tickerSymbol + ' Candlestick Chart',
    title_font=dict(size=24, color='#333'),
    font=dict(size=12, color='#333'),
    plot_bgcolor='#f5f5f5',  # Set background color
    paper_bgcolor='white',
    legend=dict(  # Add a legend
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=12, color='#333')
    )
)

# Add a shape and annotation if the selected ticker symbol is TSLA
if tickerSymbol == 'TSLA':
    fig.update_layout(shapes=[dict(
        x0='2022-05-06',
        x1='2022-05-06',
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line_width=2,
        line_color='#333',
        opacity=0.5
    )])
    fig.update_layout(annotations=[dict(
        x='2022-05-06',
        y=0.05,
        xref='x',
        yref='paper',
        showarrow=False,
        xanchor='left',
        text='Tesla Cybertruck Event',
        font=dict(size=12, color='#333')
    )])

# Display the candlestick chart
st.plotly_chart(fig)


# Display the closing price and volume
st.write('### Closing Price')
st.line_chart(tickerDf['Close'].rename("Price ($)"))  # Add y-axis label
st.write('### Volume')
st.line_chart(tickerDf['Volume'].rename("Volume"))  # Add y-axis label

# Add Simple Moving Average (SMA)
sma30 = tickerDf['Close'].rolling(window=30).mean()
sma100 = tickerDf['Close'].rolling(window=100).mean()

# Add Exponential Moving Average (EMA)
ema30 = tickerDf['Close'].ewm(span=30, adjust=False).mean()
ema100 = tickerDf['Close'].ewm(span=100, adjust=False).mean()

# Add SMA to the candlestick chart
fig.add_trace(go.Scatter(x=tickerDf['Date'], y=sma30, name='SMA 30 days'))
fig.add_trace(go.Scatter(x=tickerDf['Date'], y=sma100, name='SMA 100 days'))

# Set the layout for the SMA chart
fig.update_layout(
    title='Simple Moving Average (SMA)',
    title_font=dict(size=24, color='#333'),
    xaxis_title='Date',  # Add x-axis label
    yaxis_title='Price ($)',  # Add y-axis label
    font=dict(size=12, color='#333'),
    plot_bgcolor='#f5f5f5',  # Set background color
    paper_bgcolor='white',
    legend=dict(  # Add a legend
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=12, color='#333')
    )
)

# Display the SMA chart
st.plotly_chart(fig)

streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Phudu:wght@300&family=Shantell+Sans:wght@300&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Phudu', cursive;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)
# --- hide streamlit style ---

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

