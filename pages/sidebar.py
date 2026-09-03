import streamlit as st

# ==========================================
# 1. 共用功能：側邊欄
# ==========================================
def render_sidebar():
    with st.sidebar:
        st.title("功能導覽")
        st.page_link("psges/st_home.py", label="首頁", icon="🏠")
        st.page_link("pages/st.porject.py", label="分頁 (Tabs)", icon="📊")
        st.write("使用工具")
        st.divider()
        st.caption("版本：v1.0.0")





# def render_sidebar():
#     """共用的側邊欄元件"""
#     with st.sidebar:
#         st.title("導覽選單")
#         st.write("歡迎使用本系統")
#         st.divider()
        
#         # 【修正】使用安全的路徑宣告，避免分頁載入時路徑出錯導致後續元件中斷
#         st.page_link("streamlit_web.py", label="首頁", icon="🏠")
#         st.page_link("pages/streamlit_tabs.py", label="分頁 (Tabs)", icon="📊")
        
#         st.divider()

#         with st.expander("下拉選單"):
#             st.write("可以放置選項、按鈕等元件。")
#             # 加上唯一的 key="sidebar_b1"
#             b1 = st.button("點擊我開啟tabs頁面", key="sidebar_b1")
#             if b1:
#                 st.switch_page("pages/streamlit_tabs.py")
            
    
#         st.divider()

#         st.subheader("專案標題1。")
#         st.write("內容介紹1。")
#         # 加上唯一的 key="sidebar_b2"
#         st.button("點擊我1", key="sidebar_b2")

#         st.divider()

#         st.subheader("專案標題2。")
#         st.write("內容介紹2。")
#         # 加上唯一的 key="sidebar_b3"
#         st.button("點擊我2", key="sidebar_b3")

#         st.divider()
#         st.caption("版本：v1.0.0")