import streamlit as st
import PyPDF2
import nltk
from transformers import pipeline
import re

st.set_page_config(page_title="PDF Chatbot", layout="wide", page_icon="📚")

# CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

s
@st.cache_resource
def download_nltk_resources():
    nltk.download('punkt', quiet=True)

download_nltk_resources()


@st.cache_resource
def load_qa_model():
    return pipeline("question-answering")

qa_model = load_qa_model()

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def answer_question(context, question):
    try:
        result = qa_model(question=question, context=context)
        return result['answer']
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None


st.title("📚 PDF Chatbot PROVA 1")
st.markdown("### Upload a PDF and ask questions about its content!")

uploaded_file = st.file_uploader("Choose a PDF file from your device", type="pdf")

if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    if pdf_text:
        st.success("✅ PDF successfully uploaded and processed! I'm ready")
        
        
        with st.expander("📄 Preview of extracted text"):
            st.text_area("", value=pdf_text[:500] + "...", height=200)
        
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        
        user_question = st.text_input("🤔 Please, ask a question about the PDF content:")
        
        if user_question:
            answer = answer_question(pdf_text, user_question)
            if answer:
                st.session_state.chat_history.append((user_question, answer))
        
        
        if st.session_state.chat_history:
            st.subheader("💬 Chat History")
            for q, a in st.session_state.chat_history:
                st.markdown(f'<div class="chat-message user"><div class="avatar">👤</div><div class="message">Q: {q}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-message bot"><div class="avatar">🤖</div><div class="message">A: {a}</div></div>', unsafe_allow_html=True)

else:
    st.info("👆 Upload a PDF to start chatting with me!")

st.markdown("---")
st.markdown("Made by Fabio")
