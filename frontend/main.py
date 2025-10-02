import streamlit as st
from dotenv import load_dotenv
from pages import home, about, todos

load_dotenv()

st.set_page_config(page_title="Todo App", page_icon="✅", layout="wide")

def main():
    # Define pages for navigation
    home_page = st.Page(home.show, title="Home", icon="🏠")
    about_page = st.Page(about.show, title="About", icon="ℹ️")
    todos_page = st.Page(todos.show, title="Todos", icon="📋")
    
    # Create navigation with top style
    pg = st.navigation([home_page, about_page, todos_page], position="top")
    
    # Run the selected page
    pg.run()

if __name__ == "__main__":
    main()