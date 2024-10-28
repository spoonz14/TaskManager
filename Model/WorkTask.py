from Model.Task import Task

class WorkTask(Task):
    def __init__(self, title, description, due_date):
        super().__init__(title, description, due_date)
        self.type = "Work"

    def to_dict(self):
        data = super().to_dict()
        data['type'] = self.type 
        return data

def createWorkTask(title, description, due_date):
    return WorkTask(title, description, due_date)
