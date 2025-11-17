'''
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq


# load the env variables
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered",
)
st.title("💬 Welcome from Shipo, ask me anythings")

# initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# llm initiate
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0,
)

# input box
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input = [{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
    )
    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
'''
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
import os # Added for better practice with environment variables

# load the env variables
load_dotenv()

# --- Streamlit Page Configuration ---
# Use a built-in theme (e.g., 'dark') and better layout options
st.set_page_config(
    page_title="🤖 AI Chat Assistant",
    page_icon="✨",
    layout="wide", # Use 'wide' layout for more space
    initial_sidebar_state="expanded" # Keep the sidebar open by default
)

# --- Sidebar for Aesthetics and Information ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1543269865-cbe42617f093?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", width=250)
    st.title("AI Assistant Settings")
    
    st.markdown("""
        Hello! I'm your AI Chatbot, powered by **llama-3.3-70b-versatile** via the **Groq API**.
        
        *Feel free to ask me anything!*
    """)
    
    # You could add user-configurable options here later, like temperature.
    st.subheader("Model Details")
    st.info(f"Model: `llama-3.3-70b-versatile`")
    
    # Add a clear way to reset the chat
    if st.button("🔄 Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# --- Main Page Title and Header ---
st.header("💬 Shipo's Groq-Powered Chatbot", divider='rainbow')
st.markdown("### Ask me anything, and let's start a conversation! 🚀")

# initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- LLM Initiate ---
# Get API Key from environment variable (Best practice)
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY not found. Please set it in your environment variables.")
else:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
        groq_api_key=groq_api_key # Pass key explicitly
    )
    
# --- Display Chat History ---
# Display messages using Streamlit's chat elements
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input and LLM Interaction ---
user_prompt = st.chat_input("Type your message here...")

if user_prompt and 'llm' in locals(): # Check if LLM was successfully initialized
    # 1. Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
        
    # 2. Append to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # 3. Generate response
    with st.spinner("Thinking..."): # Added a spinner for better UX
        # The prompt structure with role messages is maintained as requested
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.chat_history
        ]
        
        try:
            response = llm.invoke(messages)
            assistant_response = response.content
        except Exception as e:
            assistant_response = f"An error occurred: {e}"

    # 4. Display assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        
    # 5. Append assistant response to history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
