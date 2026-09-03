import streamlit as st
import time

st.page_link("pages/st_project.py", label="返回專題頁面", icon="📚")
st.title("專題頁面4-社會分析")


placeholder = st.empty()

# 倒數計時 10 秒
for i in range(5, 0, -1):
    placeholder.info(f"⏱️ 將在 {i} 秒後自動返回主頁...")
    time.sleep(1)

# 清除倒數訊息並切換頁面
placeholder.empty()


st.switch_page("pages/st_project.py")  # 💡 請替換成您指定頁面的路徑