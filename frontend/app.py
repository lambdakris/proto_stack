import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Backend API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")

st.set_page_config(page_title="Todo App", page_icon="✅", layout="wide")

def get_todos():
    """Fetch all todos from the backend API"""
    try:
        response = requests.get(f"{API_BASE_URL}/todos")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch todos: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return []

def create_todo(title, description):
    """Create a new todo via the backend API"""
    try:
        payload = {"title": title, "description": description}
        response = requests.post(f"{API_BASE_URL}/todos", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to create todo: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return None

def update_todo(todo_id, title=None, description=None, completed=None):
    """Update a todo via the backend API"""
    try:
        payload = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if completed is not None:
            payload["completed"] = completed
        
        response = requests.put(f"{API_BASE_URL}/todos/{todo_id}", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to update todo: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return None

def delete_todo(todo_id):
    """Delete a todo via the backend API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/todos/{todo_id}")
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to delete todo: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return False

def main():
    st.title("🚀 Todo App")
    st.markdown("A minimal todo application built with Streamlit and FastAPI")
    
    # Create new todo section
    st.header("➕ Add New Todo")
    with st.form("new_todo_form"):
        title = st.text_input("Title*", placeholder="Enter todo title...")
        description = st.text_area("Description", placeholder="Enter todo description...")
        submitted = st.form_submit_button("Add Todo")
        
        if submitted and title:
            todo = create_todo(title, description)
            if todo:
                st.success("Todo created successfully!")
                st.rerun()
        elif submitted and not title:
            st.error("Title is required!")
    
    # Display todos section
    st.header("📋 Your Todos")
    todos = get_todos()
    
    if not todos:
        st.info("No todos yet. Add one above!")
    else:
        for todo in todos:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    if todo["completed"]:
                        st.markdown(f"~~**{todo['title']}**~~")
                        if todo["description"]:
                            st.markdown(f"~~{todo['description']}~~")
                    else:
                        st.markdown(f"**{todo['title']}**")
                        if todo["description"]:
                            st.markdown(todo["description"])
                
                with col2:
                    # Toggle completion status
                    new_status = not todo["completed"]
                    status_text = "Mark Incomplete" if todo["completed"] else "Mark Complete"
                    if st.button(status_text, key=f"toggle_{todo['id']}"):
                        update_todo(todo["id"], completed=new_status)
                        st.rerun()
                
                with col3:
                    # Delete todo
                    if st.button("🗑️ Delete", key=f"delete_{todo['id']}"):
                        if delete_todo(todo["id"]):
                            st.success("Todo deleted!")
                            st.rerun()
                
                st.divider()

if __name__ == "__main__":
    main()