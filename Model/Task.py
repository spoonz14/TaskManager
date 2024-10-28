import os
import sys
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

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

# Also used this file as the main Task Controller
# Function to create a task
def createTask(title, description, due_date):
    task = Task(title, description, due_date)
    return task

def readTasks():
    tasks = collection.find({})
    list_of_tasks = []

    # Loop through the tasks and create a dictionary for each task
    for task in tasks:
        # Create a task dictionary excluding the '_id' field
        task_dict = {k: v for k, v in task.items() if k != '_id'}
        
        # Add 'type' to the task dictionary if it exists; default to 'Unknown'
        task_dict['type'] = task_dict.get('type', 'Unknown')
        
        list_of_tasks.append(task_dict)

    # Display the tasks as a table
    if list_of_tasks:
        st.table(list_of_tasks)
    else:
        st.write("No tasks found.")

def findByTitle(title):
    tasks = collection.find({'title': f'{title}'})
    for task in tasks:
        print(task)

def sortByType(type):
    # Correctly format the query as a dictionary
    tasks = collection.find({'type': type})
    list_of_tasks = []
    
    # Loop through the tasks and create a list of dictionaries
    for task in tasks:
        task_dict = {k: v for k, v in task.items() if k != '_id'}  # Exclude '_id'
        list_of_tasks.append(task_dict)

    # Display the tasks as a table
    if list_of_tasks:
        st.table(list_of_tasks)
    else:
        st.write("No tasks found for this type.")

    

def deleteAllTasks():
    deletion = collection.delete_many({})
    print(deletion.deleted_count)