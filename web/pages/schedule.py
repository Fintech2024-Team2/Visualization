import streamlit as st
import pandas as pd

def show():
    st.title("워크숍 주요 일정")

    # 주요 일정 데이터
    schedule_data = {
        "날짜": [
            "8.12", "8.12", "8.12", "8.12", "8.12", "8.13", "8.13", "8.13", "8.13"
        ],
        "시간": [
             "10:00", "12:00", "14:00", "19:00", "22:00",  "07:00", "08:30", "11:30", "13:00"
        ],
        "일정": [
            "버스 출발", 
            "횡성축협 점심", 
            "교육 및 캡스톤 케이스 스터디", 
            "OX 퀴즈 및 미니 체육대회", 
            "술(조별로)", 
            "기상",
            "강의 시작(이재욱 교수님 특강)", 
            "오대산 도착 및 등산",
            "점심식사"
        ]
    }

    df_schedule = pd.DataFrame(schedule_data)

    # Streamlit에서 일정 표시
    for date in df_schedule['날짜'].unique():
        st.subheader(f"{date}")
        day_schedule = df_schedule[df_schedule['날짜'] == date]
        for index, row in day_schedule.iterrows():
            st.markdown(f"**{row['시간']}** - {row['일정']}")

# 이 함수는 페이지를 실행할 때 호출됩니다.
if __name__ == "__main__":
    show()
