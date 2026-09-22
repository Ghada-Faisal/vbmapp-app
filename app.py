import streamlit as st
from google import genai

st.set_page_config(page_title="G-Ai VBMAPP System", page_icon="📊", layout="centered")

st.markdown("""
<div dir="rtl" style="text-align: right;">
    <h2>نظام G-Ai VBMAPP لتحليل التقييمات السلوكية 📊</h2>
    <p>أدخل بيانات التقييم أو اطرح استفسارك الإكلينيكي مباشرة.</p>
</div>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTIONS = """
أنت نظام خبير ذكي في تحليل تقييمات VB-MAPP. قم بتحليل البيانات الواردة وتقديم جداول البيانات الوصفية والتحليلية والتقارير الإكلينيكية بدقة متناهية.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div dir='rtl' style='text-align: right;'>{msg['content']}</div>", unsafe_allow_html=True)

if user_input := st.chat_input("أدخل البيانات أو استفسارك هنا..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"<div dir='rtl' style='text-align: right;'>{user_input}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("جاري التحليل الإكلينيكي..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config={
                    "system_instruction": SYSTEM_INSTRUCTIONS,
                    "temperature": 0.2,
                }
            )
            reply = response.text
            st.markdown(f"<div dir='rtl' style='text-align: right;'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})
