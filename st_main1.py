import streamlit as st



pages = [st.Page("pages/st_home.py", title="首頁", icon="🏠"), 
         st.Page("pages/st_project.py", title="專題頁面", icon="📚"),
         st.Page("pages/st_me.py", title="自我介紹", icon="👤")]

panav = st.navigation(pages = pages, position ="top")   # sidebar, top, hidden

panav.run()


