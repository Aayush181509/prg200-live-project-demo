import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API Configuration
API_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🎓 Student Management System</h1>', unsafe_allow_html=True)

# Helper functions
def get_all_students():
    """Fetch all students from API"""
    try:
        response = requests.get(f"{API_URL}/students")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching students: {e}")
        return []

def create_student(name, email, age, course):
    """Create a new student"""
    try:
        data = {
            "name": name,
            "email": email,
            "age": age,
            "course": course
        }
        response = requests.post(f"{API_URL}/students", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating student: {e}")
        return None

def update_student(student_id, name, email, age, course):
    """Update an existing student"""
    try:
        data = {
            "name": name,
            "email": email,
            "age": age,
            "course": course
        }
        response = requests.put(f"{API_URL}/students/{student_id}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating student: {e}")
        return None

def delete_student(student_id):
    """Delete a student"""
    try:
        response = requests.delete(f"{API_URL}/students/{student_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting student: {e}")
        return None

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Select Option", ["View All Students", "Add Student", "Update Student", "Delete Student"])

# View All Students
if menu == "View All Students":
    st.header("📋 All Students")
    
    students = get_all_students()
    
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)
        st.success(f"Total Students: {len(students)}")
    else:
        st.info("No students found. Add some students to get started!")

# Add Student
elif menu == "Add Student":
    st.header("➕ Add New Student")
    
    with st.form("add_student_form"):
        name = st.text_input("Name *", placeholder="Enter student name")
        email = st.text_input("Email *", placeholder="Enter email address")
        age = st.number_input("Age *", min_value=15, max_value=100, value=20)
        course = st.text_input("Course *", placeholder="Enter course name")
        
        submitted = st.form_submit_button("Add Student")
        
        if submitted:
            if name and email and course:
                result = create_student(name, email, age, course)
                if result:
                    st.success(f"✅ Student '{name}' added successfully!")
                    st.json(result)
            else:
                st.error("Please fill in all required fields!")

# Update Student
elif menu == "Update Student":
    st.header("✏️ Update Student")
    
    students = get_all_students()
    
    if students:
        student_options = {f"{s['id']} - {s['name']}": s for s in students}
        selected = st.selectbox("Select Student to Update", list(student_options.keys()))
        
        if selected:
            student = student_options[selected]
            
            with st.form("update_student_form"):
                name = st.text_input("Name *", value=student['name'])
                email = st.text_input("Email *", value=student['email'])
                age = st.number_input("Age *", min_value=15, max_value=100, value=student['age'])
                course = st.text_input("Course *", value=student['course'])
                
                submitted = st.form_submit_button("Update Student")
                
                if submitted:
                    if name and email and course:
                        result = update_student(student['id'], name, email, age, course)
                        if result:
                            st.success(f"✅ Student updated successfully!")
                            st.json(result)
                    else:
                        st.error("Please fill in all required fields!")
    else:
        st.info("No students available to update.")

# Delete Student
elif menu == "Delete Student":
    st.header("🗑️ Delete Student")
    
    students = get_all_students()
    
    if students:
        student_options = {f"{s['id']} - {s['name']}": s for s in students}
        selected = st.selectbox("Select Student to Delete", list(student_options.keys()))
        
        if selected:
            student = student_options[selected]
            
            st.warning(f"Are you sure you want to delete **{student['name']}**?")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Yes, Delete", type="primary"):
                    result = delete_student(student['id'])
                    if result:
                        st.success(f"✅ Student '{student['name']}' deleted successfully!")
                        st.rerun()
            
            with col2:
                if st.button("Cancel"):
                    st.info("Delete operation cancelled.")
    else:
        st.info("No students available to delete.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Make sure the FastAPI backend is running on port 8000")
