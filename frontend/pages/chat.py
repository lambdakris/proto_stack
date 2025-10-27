import streamlit as st
import requests
import os

# Backend API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")

# Initialize chat history in session state
def initialize_chat_history():
    """Initialize chat history if it doesn't exist"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_messages():
    """Display all chat messages from history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_assistant_response_stream(user_message):
    """
    Call the backend API to get streaming AI assistant response.
    Returns a generator that yields response chunks.
    """
    try:
        payload = {"message": user_message}
        response = requests.post(
            f"{API_BASE_URL}/chat", 
            json=payload,
            stream=True,
            headers={"Accept": "text/event-stream"}
        )
        
        if response.status_code == 200:
            # Stream the response
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        import json
                        data = json.loads(line[6:])  # Remove 'data: ' prefix
                        yield data['content']
        else:
            st.error(f"Failed to get response: {response.status_code}")
            yield "I apologize, but I'm having trouble responding right now. Please try again."
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        yield "I apologize, but I'm having trouble connecting to the backend. Please try again."

def handle_user_input():
    """Handle new user input from chat input widget"""
    if prompt := st.chat_input("What would you like to talk about?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response with streaming
        with st.chat_message("assistant"):
            # Use st.write_stream to display streaming response
            response = st.write_stream(get_assistant_response_stream(prompt))
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def show():
    """Display the Chat page"""
    st.title("💬 Chatbot")
    st.markdown("Have a conversation with our AI assistant!")
    
    # Add a button to clear chat history
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Initialize chat history
    initialize_chat_history()
    
    # Display existing messages
    display_chat_messages()
    
    # Handle new user input
    handle_user_input()

show()
