import streamlit as st
from pypdf import PdfReader

# Page title
st.title("🏥 MediQuery AI")
st.subheader("Upload your medical report and ask questions in plain English")

# PDF Upload section
st.write("---")
uploaded_file = st.file_uploader("📄 Upload your medical PDF report", type="pdf")

# If a file is uploaded
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
    
    # Show basic stats
    st.write("---")
    st.info(f"📊 Total pages: {len(reader.pages)} | Total characters: {len(text)}")

else:
    st.warning("⬆️ Please upload a medical PDF report to get started")

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Split text into chunks
if uploaded_file is not None:
    st.write("---")
    st.subheader("✂️ Splitting document into chunks...")
    
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # each chunk = 500 characters
        chunk_overlap=50     # 50 characters overlap between chunks
    )
    
    # Split the text
    chunks = text_splitter.split_text(text)
    
    # Show chunk info
    st.success(f"✅ Document split into {len(chunks)} chunks!")
    
    # Show first chunk as example
    st.write("**Example — First chunk:**")
    st.info(chunks[0] if chunks else "No chunks found")  

# Question input section
if uploaded_file is not None:
    st.write("---")
    st.subheader("❓ Ask a Question About Your Report")
    
    question = st.text_input("Type your question here (e.g. What is my blood pressure?)")
    
    if question:
        st.write("---")
        st.subheader("🔍 Searching your report...")
        
        # Simple keyword search for now
        question_words = question.lower().split()
        relevant_lines = []
        
        for line in text.split("."):
            for word in question_words:
                if word in line.lower() and len(line.strip()) > 10:
                    relevant_lines.append(line.strip())
                    break
        
        if relevant_lines:
            st.success("✅ Found relevant information:")
            for line in relevant_lines[:5]:
                st.write(f"• {line}")
        else:
            st.warning("❌ No relevant information found for your question")
