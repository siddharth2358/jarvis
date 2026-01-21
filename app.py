import streamlit as st
import os
from rag_agent import Jarvis

# Page configuration
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="wide")

# Custom CSS for "Jarvis" feel
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .stTextInput > div > div > input {
        background-color: #161b22;
        color: #c9d1d9;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #21262d;
        border-left: 5px solid #1f6feb;
    }
    .bot-message {
        background-color: #161b22;
        border-left: 5px solid #238636;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Build Your Own Jarvis")
st.caption("Powered by Pinecone & Llama (via Ollama)")

import os
from dotenv import load_dotenv

load_dotenv()

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    # Try to load from secrets or env
    env_key = os.getenv("PINECONE_API_KEY")
    secret_key = st.secrets["pinecone"]["api_key"] if "pinecone" in st.secrets else ""
    default_api_key = env_key if env_key else secret_key
    
    api_key = st.text_input("Pinecone API Key", value=default_api_key, type="password")
    model_name = st.text_input("Ollama Model Name", value="llama3")
    
    st.divider()
    
    st.header("Knowledge Base")
    uploaded_file = st.file_uploader("Upload a text file to learn from", type="txt")
    if st.button("Learn from File"):
        if uploaded_file and api_key:
            try:
                text_content = uploaded_file.read().decode("utf-8")
                jarvis = Jarvis(pinecone_api_key=api_key, model_name=model_name)
                status = jarvis.learn(text_content)
                st.success(status)
            except Exception as e:
                st.error(f"Error learning: {e}")
        elif not api_key:
            st.warning("Please enter Pinecone API Key first.")
        else:
            st.warning("Please upload a file first.")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "bot-message"
    with st.container():
        st.markdown(f"""
        <div class="chat-message {role_class}">
            <strong>{message["role"].upper()}:</strong>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("What is your command?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Check if configured
    if not api_key:
        st.error("Please configure the Pinecone API Key in the sidebar.")
    else:
        try:
            # Initialize Jarvis
            # Note: In a real production app, we would cache the instance resources
            jarvis = Jarvis(pinecone_api_key=api_key, model_name=model_name)
            
            with st.spinner("Processing..."):
                response = jarvis.ask(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
