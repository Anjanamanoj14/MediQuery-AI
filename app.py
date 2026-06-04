import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page title
st.title("🏥 MediQuery AI")
st.subheader("Upload your medical report and ask questions in plain English")

# PDF Upload section
st.write("---")
uploaded_file = st.file_uploader("📄 Upload your medical PDF report", type="pdf")

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")

    # Extract text from PDF
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Show extracted text
    st.write("---")
    st.subheader("📋 Extracted Text from your Report:")
    st.text_area("Report Content", text, height=300)
    st.info(f"📊 Total pages: {len(reader.pages)} | Total characters: {len(text)}")

    # Split text into chunks
    st.write("---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(text)
    st.success(f"✅ Document split into {len(chunks)} chunks!")

    # Question input section
    st.write("---")
    st.subheader("❓ Ask a Question About Your Report")
    question = st.text_input("Type your question here (e.g. What is my diagnosis?)")

    if question:
        with st.spinner("🤖 AI is thinking..."):
            context = "\n".join(chunks)
            prompt = f"""You are a helpful medical assistant. 
A patient has uploaded their medical report. 
Based ONLY on the report below, answer the question clearly and simply.
If the answer is not in the report, say "I could not find that information in your report."

Medical Report:
{context}

Patient Question: {question}

Answer in simple, easy to understand language:"""

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)

            st.write("---")
            st.subheader("🤖 AI Answer:")
            st.success(response.text)

else:
    st.warning("⬆️ Please upload a medical PDF report to get started")