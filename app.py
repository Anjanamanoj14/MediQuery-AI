import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page config
st.set_page_config(
    page_title="MediQuery AI",
    page_icon="🏥",
    layout="wide"
)
# HuggingFace fix
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"

# Custom CSS
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }

    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
        animation: gradient 3s ease infinite;
    }

    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Card styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }

    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(0, 212, 255, 0.1) !important;
        margin: 10px 0 !important;
    }

    /* Success box */
    .stSuccess {
        background: rgba(0, 212, 100, 0.1) !important;
        border: 1px solid rgba(0, 212, 100, 0.3) !important;
        border-radius: 10px !important;
    }

    /* Info box */
    .stInfo {
        background: rgba(0, 212, 255, 0.1) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
    }

    /* Sidebar */
    .css-1d391kg {
        background: rgba(26, 26, 46, 0.95) !important;
    }

    /* Upload button */
    .stFileUploader {
        border: 2px dashed rgba(0, 212, 255, 0.4) !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }

    /* Chat input */
    .stChatInput {
        border-radius: 25px !important;
    }

    /* Metrics */
    .metric-card {
        background: rgba(123, 47, 247, 0.15);
        border: 1px solid rgba(123, 47, 247, 0.3);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }

    /* Divider */
    hr {
        border-color: rgba(0, 212, 255, 0.2) !important;
    }

    /* Spinner */
    .stSpinner {
        color: #00d4ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🏥 MediQuery AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Personal AI-Powered Medical Report Assistant</p>', unsafe_allow_html=True)

# Stats bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color:#00d4ff">🤖</h3>
        <p style="color:white;margin:0">Gemini AI</p>
        <small style="color:#a0aec0">Powered</small>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color:#00d4ff">📄</h3>
        <p style="color:white;margin:0">PDF Reader</p>
        <small style="color:#a0aec0">Any Report</small>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color:#00d4ff">💬</h3>
        <p style="color:white;margin:0">Chat Based</p>
        <small style="color:#a0aec0">Ask Anything</small>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color:#00d4ff">🔒</h3>
        <p style="color:white;margin:0">Secure</p>
        <small style="color:#a0aec0">Private</small>
    </div>""", unsafe_allow_html=True)

st.write("---")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False
if "chunks" not in st.session_state:
    st.session_state.chunks = []

# Sidebar
with st.sidebar:
    st.markdown("## 📂 Upload Your Report")
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Drop your medical PDF here",
        type="pdf",
        help="Supported: Blood reports, prescriptions, discharge summaries"
    )

    if uploaded_file is not None:
        with st.spinner("🔍 Analyzing your report..."):
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            st.session_state.chunks = text_splitter.split_text(text)
            st.session_state.pdf_processed = True

        st.success("✅ Report Ready!")

        # Report stats
        st.markdown("### 📊 Report Stats")
        st.metric("Pages", len(reader.pages))
        st.metric("Chunks", len(st.session_state.chunks))
        st.metric("Characters", len(text))

    st.markdown("---")
    st.markdown("### 🌍 Select Language")
    language = st.selectbox(
    "Answer language",
    ["English", "Malayalam", "Hindi",
     "Tamil", "Telugu", "Kannada",
     "Bengali", "Arabic", "French"]
    )
    st.markdown("### 💡 Try Asking:")
    questions = [
        "What is the diagnosis?",
        "What medicines are prescribed?",
        "What is the blood pressure?",
        "What advice was given?",
        "Is anything abnormal?"
    ]
    for q in questions:
        st.markdown(f"• *{q}*")

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center;color:#a0aec0;font-size:0.8rem'>
        Built with ❤️ by Anjan<br>
        Powered by Gemini AI
    </div>
    """, unsafe_allow_html=True)

# Main chat area
if not st.session_state.pdf_processed:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color:#00d4ff">👈 Get Started</h3>
        <p style="color:#a0aec0">Upload your medical PDF report from the sidebar to begin</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#00d4ff">📤 Step 1</h4>
            <p style="color:white">Upload your medical PDF from the sidebar</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#00d4ff">❓ Step 2</h4>
            <p style="color:white">Type your question in plain English</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#00d4ff">🤖 Step 3</h4>
            <p style="color:white">Get clear AI-powered answers instantly</p>
        </div>""", unsafe_allow_html=True)

else:
    # Auto Summary Section
   st.write("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("📋 Generate Report Summary", use_container_width=True):
        with st.spinner("📋 Generating summary..."):
            try:
                context = "\n".join(st.session_state.chunks)
                summary_prompt = f"""You are a helpful medical assistant.
Summarize this medical report in {language} language in simple terms.
Structure your summary as:

👤 Patient Details:
🏥 Main Diagnosis:
🌡️ Vital Signs:
💊 Prescribed Medicines:
📋 Doctor's Advice:
⚠️ Important Notes:

Medical Report:
{context}

Provide a clear, simple summary in {language} language:"""

                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(summary_prompt)
                st.session_state.summary = response.text

            except Exception as e:
                if "429" in str(e):
                    st.warning("⏳ Please wait 30 seconds and try again!")
                else:
                    st.error(f"❌ Error: {str(e)}")

with col2:
    if st.button("⚠️ Check Abnormal Values", use_container_width=True):
        with st.spinner("🔍 Checking for abnormal values..."):
            try:
                context = "\n".join(st.session_state.chunks)
                abnormal_prompt = f"""You are a medical expert assistant.
Analyze this medical report and identify in {language} language:

1. ⚠️ Abnormal Values — list each abnormal finding
2. 📊 Normal Range — what the normal range should be
3. 🔍 What it means — simple explanation
4. 🏥 Recommendation — what the patient should do

If everything is normal, say "All values appear to be within normal range."

Medical Report:
{context}

Answer in {language} language:"""

                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(abnormal_prompt)
                st.session_state.abnormal = response.text

            except Exception as e:
                if "429" in str(e):
                    st.warning("⏳ Please wait 30 seconds and try again!")
                else:
                    st.error(f"❌ Error: {str(e)}")

# Show summary if generated
if "summary" in st.session_state and st.session_state.summary:
    st.write("---")
    st.subheader("📋 Report Summary")
    st.info(st.session_state.summary)

# Show abnormal values if generated
if "abnormal" in st.session_state and st.session_state.abnormal:
    st.write("---")
    st.subheader("⚠️ Abnormal Values Analysis")
    st.warning(st.session_state.abnormal)
# Medicine Explainer Button
st.write("")
if st.button("💊 Explain My Medicines", use_container_width=True):
    with st.spinner("💊 Analyzing medicines..."):
        try:
            context = "\n".join(st.session_state.chunks)
            medicine_prompt = f"""You are a helpful medical assistant.
From this medical report, find all medicines and explain in {language} language:

For each medicine provide:
💊 Medicine Name:
🎯 What it is for:
📏 Dosage & Duration:
⚠️ Common Side Effects:
🔔 Important Precautions:

Medical Report:
{context}

If no medicines found, say "No medicines found in this report."
Answer in {language} language:"""

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(medicine_prompt)
            st.session_state.medicines = response.text

        except Exception as e:
            if "429" in str(e):
                st.warning("⏳ Please wait 30 seconds and try again!")
            else:
                st.error(f"❌ Error: {str(e)}")

# Show medicines if generated
if "medicines" in st.session_state and st.session_state.medicines:
    st.write("---")
    st.subheader("💊 Medicine Information")
    st.info(st.session_state.medicines)

st.write("---")
st.markdown("### 💬 Chat with Your Report")

for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
question = st.chat_input(f"Ask your question in {language}...")

if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("🤖 Analyzing your report..."):
                try:
                    context = "\n".join(st.session_state.chunks)
                    prompt = f"""You are a helpful medical assistant.
A patient has uploaded their medical report.
Based ONLY on the report below, answer the question clearly and simply.
If the answer is not in the report, say "I could not find that information in your report."

Medical Report:
{context}

Patient Question: {question}

IMPORTANT INSTRUCTIONS:
- The question may be asked in any language
- You must understand the question regardless of language
- Answer strictly in {language} language only
- Use simple, easy to understand language
- Do not translate the medical report, only the answer

Answer:"""

                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(prompt)
                    answer = response.text
                    st.write(answer)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:
                    if "429" in str(e):
                        st.warning("⏳ Too many requests! Please wait 30 seconds and try again.")
                    else:
                        st.error(f"❌ Error: {str(e)}")