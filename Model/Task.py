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

    def __str__(self):
        return f'Task(title={self._title}, description={self._description}, due_date={self._due_date})'

    def to_dict(self):
        return {
            'title': self._title,
            'description': self._description,
            'due_date': self._due_date
        }

def createTask(title, description, due_date):
    task = Task(title, description, due_date)
    return task

def readTasks():
    tasks = collection.find({})
    list_of_tasks = list(tasks)
    st.table(list_of_tasks)

def findByTitle(title):
    tasks = collection.find({'title': f'{title}'})
    for task in tasks:
        print(task)


task = createTask("Dog", "Walk dog", "10-29-2024")
#print(task.to_dict())  
collection.insert_one(task.to_dict())

