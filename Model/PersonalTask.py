import Task

class PersonalTask(Task):
    def __init__(self, title, description, due_date):
        super().__init__(title, description, due_date)
        
