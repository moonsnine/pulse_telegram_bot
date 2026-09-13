from abc import abstractmethod, ABC
from datetime import datetime

class BaseItem(ABC):
    def __init__(self, id, created_at = datetime.now().date()):
        self.id = id
        self.created_at = created_at

    @abstractmethod
    def to_dict(self):
        return {"id": self.id, "created_at": self.created_at}

    @classmethod
    @abstractmethod
    def from_dict(cls, d):
        note = cls(d["id"], d["created_at"])
        return note

    @abstractmethod
    def __repr__(self):
        return f"{self.id}. {self.created_at}"

class Note(BaseItem):
    def __init__(self, name, created_at):
        super().__init__(created_at)
        self.name = name

    def to_dict(self):
        return {"name": self.name, "created_at": self.created_at}

    @classmethod
    def from_dict(cls, d):
        note = cls(d["name"], d["created_at"])
        return note

    def __repr__(self):
        return f"{self.name} - {self.created_at}"

class Expense(Note):
    def __init__(self, created_at, value):
        super().__init__(created_at)
        self.value = value

    def __repr__(self):
        return f"{self.value} - {self.created_at}"