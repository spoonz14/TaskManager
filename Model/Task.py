
class Task:
    def __init__(self, title, description, due_date):
        self._title = title
        self._description = description
        self._due_date = due_date

    def __str__(self):
        return f'Task(title={self._title}, description={self._description}, due_date={self._due_date})'

    def to_dict(self):
        return{
            'title': self._title,
            'description': self._description,
            'due_date': self._due_date
        }
        
