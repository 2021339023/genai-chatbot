import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables from .env file
load_dotenv()

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Shipo's AI Assistant",
    page_icon="🤖",
    layout="centered", # 'centered' layoutchat এর জন্য বেশি সুন্দর দেখায়
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Attractive UI ---
st.markdown("""
    <style>
    /* Main Background & Font */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Header Styling */
    h1 {
        color: #00adb5;
        font-family: 'Inter', sans-serif;
    }
    
    /* Chat Input Field Customization */
    .stChatInput input {
        background-color: #1f2833 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #45567d !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Custom Buttons */
    .stButton button {
        background-color: #ff4c4c;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #ff1e1e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.title("Control Panel")
    st.markdown("---")
    st.markdown("✨ **Developer:** Shipo")
    st.markdown("🚀 **Model:** `openai/gpt-oss-120b`")
    st.markdown("⚡ **Status:** Active & Ready")
    st.markdown("---")
    
    # Clear Chat History Button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
        
    st.markdown("---")
    st.caption("A smart AI-powered assistant built with Streamlit & LangChain.")

# --- Main App Header ---
st.markdown("<h1 style='text-align: center;'>💬 Shipo's AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Ask me anything, and let's start a conversation! 🚀</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- LLM Initialization ---
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY not found in environment variables or .env file.")
else:
    llm = ChatGroq(
        model="openai/gpt-oss-120b",  # Working model
        temperature=0.3,
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
                SystemMessage(content="You are a helpful, smart, and friendly assistant."),
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
