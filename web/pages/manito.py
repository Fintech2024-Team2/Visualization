import streamlit as st

def show():
    st.title("마니또")
    st.write("당신의 마니또를 검색하세요!")

    search_query = st.text_input('마니또 검색')
    if search_query:
        search_results = [node for node in G.nodes if search_query in node]
        if search_results:
            st.subheader('검색 결과:')
            for result in search_results:
                st.write(result)
        else:
            st.write('검색 결과가 없습니다.')
    
    st.write("마니또 검색하면 뭐가 나오게 하면 좋을까용")
    st.write("마니또 데이터프레임도 만들어야 해요")

# 이 함수는 페이지를 실행할 때 호출됩니다.
if __name__ == "__main__":
    show()