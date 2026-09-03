import streamlit as st

st.title("專題總覽")


with st.sidebar:
    st.title("專題介紹")
    st.write("使用工具。")
    st.page_link("pages/st_project.py", label="專題頁面", icon="📚")
    st.page_link("pages/st_project1.py", label="專題頁面1-商業分析", icon="📊")
    st.page_link("pages/st_project2.py", label="專題頁面2-科學分析", icon="🔬")
    st.page_link("pages/st_project3.py", label="專題頁面3-氣象分析", icon="🌤️")
    st.page_link("pages/st_project4.py", label="專題頁面4-社會分析", icon="🌏")
    st.page_link("pages/st_ stock/b.py", label="專題頁面5-股票分析", icon="📈")
    st.divider()
    st.page_link("pages/st_home.py", label="首頁", icon="🏠")
    st.page_link("pages/st_me.py", label="自我介紹", icon="👤")
    st.page_link("https://github.com/", label="我的GitHub頁面", icon="🐙")
    st.divider()
    st.caption("版本：v1.0.0")