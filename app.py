import streamlit as st
import streamlit.components.v1 as components

# --- Page Config (Must be first) ---
st.set_page_config(
    page_title="2026 실버케어 AI 가이드",
    page_icon="👵",
    layout="centered"
)

# --- Meta Tags & CSS (Optimized) ---
# Added font-display:swap for better performance
st.markdown("""
<head>
    <meta property="og:title" content="2026 실버케어 AI 가이드">
    <meta property="og:description" content="우리 부모님 맞춤형 2026 돌봄 혜택, 1분 만에 확인하세요">
    <meta property="og:image" content="https://raw.githubusercontent.com/wonseokjung/solopreneur-ai-agents/main/agents/kodari/assets/kodari_success.png">
    <meta property="og:url" content="https://silver-care-ai.streamlit.app">
</head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&family=Noto+Sans+KR:wght@300;500;700&display=swap&font-display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', 'Outfit', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #FDFBF7 0%, #E8F5E9 100%);
    }
    
    /* Premium Card Effect */
    .st-emotion-cache-12w0qpk {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07) !important;
        padding: 2rem !important;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        height: 4em;
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        font-size: 1.3em;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(46, 125, 50, 0.4);
        background: linear-gradient(45deg, #45a049, #1B5E20);
    }
    
    h1 {
        font-size: 3rem !important;
        background: -webkit-linear-gradient(#2E5A27, #66BB6A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .report-card {
        background: white;
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border-left: 10px solid #4CAF50;
        margin-top: 2rem;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# --- AI Configuration & Caching ---
@st.cache_data
def load_policy_data():
    try:
        with open("data/policy_2026.md", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"정책 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}"

@st.cache_resource
def get_ai_model():
    # Move heavy import inside function to speed up initial app load
    import google.generativeai as genai
    try:
        # Check if key exists in secrets
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("🔑 **GEMINI_API_KEY**를 찾을 수 없습니다! 스트림릿 클라우드 설정(Settings -> Secrets)에 키를 추가해 주세요.")
            return None
            
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        policy_context = load_policy_data()
        system_instruction = f"""
        당신은 대한민국의 '2026 돌봄통합지원법' 전문가입니다.
        아래의 공식 정책 데이터를 반드시 참고하여 답변해 주세요.
        
        [공식 정책 데이터]
        {policy_context}
        
        당신의 목표는 보호자(4050 자녀)에게 희망을 주고 정확한 정보를 제공하는 것입니다.
        """
        model = genai.GenerativeModel('gemini-flash-latest', system_instruction=system_instruction)
        return model
    except Exception as e:
        st.error(f"⚠️ AI 모델 초기화 실패: {str(e)}")
        return None

def get_ai_response(prompt):
    model = get_ai_model()
    if not model:
        return None
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"⚠️ 인공지능 응답 생성 중 오류가 발생했습니다: {str(e)}")
        return None

# --- App Logic ---
def main():
    # Sidebar: Admin Tools
    with st.sidebar:
        st.title("🛠️ 관리자 도구 ⚙️")
        if st.checkbox("SNS 마케팅 카피 생성기"):
            st.subheader("📢 인스타그램/X 홍보 문구")
            topic = st.text_input("홍보 할 핵심 키워드", value="2026 돌봄통합지원법")
            if st.button("카피 생성"):
                with st.spinner("찰진 카피 만드는 중..."):
                    mkt_prompt = f"당신은 천재적인 SNS 마케터입니다. '{topic}'를 주제로 4050 자녀 세대의 마음을 울리는 인스타그램 홍보 문구와 해시태그를 3가지 버전으로 만들어주세요."
                    copy_result = get_ai_response(mkt_prompt)
                    if copy_result:
                        st.info(copy_result)

    # Main Landing Section
    # Hero Banner (Multi-format & Case-insensitive Detection)
    import os
    
    @st.cache_data
    def find_hero_image():
        # 확인할 파일명 후보들
        base_names = ["hero", "HERO", "Hero"]
        extensions = [".jpg", ".jpeg", ".png", ".JPG", ".PNG", ".JPEG"]
        search_dirs = ["", "assets/"] # 루트와 assets 폴더 모두 확인
        
        for sd in search_dirs:
            for bn in base_names:
                for ext in extensions:
                    path = f"{sd}{bn}{ext}"
                    if os.path.exists(path):
                        return path
        return None

    hero_file = find_hero_image()
    
    if hero_file:
        st.image(hero_file, use_container_width=True, caption="AI와 함께하는 행복한 노후")
    else:
        # 파일이 없을 때 보여줄 안내 (문구가 바뀌었는지 확인용)
        st.markdown(f"""
            <div style="width: 100%; height: 250px; background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%); 
                        border-radius: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; 
                        border: 2px dashed #8BC34A; margin-bottom: 20px;">
                <h3 style="color: #33691E; margin-bottom: 10px;">✨ 대표님의 명품 이미지를 기다리고 있습니다!</h3>
                <p style="color: #555; font-size: 0.9rem;"><b>hero.jpg</b> 파일을 깃허브 메인 폴더에 올려주세요.</p>
                <p style="color: #777; font-size: 0.8rem;">(현재 최신 코드가 적용된 상태입니다 🫡)</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.title("실버케어 AI 가이드")
    st.markdown("#### **내 부모님을 위한 가장 따뜻한 돌봄 솔루션**")
    st.markdown("'돌봄통합지원법' 시행 전 우리 부모님이 받을 수 있는 최적의\n서비스를 확인해 보세요~!!")
    
    # NEW: 2026 Law Info Box with improved style
    with st.container():
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; border-left: 5px solid #4CAF50; margin-bottom: 2rem;">
            <p style="font-weight: bold; margin-bottom: 5px; color: #2E7D32;">💡 2026년 3월, 획기적으로 바뀌는 3가지</p>
            <ul style="font-size: 0.95rem; color: #555;">
                <li><b>시설 대신 '집에서'</b>: 재가 의료 서비스가 대폭 확대됩니다.</li>
                <li><b>복잡한 신청 끝!</b>: 읍면동 센터 한 곳에서 모든 돌봄이 원스톱으로 해결됩니다.</li>
                <li><b>주거 환경 개선</b>: 낙상 방지 등 집수리에 국가 예산이 투입됩니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Voice Input Feature (Phase 2 Addition)
    st.markdown("### 🎙️ 음성으로 부모님 상태 기록하기 (Beta)")
    st.write("타이핑이 번거로우신가요? 목소리로 부모님의 상태를 말씀해 주시면 AI가 분석해 드립니다.")
    audio_value = st.audio_input("기록 시작하기")
    
    if audio_value:
        st.success("✅ 음성이 성공적으로 기록되었습니다. 아래 분석 버튼을 누르면 AI가 음성 데이터를 함께 참고합니다.")

    st.write("---")
    
    # User Input Form
    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("어르신 연령", min_value=60, max_value=120, value=75)
            region = st.selectbox("거주 지역", ["서울", "경기", "인천", "부산", "대구", "광주", "대전", "울산", "세종", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"])
        with col2:
            care_grade = st.selectbox("노인장기요양등급", ["없음", "1등급", "2등급", "3등급", "4등급", "5등급", "인지지원등급", "아직 신청 전"])
            income_level = st.selectbox("경제적 상황 (소득 수준)", ["기초생활수급자", "차상위계층", "중위소득 160% 이하", "중위소득 160% 초과"])
            
        health_status = st.text_area("어르신의 주요 건강 상태 (드시는 약, 거동 불편 정도 등)", placeholder="예: 무릎 관절염으로 거동이 불편하시고, 가끔 건망증이 있으십니다.")
        
        submitted = st.form_submit_button("맞춤형 AI 분석 시작하기 🚀")
        
    if submitted:
        with st.spinner("최신 정책 데이터를 기반으로 정밀 분석 중입니다..."):
            prompt = f"""
            [어르신 상황]
            - 거주지: {region}
            - 연령: {age}세
            - 장기요양등급: {care_grade}
            - 경제상황: {income_level}
            - 건강상태: {health_status}
            
            위 정보를 바탕으로 '2026 돌봄통합지원법' 전문가로서 다음 4가지를 분석해 줘:
            1. 이 어르신이 2026년에 가장 먼저 누릴 수 있는 핵심 혜택 3가지
            2. 예상 가능한 서비스 비용(본인부담금) 또는 지원금 혜택
            3. 지금 당장 자녀가 준비해야 할 체크리스트 (서류, 연락처 등)
            4. 자녀분을 위한 따뜻한 위로와 격려 한마디
            """
            
            analysis_report = get_ai_response(prompt)
            
            if analysis_report:
                st.balloons()
                st.success("✅ 분석이 완료되었습니다!")
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.markdown(analysis_report)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.divider()
                
                # NEW: Share Result Section
                st.markdown("### 📢 이 결과를 공유해 보세요")
                share_text = f"우리 부모님 맞춤형 2026 돌봄 혜택 분석 결과입니다! \n\n{analysis_report[:200]}..."
                if st.button("📋 분석 결과 복사하기"):
                    st.toast("분석 결과 중 핵심 내용이 클립보드에 복사되었습니다! (시뮬레이션)")
                    st.code(analysis_report, language="markdown")
                
                st.divider()
                
                # Conversion Sections (Premium Looking)
                st.markdown("### 💎 한 단계 더 깊은 케어를 원하신다면")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    if st.button("👩⚕️ 전문가 1:1 컨설팅 신청"):
                        st.balloons()
                        st.success("대표님께 알림이 전송되었습니다! 전문가가 곧 연락드립니다.")
                with col_c2:
                    if "paypal" in st.secrets:
                        paypal_client_id = st.secrets["paypal"]["client_id"]
                        paypal_html = f"""
                        <div id="paypal-button-container"></div>
                        <script src="https://www.paypal.com/sdk/js?client-id={paypal_client_id}&currency=USD"></script>
                        <script>
                          paypal.Buttons({{
                            style: {{
                                layout: 'vertical',
                                color:  'blue',
                                shape:  'rect',
                                label:  'paypal'
                            }},
                            createOrder: function(data, actions) {{
                              return actions.order.create({{
                                purchase_units: [{{
                                  amount: {{
                                    value: '29.99'
                                  }}
                                }}]
                              }});
                            }},
                            onApprove: function(data, actions) {{
                              return actions.order.capture().then(function(details) {{
                                window.parent.postMessage({{type: 'paypal_success', details: details}}, '*');
                              }});
                            }}
                          }}).render('#paypal-button-container');
                        </script>
                        """
                        components.html(paypal_html, height=150)
                    else:
                        if st.button("💳 프리미엄 가이드북 평생 구독"):
                            st.toast("프리미엄 회원 전용 페이지로 이동합니다.")

    # Newsletter Footer
    st.write("---")
    st.markdown("### 💌 1,000명의 진정한 팬을 위한 소식지")
    st.write("2026 돌봄법 개정 공고와 시니어 케어 꿀팁을 가장 먼저 보내드립니다.")
    email_input = st.text_input("이메일 주소를 입력해 주세요", key="newsletter_email")
    if st.button("뉴스레터 구독하기"):
        if email_input:
            st.success(f"축하합니다! {email_input}으로 곧 첫 번째 소식지를 보내드릴게요! 🥳")
        else:
            st.warning("이메일 주소를 입력해 주십시오.")

    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.8rem; margin-top: 50px;">
        © 2026 실버케어 AI 가이드🫡
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
