import streamlit as st
import requests
import uuid
from datetime import datetime

st.set_page_config(page_title="Medical AI Assistant", page_icon="⚕️", layout="wide")

st.title("⚕️ AI Medical Assistant")
st.write("Please submit your medical details first. This is **not a medical diagnosis**.")

# Backend API URL
API_URL = "http://127.0.0.1:8000/ask"

# Session user ID
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# States
if "patient_info_submitted" not in st.session_state:
    st.session_state.patient_info_submitted = False
if "history" not in st.session_state:
    st.session_state.history = []

# --- Step 1: Intake Form ---
if not st.session_state.patient_info_submitted:
    st.subheader("👤 Patient Intake Form")
    with st.form(key="patient_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        sex = st.selectbox("Sex", ["", "Male", "Female", "Other"])
        region = st.text_input("Region / City")
        conditions = st.text_area("Existing medical conditions (if any)")
        symptoms = st.text_area("Current symptoms or concerns")
        
        submitted = st.form_submit_button("Submit Details")
        if submitted:
            if not name or not age or not sex:
                st.warning("Please fill in Name, Age, and Sex at minimum.")
            else:
                st.session_state.patient_info = {
                    "Name": name,
                    "Age": age,
                    "Sex": sex,
                    "Region": region,
                    "Existing conditions": conditions,
                    "Current symptoms": symptoms
                }
                st.session_state.patient_info_submitted = True
                st.success("Details submitted! You can now chat with your AI doctor.")
                st.rerun()

# --- Step 2: Chat Interface ---
else:
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("💬 Chat with AI Doctor")
        question = st.text_input("Type your question here:")

        if st.button("Ask"):
            if question.strip() == "":
                st.warning("Please enter your question.")
            else:
                payload = {
                    "user_id": st.session_state.user_id,
                    "question": question,
                    "patient_info": st.session_state.patient_info
                }
                try:
                    response = requests.post(API_URL, json=payload)
                    if response.status_code == 200:
                        answer = response.json().get("answer", "No answer received")
                        st.session_state.history.append({
                            "question": question,
                            "answer": answer,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                    else:
                        st.error(f"Backend error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"⚠️ Error connecting to backend: {e}")

        # Chat messages with colored bubbles
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state.history:
                # User message (blue bubble)
                st.markdown(
                    f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; margin-bottom:5px;'>"
                    f"<strong>You ({chat['timestamp']}):</strong><br>{chat['question']}</div>",
                    unsafe_allow_html=True
                )
                # AI message (gray bubble)
                st.markdown(
                    f"<div style='background-color:#F1F0F0; padding:10px; border-radius:10px; margin-bottom:10px;'>"
                    f"<strong>Doctor AI:</strong><br>{chat['answer']}</div>",
                    unsafe_allow_html=True
                )

    with col2:
        st.subheader("👤 Patient Info")
        st.markdown(f"**Name:** {st.session_state.patient_info['Name']}")
        st.markdown(f"**Age:** {st.session_state.patient_info['Age']}")
        st.markdown(f"**Sex:** {st.session_state.patient_info['Sex']}")
        st.markdown(f"**Region:** {st.session_state.patient_info.get('Region','')}")
        st.markdown(f"**Existing Conditions:** {st.session_state.patient_info.get('Existing conditions','')}")
        st.markdown(f"**Current Symptoms:** {st.session_state.patient_info.get('Current symptoms','')}")
