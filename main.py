import os
import sys
import streamlit as st
sys.path.insert(0, os.path.abspath('D:\\Projects\\TaskManager\\Model'))
from Model.Task import Task, readTasks, sortByType, deleteAllTasks
from Model.PersonalTask import createPersonalTask
from Model.WorkTask import createWorkTask
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

    # Initializing the session stage, this is used to sequentially move through the app without rerunning and losing values
    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    def set_stage(stage):
        st.session_state.stage = stage

    st.set_page_config(layout="wide")

    st.title("Task Manager")

    # default/home stage
    if st.session_state.stage == 0:
        st.button("View Tasks", key=1, on_click=set_stage, args=(1,))

    # stage to view all tasks
    if st.session_state.stage == 1:
        readTasks()
        with st.container():
            col1, col2, col3, col4 = st.columns([1,1,1,8])
            # Adjusting spacing with markdown
            #st.markdown("<style>div.stButton {margin: 0 5px;}</style>", unsafe_allow_html=True)
            # Placing the buttons in a row
            with col1:   
                st.button("Return", key=7, on_click=set_stage, args=(0,), type="secondary")
            with col2:
                st.button("Delete All", type="primary", on_click=set_stage, args=(2,))
            with col3:
                st.button("Sort By Type", on_click=set_stage, args=(4,))
            # Attempting to format the buttons
            with col4:
                st.write("")

    # Stage to perform a full deletion of the collection
    if st.session_state.stage == 2:
        deleteAllTasks()
        set_stage(1)  #return to stage 1
        st.rerun()

    # Stage to sort by task type
    if st.session_state.stage == 4:
        type = st.selectbox("Sort by Type:", ('Work', 'Personal'))
        sortByType(type)
        st.button("Return", key=10, on_click=set_stage, args=(1,))
    
    
    # Button and form to create tasks
    st.button("Create Task", key=2, type="secondary", on_click=set_stage, args=(3,))
    
    # Stage to create a new task using a simple form
    if st.session_state.stage == 3:
        st.button("Return", key=30, on_click=set_stage, args=(0,), type="secondary")
        with st.form(key="task_form"):
            st.header("Create Task")

            type = st.selectbox("Type of Task:", ('Work', 'Personal'))
            title = st.text_input("Title:")
            description = st.text_input("Description:")
            due_date = st.text_input("Due Date:")

            submit_form = st.form_submit_button(label="Submit")
            
            # Conditional to save the type of task
            if submit_form:
                if type == 'Work':
                    task = createWorkTask(title, description, due_date)
                    collection.insert_one(task.to_dict())
                    st.success("Work Task created!")
                elif type == 'Personal':
                    task = createPersonalTask(title, description, due_date)
                    collection.insert_one(task.to_dict())
                    st.success("Personal Task created!")

                set_stage(1) # Return to the view all stage
                st.rerun()
