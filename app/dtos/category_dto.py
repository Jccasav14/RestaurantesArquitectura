class CategoryDTO:
    def __init__(self, id=None, name=''):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
