import os
import sys
import streamlit as st
from Model.Task import readTasks, createTask
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection setup
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
db_name = os.getenv("MONGO_DB_NAME")
cl_name = os.getenv("MONGO_CL_NAME")

# Connect to MongoDB
connection_string = f'mongodb+srv://{username}:{password}@cluster0.i4tgncs.mongodb.net/'
client = MongoClient(connection_string)

# Access the database and collection
db = client[db_name]
collection = db[cl_name]

st.title("Task Manager")

# Button to view all tasks
if st.button("View Tasks", key=1):
    if st.button("Return", key=7, type="primary"):
        st.experimental_rerun()
    readTasks()

# Initialize session state for form inputs if not already set
if "title_input" not in st.session_state:
    st.session_state["title_input"] = ""
if "desc_input" not in st.session_state:
    st.session_state["desc_input"] = ""
if "due_date_input" not in st.session_state:
    st.session_state["due_date_input"] = ""

# Button and form to create tasks
if st.button("Create Task", key=2, type="secondary"):
    with st.form(key="task_form"):
        st.header("Create Task")

        # Input fields for the form
        title = st.text_input("Title:", value=st.session_state["title_input"], key="title_input")
        description = st.text_input("Description:", value=st.session_state["desc_input"], key="desc_input")
        due_date = st.text_input("Due Date:", value=st.session_state["due_date_input"], key="due_date_input")

        # Submit button inside the form
        if st.form_submit_button(label="Submit"):
            # Save input to session state
            st.session_state["title_input"] = title
            st.session_state["desc_input"] = description
            st.session_state["due_date_input"] = due_date

            # Create the task and insert into MongoDB
            task = createTask(title, description, due_date)
            collection.insert_one(task.to_dict())
            st.success("Task created!")

            # Clear session state after submission
            st.session_state["title_input"] = ""
            st.session_state["desc_input"] = ""
            st.session_state["due_date_input"] = ""

