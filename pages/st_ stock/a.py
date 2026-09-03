import streamlit as st
import yfinance
from pprint import pprint

def get_stock_info(stock):
    yf = yfinance.Ticker(stock)    # 基本用法
    st.write(f'{stock} 的詳細資料如下：')
    st.write(f'{stock} 的開盤價：{yf.fast_info["open"]}')
    st.write(f'{stock} 的收盤價：{yf.fast_info["previousClose"]}')
    st.write(f'{stock} 單日最高價：{yf.fast_info["dayHigh"]}')
    st.write(f'{stock} 單日最低價：{yf.fast_info["dayLow"]}')





st.page_link("pages/st_project.py", label="返回專題頁面", icon="📚")

with st.sidebar:
    st.title("股票選擇")
    # select_radio = st.radio("選擇股票:", ["2330.TW", "2317.TW", "2454.TW", "3008.TW", "2412.TW"])
    select_box = st.selectbox("選擇股票:", ["2330.TW", "2317.TW", "2454.TW", "3008.TW", "2412.TW"])

# st.subheader(f"選擇的股票:{select_radio}")
st.subheader(f"選擇的股票:{select_box}")

# 呼叫函數
get_stock_info(select_box)


