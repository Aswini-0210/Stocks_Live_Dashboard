import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import time

# Page config (default Streamlit theme)
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📈 Stock Market Dashboard")

# --- Sector dictionary with display names (for sidebar) and tickers (for data)
sectors = {
    "🌐 Overall Summary": [],
    "💻 Technology": [("Apple", "AAPL"), ("Microsoft", "MSFT"), ("Google", "GOOGL"), ("Meta", "META"), ("Oracle", "ORCL"), ("IBM", "IBM"), ("Intuit", "INTU"), ("Adobe", "ADBE"), ("AMD", "AMD"), ("NVIDIA", "NVDA")],
    "🏦 Finance": [("HDFC Bank", "HDFCBANK.NS"), ("ICICI Bank", "ICICIBANK.NS"), ("JPMorgan Chase", "JPM"), ("Bank of America", "BAC"), ("Axis Bank", "AXISBANK.NS"), ("SBI", "SBIN.NS"), ("Goldman Sachs", "GS"), ("Citi", "C"), ("Kotak Bank", "KOTAKBANK.NS"), ("PNB", "PNB.NS")],
    "🧠 IT Services": [("Infosys", "INFY.NS"), ("TCS", "TCS.NS"), ("Wipro", "WIPRO.NS"), ("Tech Mahindra", "TECHM.NS"), ("HCL Tech", "HCLTECH.NS"), ("Mphasis", "MPHASIS.NS"), ("LTTS", "LTTS.NS"), ("Birlasoft", "BSOFT.NS"), ("Coforge", "COFORGE.NS"), ("Sona Comstar", "SONACOMS.NS")],
    "🏭 Industrial": [("Reliance", "RELIANCE.NS"), ("Tata Motors", "TATAMOTORS.NS"), ("L&T", "LT.NS"), ("Hindalco", "HINDALCO.NS"), ("Adani Ports", "ADANIPORTS.NS"), ("GAIL", "GAIL.NS"), ("BHEL", "BHEL.NS"), ("NTPC", "NTPC.NS"), ("Power Grid", "POWERGRID.NS"), ("JSW Steel", "JSWSTEEL.NS")],
    "🏠 FMCG": [("ITC", "ITC.NS"), ("HUL", "HINDUNILVR.NS"), ("Dabur", "DABUR.NS"), ("Nestle", "NESTLEIND.NS"), ("Britannia", "BRITANNIA.NS"), ("Colgate", "COLPAL.NS"), ("Emami", "EMAMILTD.NS"), ("Godrej", "GODREJCP.NS"), ("Marico", "MARICO.NS"), ("Radico", "RADICO.NS")],
    "🔌 Energy": [("ONGC", "ONGC.NS"), ("Coal India", "COALINDIA.NS"), ("IOC", "IOC.NS"), ("BPCL", "BPCL.NS"), ("Adani Energy", "ADANIENSOL.NS"), ("NHPC", "NHPC.NS"), ("Tata Power", "TATAPOWER.NS"), ("GAIL", "GAIL.NS"), ("Power Grid", "POWERGRID.NS"), ("NTPC", "NTPC.NS")],
    "🚗 Auto": [("Maruti", "MARUTI.NS"), ("Tata Motors", "TATAMOTORS.NS"), ("Hero MotoCorp", "HEROMOTOCO.NS"), ("Bajaj Auto", "BAJAJ-AUTO.NS"), ("Mahindra", "M&M.NS"), ("TVS", "TVSMOTOR.NS"), ("Ashok Leyland", "ASHOKLEY.NS"), ("Escorts", "ESCORTS.NS"), ("Eicher Motors", "EICHERMOT.NS"), ("Sona", "SONA.NS")],
    "📱 Telecom": [("Airtel", "BHARTIARTL.NS"), ("Jio Finance", "JIOFIN.NS"), ("Vodafone Idea", "VODAFONEIDEA.NS"), ("Tejas Networks", "TEJASNET.NS"), ("HFCL", "HFCL.NS"), ("Sterlite", "STL.NS")],
    "🏥 Pharma": [("Sun Pharma", "SUNPHARMA.NS"), ("Dr Reddy's", "DRREDDY.NS"), ("Cipla", "CIPLA.NS"), ("Divi's Lab", "DIVISLAB.NS"), ("Aurobindo", "AUROBINDO.NS"), ("Lupin", "LUPIN.NS"), ("Biocon", "BIOCON.NS"), ("Cadila", "CADILAHC.NS"), ("Torrent", "TORNTPOWER.NS"), ("Abbott India", "ABBOTINDIA.NS")],
    "🛍️ Retail": [("DMart", "DMART.NS"), ("Trent", "TRENT.NS"), ("Shoppers Stop", "SHOPERSTOP.NS"), ("Future Retail", "FUTURERETAIL.NS"), ("Titan", "TITAN.NS"), ("V-Mart", "VMART.NS"), ("Varun Beverages", "VBL.NS"), ("Reliance Retail", "RELIANCERETAIL.NS"), ("Pantaloons", "PANTALOONS.NS"), ("Arvind", "ARVIND.NS")]
}

# Sidebar sector and display selection
st.sidebar.subheader("🔍 Explore by Sector")
selected_sector = st.sidebar.selectbox("Select Sector", list(sectors.keys()))
company_list = sectors[selected_sector]
company_display = [c[0] for c in company_list]
selected_display = st.sidebar.selectbox("Select Company", company_display)
ticker_map = {c[0]: c[1] for comp in sectors.values() for c in comp}
selected_ticker = ticker_map.get(selected_display)

if selected_sector == "🌐 Overall Summary":
    st.subheader("📊 Market Summary")
    top_stocks = ["AAPL", "GOOGL", "MSFT", "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
    cols = st.columns(len(top_stocks))
    for i, ticker in enumerate(top_stocks):
        stock = yf.Ticker(ticker)
        info = stock.info
        name = info.get("shortName", ticker)
        price = info.get("currentPrice", 0)
        prev = info.get("previousClose", 0)
        change = price - prev
        pct = (change / prev * 100) if prev else 0
        cols[i].metric(label=name, value=f"₹ {price}", delta=f"{pct:.2f}%")

    index_ticker = yf.Ticker("^NSEI")
    index_data = index_ticker.history(period="5d", interval="1h")
    if not index_data.empty:
        fig = px.line(index_data, x=index_data.index, y="Close", title="📈 Nifty 50 - 5 Day Trend")
        st.plotly_chart(fig, use_container_width=True)

elif selected_ticker:
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🌐 Overall Market Summary:**")
    for name, ticker in [("Apple", "AAPL"), ("Google", "GOOGL"), ("Microsoft", "MSFT"), ("Reliance", "RELIANCE.NS"), ("TCS", "TCS.NS")]:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("currentPrice", 0)
        st.sidebar.write(f"{name}: ₹{price}")

    stock = yf.Ticker(selected_ticker)
    info = stock.info
    name = info.get("longName", selected_display).replace(f" ({selected_ticker})", "")
    st.markdown(f"## {name}")

    col1, col2 = st.columns(2)
    with col2:
        st.markdown(f"<p class='small-text'>🔗 <a href='https://finance.yahoo.com/quote/{selected_ticker}?p={selected_ticker}' target='_blank'>Click here to view full stock page</a></p>", unsafe_allow_html=True)
        df = stock.history(period="5d", interval="1h")
        if not df.empty:
            fig = px.line(df, x=df.index, y="Close", title=f"{selected_display} - 5 Day Price Trend")
            st.plotly_chart(fig, use_container_width=True)

    with col1:
        price = info.get("currentPrice", 0)
        prev = info.get("previousClose", 0)
        change = price - prev
        pct = (change / prev * 100) if prev else 0
        st.metric("Current Price", f"₹ {price}", delta=f"{pct:.2f}%")
        st.markdown(f"**Sector**: {info.get('sector', 'N/A')}")
        st.markdown(f"**Market Cap**: {info.get('marketCap', 'N/A')}")
        st.markdown("#### Company Overview")
        summary = info.get("longBusinessSummary", "No info available")
        st.info(summary[:300] + ("..." if len(summary) > 300 else ""))
