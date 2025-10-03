import streamlit as st
import random
import time

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

def get_assistant_response(user_message):
    """
    Stub function to simulate LLM response.
    In a real implementation, this would call an actual LLM API.
    """
    # Simulate processing delay
    time.sleep(0.5)
    
    # Stubbed responses based on simple keyword matching
    user_lower = user_message.lower()
    
    if "hello" in user_lower or "hi" in user_lower:
        responses = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! Nice to meet you. What's on your mind?"
        ]
    elif "how are you" in user_lower:
        responses = [
            "I'm doing great, thank you for asking! How about you?",
            "I'm functioning well! How can I assist you today?"
        ]
    elif "thank" in user_lower:
        responses = [
            "You're welcome! Is there anything else I can help with?",
            "Happy to help! Let me know if you need anything else."
        ]
    elif "bye" in user_lower or "goodbye" in user_lower:
        responses = [
            "Goodbye! Have a great day!",
            "See you later! Feel free to come back anytime."
        ]
    elif "help" in user_lower:
        responses = [
            "I'm here to help! You can ask me questions about the Proto Stack application, or just chat with me.",
            "I can help with various topics. What would you like to know?"
        ]
    else:
        responses = [
            f"That's an interesting point about '{user_message}'. Tell me more!",
            f"I understand you mentioned '{user_message}'. Can you elaborate?",
            "That's a great question! In a full implementation, I'd provide a detailed response.",
            "Interesting! I'd love to help with that. This is a demo chatbot, so my responses are limited.",
        ]
    
    return random.choice(responses)

def handle_user_input():
    """Handle new user input from chat input widget"""
    if prompt := st.chat_input("What would you like to talk about?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_assistant_response(prompt)
            st.markdown(response)
        
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
