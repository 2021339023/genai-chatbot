import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables from .env file
load_dotenv()

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3592/3592078.png", width=150)
    st.title("AI Assistant Settings")
    st.markdown("Powered by **openai/gpt-oss-20b** via **Groq API**.")
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# --- Main App Header ---
st.header("💬 Shipo's Groq-Powered Chatbot", divider='rainbow')

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- LLM Initialization ---
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY not found in environment variables or .env file.")
else:
    llm = ChatGroq(
        model="openai/gpt-oss-20b",  # Active Groq model ID
        temperature=0.0,
        groq_api_key=groq_api_key
    )

    # --- Display Existing Chat History ---
    for message in st.session_state.chat_history:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

    # --- User Input Handler ---
    user_prompt = st.chat_input("Type your message here...")

    if user_prompt:
        # Display user message instantly on UI
        with st.chat_message("user"):
            st.markdown(user_prompt)
            
        # Append to history as a HumanMessage object
        st.session_state.chat_history.append(HumanMessage(content=user_prompt))

        # Generate LLM response with a loading spinner
        with st.spinner("Thinking..."):
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                *st.session_state.chat_history
            ]
            
            try:
                response = llm.invoke(messages)
                assistant_response = response.content
            except Exception as e:
                assistant_response = f"An error occurred: {e}"

        # Display and save assistant response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
            
        st.session_state.chat_history.append(AIMessage(content=assistant_response))
