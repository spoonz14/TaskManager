import Task

class WorkTask(Task):
    def __init__(self, title, description, due_date):
        super().__init__(title, description, due_date)
        