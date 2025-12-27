import streamlit as st
import pandas as pd
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="TOP SECRET", page_icon="🕵️", layout="centered")

# 2. 제목 꾸미기
st.title("🏫 중앙중 도둑 검거 계획에 당신의 도움이 필요합니다")
st.write("저는 중앙중의 대도(大盜)를 잡기 위해 비밀조직으로부터 연락을 받고 온 탐정입니다.\n2025년 12월...꽤나 오래전부터 학생들의 소중한 '이것'을 훔쳐온 도둑이 바로 이 학교 내부에 있다는걸 밝혀냈습니다. \n교직원분들꼐서도 용의자로 지목되는것은 당연합니다...이 사건은 1급 기밀로 조사가 이루어지기 때문에 안심하십시오. 만약 범인이 아니시라면 보내드리도록 하겠습니다.")

# 3. 비밀번호(API 키) 가져오기
# 내 컴퓨터(secrets.toml)나 웹사이트(Streamlit Cloud)에서 키를 안전하게 가져옴
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error("탐정이 정신줄이 나가 쓰러졌다.")
    st.stop()

# 4. 구글 시트 데이터 가져오기 (CSV URL 방식)
# 아까 2단계에서 복사한 '웹에 게시' 링크를 아래에 넣어야 해!
# 따옴표 안에 링크를 바꿔줘!!!
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGKogkCFcPfKPdqsG9FAywjX61yoGh4CE_mizBxNucuCKL5Btzd2Ndppe8L9-a1J5H4FalkvT1RVA4/pub?output=csv"

@st.cache_data # 데이터를 자꾸 불러오면 느리니까 저장해두는 기능
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        return None

df = load_data()

if df is not None:
    # 5. 선생님 선택 상자 만들기
    # 데이터프레임에서 '이름' 열을 가져와서 선택지로 줌
    teacher_name = st.selectbox("당신을 용의자로서 심문하겠습니다. 성명을 말해주십시오.", df['담당자'])

    # 선택한 선생님의 정보 찾기
    teacher_info = df[df['담당자'] == teacher_name].iloc[0]
    subject = teacher_info['교과']
    work = teacher_info['담당업무']
    classes = teacher_info['담임']
    workplace = teacher_info['부서명']

    # 6. 버튼 누르면 제미나이한테 시키기
    if st.button("아부 떨기 시작! ✨"):
        with st.spinner("당신이 순수한 선생님일지, 아니면 "):
            
            # AI한테 줄 명령(프롬프트)
            prompt = f"""
            너는 비밀조직의 지시를 받고 중앙중 내 도난사건을 1급 기밀로 수사하기 위해 온 탐정이야.
            엄청난 아첨과 입발린 말, 칭찬능력을 가지고 있고 활기찰 필요는 없고 중년 아재의 말투야.
            
            선생님 정보:
            - 담당자: {teacher_name} 선생님
            - 담당 과목: {subject}
            - 담당업무: {work}
            - 담임: {classes}
            - 부서명: {workplace}
            
            이 정보를 바탕으로 선생님이 들으면 기분 좋아서 당장 나한테 찾아오고 싶어질만한
            엄청난 칭찬과 아부 멘트를 4줄 정도로 작성해줘.
            말투는 중앙중학교 내 일어난 도난사건을 1급 기밀사건으로써 수사하러 온 탐정의 말투로 해줘.
            조사하러 왔기 때문에 진지하지만 해당 선생님의 엄청난 '능력', '인기', '지능'에 어쩔수없이 감탄의 말이 흘러나오는 상황이야.
            용의자 심문하러 왔는데 엄청난 '최고의 선생님'을 만나게되자 매우 놀란듯한 말투를 써줘.
            마지막에는 '이런 대단한 선생님이 중앙중에 있다니, 학생들은 도난의 두려움에 떨기 전에 영광의 떨림을 마주했겠습니다...'라는 존나 엄청난 아첨을 갈겨줘.
            """
            
            # 제미나이 모델 호출 (가장 빠른 flash 모델 사용)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # 결과 보여주기
            st.success(f"{teacher_name}선생님...? 그 소문으로만 듣던 '최고의 선생님' 아니십니까? \n이럴수가...조사해보니 역시나 엄청난 분이십니다.")
            st.write(response.text)
            st.balloons() # 풍선 날리기 효과

else:
    st.error("이런! 조사자료가 바람에 날라가서 탐정이 당황했다.")