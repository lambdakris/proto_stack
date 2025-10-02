import streamlit as st

def show():
    """Display the About page"""
    st.title("ℹ️ About Proto Stack")
    
    st.markdown("""
    ## Project Overview
    
    Proto Stack is a modern full-stack application template that demonstrates best practices 
    for building web applications with Python.
    
    ### Architecture
    
    The application follows a clean architecture with clear separation of concerns:
    
    1. **Frontend (Streamlit)**: Provides an interactive web interface
    2. **Backend (FastAPI)**: Handles business logic and API endpoints
    3. **Database (PostgreSQL)**: Stores persistent data
    4. **Migrations (Liquibase)**: Manages database schema versions
    
    ### Technology Stack
    
    - **Frontend**: [Streamlit](https://streamlit.io/) - Python web app framework
    - **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python API framework
    - **Database**: [PostgreSQL](https://www.postgresql.org/) - Robust relational database
    - **Schema Migration**: [Liquibase](https://www.liquibase.org/) - Database version control
    - **Package Management**: [UV](https://docs.astral.sh/uv/) - Fast Python package manager
    - **Orchestration**: [Docker Compose](https://docs.docker.com/compose/) - Multi-container orchestration
    
    ### Development Features
    
    - 🔄 Hot reload for rapid development
    - 🐛 Integrated debugging with debugpy
    - 📦 Fast dependency management with UV
    - 🐳 Containerized development environment
    - 📚 Automatic API documentation (FastAPI)
    
    ### Contact
    
    For more information, visit the [GitHub repository](https://github.com/lambdakris/proto_stack).
    """)
