import os
import sys
import os
sys.path.insert(0, os.path.abspath('D:\\Projects\\TaskManager\\Model'))
from Model.Task import Task
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

def createTask(task_id, title, description, due_date):
    task = {
        '_id': task_id,
        'title': title,
        'description': description,
        'due_date': due_date
    }
    return task

#task = Task(title='Homework',description='Homework for school',due_date='10-30-2024')
#print(task)

#collection.delete_one({'title': 'Homework'})
collection.insert_one(createTask(1, 'Homework', 'Homework for school', '10-30-2024'))