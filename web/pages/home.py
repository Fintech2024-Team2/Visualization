import streamlit as st

def show():
    st.title("HOME")
    st.write("반갑습니다!")
    st.write("저희는 워크숍에서 찍은 사진을 이용해 시간 순서대로 인물 간 관계 그래프를 시각화 해보았습니다.")
    st.write("왼쪽 사이드바에서 다른 메뉴를 선택해보세요 :>")

# 이 함수는 페이지를 실행할 때 호출됩니다.
if __name__ == "__main__":
    show()