import streamlit as st

def show():
    """Display the Home page"""
    st.title("🏠 Welcome to Proto Stack Todo App")
    
    st.markdown("""
    ## About This Application
    
    A minimal todo application built with:
    - **Frontend**: Streamlit (Python web framework)
    - **Backend**: FastAPI (Modern Python API framework)
    - **Database**: PostgreSQL
    - **Schema Migration**: Liquibase
    
    ## Features
    
    - ✅ Create, read, update, delete (CRUD) operations for todos
    - ✅ Mark todos as complete/incomplete
    - ✅ Real-time updates between frontend and backend
    - ✅ Docker containerization
    - ✅ VS Code debugging support
    
    ## Get Started
    
    Navigate to the **Todos** page to start managing your tasks!
    """)
