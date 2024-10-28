from Model.Task import Task

class PersonalTask(Task):
    def __init__(self, title, description, due_date):
        super().__init__(title, description, due_date)
        self.type = "Personal"
    def to_dict(self):
        data = super().to_dict()
        data['type'] = self.type 
        return data


def createPersonalTask(title, description, due_date):
    return PersonalTask(title, description, due_date)


