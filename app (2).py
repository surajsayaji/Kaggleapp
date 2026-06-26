# TODO: Build your Streamlit chatbot application

import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

# --- Configuration ---
st.title("My Streamlit Chatbot")

# Set your Groq API key here (or use Streamlit secrets: st.secrets["GROQ_API_KEY"])
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY_HERE"

# Initialize the Groq model

# Initialize the Groq model
# You can change the model name based on what Groq currently supports (e.g., llama3-8b-8192)
llm = ChatGroq(model_name="llama3-8b-8192")

# --- Chat History Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Logic ---
# Get user input
if prompt := st.chat_input("How can I help you today?"):
    
    # 1. Display and save the user's message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Format history for LangChain
    chat_history = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_history.append(HumanMessage(content=msg["content"]))
        else:
            chat_history.append(AIMessage(content=msg["content"]))

    # 3. Call the LLM
    with st.chat_message("assistant"):
        # We can use st.spinner to show the user that the AI is thinking
        with st.spinner("Thinking..."):
            response = llm.invoke(chat_history)
            st.markdown(response.content)
            
    # 4. Save the AI's response to history
    st.session_state.messages.append({"role": "assistant", "content": response.content})
