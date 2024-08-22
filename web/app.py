import streamlit as st
from pages import home, gallery, graph, manito, search

# Streamlit 사이드바 메뉴
st.sidebar.title("메뉴")
menu_selection = st.sidebar.selectbox("메뉴 선택", ("HOME", "갤러리", "인물 관계도", "마니또", "인물 검색"))

# 각 페이지로 라우팅
if menu_selection == "HOME":
    home.show()
elif menu_selection == "갤러리":
    gallery.show()
elif menu_selection == "인물 관계도":
    graph.show()
elif menu_selection == "마니또":
    manito.show()
elif menu_selection == "인물 검색":
    search.show()
