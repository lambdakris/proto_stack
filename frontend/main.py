import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Todo App", page_icon="✅", layout="wide")

def main():
    home_page = st.Page("pages/home.py", title="Home", icon="🏠")
    about_page = st.Page("pages/about.py", title="About", icon="ℹ️")
    todos_page = st.Page("pages/todos.py", title="Todos", icon="📋")
    chat_page = st.Page("pages/chat.py", title="Chat", icon="💬")

    pg = st.navigation([home_page, about_page, todos_page, chat_page], position="top")
    pg.run()

if __name__ == "__main__":
    main()