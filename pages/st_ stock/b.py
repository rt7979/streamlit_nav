#  uv run streamlit run "pages\st_ stock\b.py" --server.port 8502


import streamlit as st
import yfinance as yf
from pathlib import Path




st.set_page_config(page_title="股票分析台", page_icon="📈", layout="wide")


def load_styles():
    style_path = Path(__file__).resolve().parents[2] / "static" / "style.css"
    st.markdown(f"<style>{style_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


@st.cache_data(ttl=900)
def get_stock_info(stock):
    return yf.Ticker(stock).history(period="6mo", auto_adjust=False)


def format_price(value):
    return "--" if value is None else f"{value:,.2f}"


load_styles()

stocks = {
    "台積電 · 2330.TW": "2330.TW",
    "鴻海 · 2317.TW": "2317.TW",
    "聯發科 · 2454.TW": "2454.TW",
    "大立光 · 3008.TW": "3008.TW",
    "中華電 · 2412.TW": "2412.TW",
}

with st.sidebar:
    st.markdown("<div class='sidebar-brand'>MARKET<br><span>VIEW</span></div>", unsafe_allow_html=True)
    st.markdown("### 觀察清單")
    selected_name = st.selectbox("選擇股票", list(stocks), label_visibility="collapsed")
    selected_stock = stocks[selected_name]
    st.divider()
    st.caption("資料來源：Yahoo Finance")

st.markdown(
    f"""
    <div class='stock-hero'>
        <div>
            <div class='eyebrow'>TAIWAN EQUITY / 06 MONTHS</div>
            <h1>{selected_name.split(' · ')[0]}</h1>
            <p>即時掌握價格趨勢與市場動能</p>
        </div>
        <div class='ticker-badge'>{selected_stock}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    data = get_stock_info(selected_stock)
except Exception as error:
    st.error(f"目前無法取得 {selected_stock} 的資料：{error}")
    st.stop()

if data.empty:
    st.warning("目前沒有可顯示的市場資料，請稍後再試。")
    st.stop()

latest = data.iloc[-1]
previous = data.iloc[-2] if len(data) > 1 else latest
change = latest["Close"] - previous["Close"]
change_percent = (change / previous["Close"] * 100) if previous["Close"] else 0
high_period = data["High"].max()
volume = latest["Volume"]

st.markdown("<div class='section-label'>MARKET SNAPSHOT</div>", unsafe_allow_html=True)
metric_columns = st.columns(5)
metrics = [
    ("最新收盤", f"NT$ {format_price(latest['Close'])}", f"{change:+,.2f} ({change_percent:+.2f}%)", change >= 0),
    ("今日開盤", f"NT$ {format_price(latest['Open'])}", "當日第一筆成交價", None),
    ("今日最高", f"NT$ {format_price(latest['High'])}", "當日價格區間", None),
    ("六個月高點", f"NT$ {format_price(high_period)}", "期間最高收盤價", None),
    ("成交量", f"{volume:,.0f}", "最新交易日", None),
]
for column, (label, value, detail, positive) in zip(metric_columns, metrics):
    tone = "up" if positive is True else "down" if positive is False else "neutral"
    column.markdown(
        f"<div class='metric-card {tone}'><div class='metric-label'>{label}</div>"
        f"<div class='metric-value'>{value}</div><div class='metric-detail'>{detail}</div></div>",
        unsafe_allow_html=True,
    )

st.markdown("<div class='section-label chart-label'>PRICE & VOLUME</div>", unsafe_allow_html=True)
chart_column, range_column = st.columns([2.2, 1])
with chart_column:
    st.markdown("<div class='chart-title'>收盤價走勢 <span>近六個月</span></div>", unsafe_allow_html=True)
    st.line_chart(data[["Close"]].rename(columns={"Close": "收盤價"}), color="#f4b860", height=330)
with range_column:
    st.markdown("<div class='chart-title'>每日成交量 <span>交易活躍度</span></div>", unsafe_allow_html=True)
    st.bar_chart(data[["Volume"]].rename(columns={"Volume": "成交量"}), color="#67c7b5", height=330)

with st.expander("查看原始交易資料"):
    display_data = data[["Open", "High", "Low", "Close", "Volume"]].copy()
    display_data.columns = ["開盤", "最高", "最低", "收盤", "成交量"]
    st.dataframe(display_data.sort_index(ascending=False), use_container_width=True)
    st.download_button(
        "下載 CSV",
        data.to_csv().encode("utf-8-sig"),
        file_name=f"{selected_stock}_market_data.csv",
        mime="text/csv",
        icon="⬇️",
    )


