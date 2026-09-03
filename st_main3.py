import streamlit as st



menulist = {
    "個人頁面": [
        st.Page("pages/st_home.py", title="首頁", icon="🏠"), 
        st.Page("pages/st_me.py", title="自我介紹", icon="👤")
        ],
    "專題頁面": [
        st.Page("pages/st_project.py", title="專題總覽", icon="📚"),
        st.Page("pages/st_project1.py", title="專題頁面1-商業分析", icon="📊"),
        st.Page("pages/st_project2.py", title="專題頁面2-科學分析", icon="🔬"),
        st.Page("pages/st_project3.py", title="專題頁面3-氣象分析", icon="🌤️"),
        st.Page("pages/st_project4.py", title="專題頁面4-社會分析", icon="🌐") 
    ],
    "股票分析": [
            st.Page("pages/st_ stock/a.py", title="持股股份", icon="📈"),
            st.Page("pages/st_ stock/b.py", title="股票歷史資訊", icon="📉")
            ],
    "網站連結": [
        st.Page("https://github.com/", title="我的GitHub頁面", icon="🐙"),
        st.Page("https://www.ebus.com.tw/RideInfo/TicketPrices", title="公車票價查詢", icon="🚌"),
        st.Page("https://www.google.com.tw/maps", title="Google Maps", icon="🗺️")
        ]}


panav = st.navigation(pages = menulist, position ="top")   # sidebar, top, hidden

panav.run()


