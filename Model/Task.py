import os
import sys
from bson import ObjectId
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

# Also used this file as the main Task Controller

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

class Task:
    def __init__(self, title, description, due_date):
        self._title = title
        self._description = description
        self._due_date = due_date

    # STR method
    def __str__(self):
        return f'Task(title={self._title}, description={self._description}, due_date={self._due_date})'

    # Method to convert the task object to a dictionary
    def to_dict(self):
        return {
            'title': self._title,
            'description': self._description,
            'due_date': self._due_date
        }


# Function to create a task
def createTask(title, description, due_date):
    task = Task(title, description, due_date)
    return task

def set_task_stage(task_stage):
    st.session_state.task_stage = task_stage

def readTasks():
    # Initializing the session stage for tasks, this is used to sequentially move through the app without rerunning and losing values
    if 'task_stage' not in st.session_state:
        st.session_state.task_stage = 0

    
        
    tasks = collection.find({})
    list_of_tasks = []
    set_task_stage(0)
    #st.write(st.session_state.task_stage)

    if st.session_state.task_stage == 0:

        # Loop through the tasks and create a dictionary for each task
        for task in tasks:
            # Create a task dictionary excluding the '_id' field
            # I don't like displaying the ID in the table for aesthetic reasons
            task_dict = {k: v for k, v in task.items()}
            
            # Add 'type' to the task dictionary if it exists; default to 'Unknown'
            task_dict['type'] = task_dict.get('type', 'Unknown')
            
            list_of_tasks.append(task_dict)


        if list_of_tasks:
            for task in list_of_tasks:

                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 5, 2, 2, 1])
                    
                    # Use unique keys for each input field
                    with col1:
                        title = st.text_input("Title", value=task['title'], key=f"title_{task['_id']}", on_change=update_task, args=(task['_id'], 'title'))
                    
                    with col2:
                        description = st.text_input("Description", value=task['description'], key=f"description_{task['_id']}", on_change=update_task, args=(task['_id'], 'description'))
                    
                    with col3:
                        due_date = st.text_input("Due Date", value=task['due_date'], key=f"due_date_{task['_id']}", on_change=update_task, args=(task['_id'], 'due_date'))
                    
                    with col4:
                        task_type = st.selectbox("Type", ['Work', 'Personal'], key=f"selectbox_{task['_id']}", index=['Work', 'Personal'].index(task['type']), on_change=update_task, args=(task['_id'], 'type'))
                    
                    with col5:
                        # Trying to format the button a bit
                        st.empty()
                        st.write('')
                        st.write('')
                        if st.button("Delete", key=f"delete_{task['_id']}", type="primary"):
                            collection.delete_one({'_id': ObjectId(task['_id'])})
                            st.success(f"Task '{task['title']}' deleted!")
                            st.rerun()  

def update_task(task_id, field):
    """Update the task in the database when text input changes."""
    # Fetch the current values from the session state
    current_title = st.session_state.get(f"title_{task_id}", "")
    current_description = st.session_state.get(f"description_{task_id}", "")
    current_due_date = st.session_state.get(f"due_date_{task_id}", "")
    current_type = st.session_state.get(f"selectbox_{task_id}", "Work")

    # Update the database with the new values
    update_fields = {}
    if field == 'title':
        if current_title.strip():
            update_fields['title'] = current_title
        else:
            st.write("Please enter a title.")
            set_task_stage(0)
    elif field == 'description':
        if current_description.strip():
            update_fields['description'] = current_description
        else:
            st.write("Please enter a description.")
            set_task_stage(0)
    elif field == 'due_date':
        if current_due_date.strip():
            update_fields['due_date'] = current_due_date
        else:
            st.write("Please enter a due date")
            set_task_stage(0)
    elif field == 'type' and current_type.strip():
        update_fields['type'] = current_type

    # Perform the update in the database
    if update_fields:
        collection.update_one({'_id': ObjectId(task_id)}, {'$set': update_fields})
        st.success("Task updated!")     

def findByTitle(title):
    tasks = collection.find({'title': f'{title}'})
    for task in tasks:
        print(task)

def sortByType(type):
    # Correctly format the query as a dictionary and retrieve tasks
    tasks = collection.find({'type': type})
    list_of_tasks = []

    # Loop through the tasks and create a list of dictionaries
    for task in tasks:
        # Include '_id' in the task_dict
        task_dict = {k: v for k, v in task.items()}  # Keep all fields
        list_of_tasks.append(task_dict)

    # Display headers at the top of the columns
    if list_of_tasks:
        # Display the tasks
        for task in list_of_tasks:
            col1, col2, col3, col4, col5 = st.columns([2, 5, 2, 2, 1])
            
            # Use unique keys for each input field
            with col1:
                title = st.text_input("Title", value=task['title'], key=f"title_{task['_id']}", on_change=update_task, args=(task['_id'], 'title'))
            
            with col2:
                description = st.text_input("Description", value=task['description'], key=f"description_{task['_id']}", on_change=update_task, args=(task['_id'], 'description'))
            
            with col3:
                due_date = st.text_input("Due Date", value=task['due_date'], key=f"due_date_{task['_id']}", on_change=update_task, args=(task['_id'], 'due_date'))
            
            with col4:
                task_type = st.selectbox("Type", ['Work', 'Personal'], key=f"selectbox_{task['_id']}", index=['Work', 'Personal'].index(task['type']), on_change=update_task, args=(task['_id'], 'type'))
            
            with col5:
                # Adding spacing to format the button better
                st.write("")
                st.write("")
                if st.button("Delete", key=f"delete_{task['_id']}", type="primary"):
                    collection.delete_one({'_id': ObjectId(task['_id'])})
                    st.success(f"Task '{task['title']}' deleted!")
                    st.experimental_rerun() 
    else:
        st.write("No tasks found for this type.")   

def deleteAllTasks():
    deletion = collection.delete_many({})
    print(deletion.deleted_count)