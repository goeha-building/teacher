import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
import streamlit.components.v1 as components

# 1. 페이지 설정 (레이아웃 설정)
st.set_page_config(page_title="TOP SECRET OF JUNGANG", page_icon="🕵️", layout="wide")

# ==========================================
# [스타일 & 함수 설정]
# ==========================================

# 배경화면 변경 함수 (가독성 위해 꺼둠)
def set_bg(image_file):
    pass

# 스크롤 긴장감을 위한 빈 공간 함수
def spacer(height=50):
    for _ in range(height):
        st.write("")

# 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 0 # 0:입력, 1:아첨, 2:긴장, 3:결말
if 'teacher_name' not in st.session_state:
    st.session_state.teacher_name = ""
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = ""
if 'animation_played' not in st.session_state:
    st.session_state.animation_played = False

# API 연결
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("탐정이 뇌손상 당했다능!! secrets.toml을 확인하세요.")

# 데이터 로드
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRGKogkCFcPfKPdqsG9FAywjX61yoGh4CE_mizBxNucuCKL5Btzd2Ndppe8L9-a1J5H4FalkvT1RVA4/pub?output=csv"

# 강제 스크롤 함수
def js_scroll_top():
    components.html(
        """
            <script>
                setTimeout(function(){
                    window.parent.scrollTo({top: 0, behavior: 'instant'});
                    var elements = window.parent.document.querySelectorAll('*');
                    for (var i = 0; i < elements.length; i++) {
                        if (elements[i].scrollTop > 0) {
                            elements[i].scrollTop = 0;
                        }
                    }
                }, 100);
            </script>
        """,
        height=0
    )

@st.cache_data(ttl=600) 
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df['담당자'] = df['담당자'].astype(str).str.strip()
        return df
    except Exception:
        return None

df = load_data()

# ==========================================
# [STEP 0] 탐정 등장 & 이름 입력
# ==========================================
if st.session_state.step == 0:
    set_bg("bg_school.png")

    st.title("🕵️ 중앙중 대도(大盜) 검거계획 : 당신의 도움이 필요합니다")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        try:
            st.image("detective1.png", width="stretch")
        except:
            st.write("🕵️ (탐정 이미지)")
            
    with col2:
        st.write("### 안녕하십니까, 중앙중학교 교직원 여러분.")
        st.write("저는 대통령도 모르는 비밀조직의 의뢰를 받고 잠입한 **비밀탐정**입니다.")
        st.write("최근 이 학교에서 소중한 **이것**이 마구 도난당했다는 1급 기밀 제보가 들어왔습니다.")
        st.write("보안을 위해 지금부터의 일은 철저히 비밀로 해주십시오. 이 도둑은 아주 오랫동안 잡히지 않은 베테랑입니다...")
        st.info("범인은... 바로 이 학교 내부에 있습니다. 조용히 협조해 주신다면 용의자 선에서 끝날 것입니다.")

    st.write("---")
    st.write("### 🚨 신원 확인")
    
    input_name = st.text_input("성함을 정확하게 입력해 주십시오. (외자 이름은 성과 이름을 띄우시고 동명이인은 이름 뒤 과목명을 붙이십시오 예: 홍길동 역사)", placeholder="입력 후 ENTER")
    
    if input_name:
        input_name = input_name.strip()
        
        if df is not None and input_name in df['담당자'].values:
            teacher_data = df[df['담당자'] == input_name].iloc[0]
            
            with st.spinner(f"'{input_name}' 선생님을 용의자로서 조사중입니다...아니, 이럴수가...!"):
                prompt = f"""
                너는 중앙중학교 도난사건을 수사하러 온 진지한 중년 탐정이야.
                용의자인 줄 알고 '{input_name}' 선생님을 조사했는데,
                알고보니 담당과목 '{teacher_data['교과']}', 부서 '{teacher_data['부서명']}'에서
                너무나 완벽하고 훌륭한 선생님이라서 깜짝 놀라는 상황이야.
                
                탐정 말투로 매우 당황하며, 이 선생님의 능력과 인품을 4~5줄로 극찬해줘.
                "이런 분을 의심하다니 내 불찰이군..." 같은 느낌으로 시작해.
                ()를 써서 생각을 표현하는 말투는 지양해줘. 엄청난 아첨을 한다는 생각으로 말해.
                """
                
                # --- [여기가 형이 실수했던 부분!! 고쳤음!!] ---
                try:
                    model = genai.GenerativeModel('gemini-flash-latest')
                    response = model.generate_content(prompt)
                    
                    # 성공하면 여기서 바로 저장하고 넘어가야 함! (try 안으로 이사옴)
                    st.session_state.teacher_name = input_name
                    st.session_state.ai_response = response.text
                    st.session_state.step = 1
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"갑자기 메테오가 떨어져 탐정이 기절했습니다. 당장 비밀요원의 치료가 필요합니다.")
                    st.stop()
                # ---------------------------------------------
                
        else:
            st.error("🚨 용의자 명단에 이름이 없으시군요. 성함을 정확히 적으셨습니까?")

# ==========================================
# [STEP 1] 아첨 폭격 & 탐정 놀람
# ==========================================
elif st.session_state.step == 1:
    set_bg("bg_school.jpg")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        try:
            st.image("detective2.png", caption="!!!", width="stretch")
        except:
            st.header("😲")

    with col2:
        st.success(f"**{st.session_state.teacher_name}** 선생님...? 당신이 중앙중 내 소문이 자자한 그 '최고의 선생님' 이셨습니까..?")
        st.write(st.session_state.ai_response)
    
    st.write("---")
    
    if st.button(f"흠흠.. 제가 바로 그 최고의 선생님 {st.session_state.teacher_name} 입니다."):
        st.session_state.step = 2
        st.rerun()

# ==========================================
# [STEP 2] 긴장감 조성
# ==========================================
elif st.session_state.step == 2:
    set_bg("bg_school.jpg")
    
    st.title("📞 띠리리리리링 따르르릉땡띵 링딩동동!!!!!!!!")

    st.error("잠시만요 선생님. 본부에서 연락이 왔습니다...")
    st.write("범인이 누군지 밝혀내었다고 합니다!! 위치까지 알아냈다는군요!")
    st.write("범인의 정체를 들었을땐 너무나 충격적이고 예상 밖이었습니다만...")
    st.write("범인이 훔친 것이 '이것' 이라는 말을 들었을 땐 너무나 당연하다는 생각이 들었습니다, 하하")
    st.write("어쩌면 지금 당장 범인을 체포할 수도 있겠습니다!!")
    spacer(7)
    st.write("범인의 정체를 알고 싶으십니까...?")
    
    spacer(10)
    st.markdown("<h3 style='text-align: center; color: gray;'>범인은...</h3>", unsafe_allow_html=True)
    spacer(10)
    st.markdown("<h3 style='text-align: center; color: gray;'>중앙중학교 안에 있었습니다.</h3>", unsafe_allow_html=True)
    spacer(20)
    st.markdown("<h3 style='text-align: center; color: red;'>범인은... 바로...</h3>", unsafe_allow_html=True)
    spacer(30)
    st.markdown("<h3 style='text-align: center; color: red;'>지금 이순간에도, 우리로부터 아주 가까이에 있습니다.</h3>", unsafe_allow_html=True)
    spacer(10)
    
    if 'reveal_criminal' not in st.session_state:
        st.session_state.reveal_criminal = False

    if st.button("📩 중앙중의 대도(大盜) 정체 확인하기"):
        st.session_state.reveal_criminal = True

    if st.session_state.reveal_criminal:
        st.warning(f"범인은...{st.session_state.teacher_name} 선생님. 바로 당신입니다!!!!!!")
        
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("저는 아무짓도 하지 않았어요!"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.button("배상할테니 한번만 봐주세요."):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.button("억울해요! 무고죄로 고소할게요!!"):
                st.session_state.step = 3
                st.rerun()

# ==========================================
# [STEP 3] 반전 & 검거 완료
# ==========================================
elif st.session_state.step == 3:
    js_scroll_top()
    set_bg("bg_cheer.jpg")
    
    # --- [애니메이션 1회 재생 로직] ---
    if not st.session_state.animation_played:
        st.balloons()
        st.snow()
        st.session_state.animation_played = True
    # --------------------------------
    
    st.title("🎉 검거 완료 : 당신은 체포되었습니다!")
    try:
        st.image("detective3.png", width="stretch")
    except:
        pass
    
    st.markdown(f"""
    <div style='text-align: center;'>
        <h2>{st.session_state.teacher_name} 선생님, 당신이 바로 그 '대도(大盜)' 입니다!</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("억울하십니까 선생님? 하지만 당신은 확실한 중앙중의 **도둑**이십니다.")
    spacer(5)
    st.write("아직도 모르시겠습니까...?")
    spacer(5)
    st.write(f"**{st.session_state.teacher_name}** 선생님...")
    spacer(7)
    st.write("당신이 모든 학생들과 교직원들에게서...")
    spacer(15)
    st.header("💘'마음'을 훔치셨지 않습니까????❤️❤️❤️❤️")
    
    st.markdown(f"""
    <div style='background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px; text-align: center;'>
        <p>모두의 마음과 시선을 빼앗는 당신의 매력과 능력...</p>
        <p>중앙중의 모두가 {st.session_state.teacher_name}선생님에게서 헤어나오지 못하는 그야말로 초위기 상황이었습니다만...</p>
        <p>이제 모든게 밝혀졌습니다.</p>
        <p>당신은 저희 비밀조직이 그토록 찾던 무시무시한 <b>'❤️사랑의 도둑❤️'</b>입니다!</p>
        <p>(여기서 감동받으셔야합니다.)</p>
        <p style='color: red; font-weight: bold;'>처벌은 '중앙중 학생들의 영원한 존경과 응원' 입니다.</p>
        <h3>❤️❤️❤️각오하십시오!!!!! ❤️❤️❤️</h3>
    </div>
    """, unsafe_allow_html=True)
    
    spacer(3)
    
    st.write("---")
    st.subheader("비밀요원의 비밀업무 평가하기")
    try:
        st.image("평가저씨.jpg", width=400)
    except:
        pass
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("재밌다! 제작자를 응원한다~ ^_^"):
            st.toast("감사합니다. 정진하는 비밀요원이 되겠습니다.")
    with c2:
        if st.button("노잼 그자체. 과고 면접 광탈한 이유를 알겠다"):
            st.toast("죄송합니다. 반성하는 비밀요원이 되겠습니다.")

    st.caption(f"제작자 : 중앙중 비밀요원(정체는 비밀입니다)")
    st.caption(f"평가내용은 절대 저장되거나 비밀조직의 손에 넘어가지 않습니다.")
    
    if st.button("처음으로🔄"):
        st.session_state.step = 0
        st.session_state.teacher_name = ""
        st.session_state.reveal_criminal = False # 범인 확인 버튼 상태 초기화
        # 애니메이션 다시 재생되도록 초기화
        if 'animation_played' in st.session_state:
            del st.session_state.animation_played
        st.rerun()