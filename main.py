import os
import sys
import streamlit as st
sys.path.insert(0, os.path.abspath('D:\\Projects\\TaskManager\\Model'))
from Model.Task import Task, readTasks, createTask
from pymongo import MongoClient
from dotenv import load_dotenv

if __name__ == "__main__":

    # Load the environment variables
    load_dotenv()

    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    db_name = os.getenv("MONGO_DB_NAME")
    cl_name = os.getenv("MONGO_CL_NAME")

    # Connection to database
    connection_string = f'mongodb+srv://{username}:{password}@cluster0.i4tgncs.mongodb.net/'
    client = MongoClient(connection_string)

    # Access the DB
    db = client[db_name]
    collection = db[cl_name]

    st.title("Task Manager")
    
    # button to view all tasks
    if st.button("View Tasks", key=1):
        if st.button("Return", key=7, type="primary"):
            st.rerun()
        readTasks()     
    
    # Initializing some session states
    formbtn = st.button("Create Task")

    if "formbtn" not in st.session_state:
        st.session_state.formbtn_state = False

    if formbtn or st.session_state.formbtn_state:
        st.session_state.formbtn_state = True

        st.subheader("Task Creation")
    # button and form to create tasks
    #if st.button("Create Task", key=2, type="secondary"):
        with st.form(key="task_form"):
            st.header("Create Task")

            title = st.text_input("Title:")
            description = st.text_input("Description:")
            due_date = st.text_input("Due Date:")

            submit_form = st.form_submit_button(label="Submit")
            
            if submit_form:
                task = createTask(title, description, due_date)
                collection.insert_one(task.to_dict())
                st.success("Task created!")
                # Clear forms
                st.session_state["title_input"] = ""
                st.session_state["desc_input"] = ""
                st.session_state["due_date_input"] = ""
                st.experimental_rerun()