from abc import ABC, abstractmethod

from backend.exceptions import ValidationError


class User(ABC):
    def __init__(self, name, user_id):
        if not name.strip() or not user_id.strip():
            raise ValidationError("Name and user ID are required.")

        self.name = name.strip()
        self.user_id = user_id.strip()

    @abstractmethod
    def display_info(self):
        pass


class Student(User):
    def __init__(self, name, user_id, year_level, section, department):
        super().__init__(name, user_id)

        self.year_level = year_level
        self.section = section
        self.department = department

    def display_info(self):
        print(f"Student: {self.name}")
        print(f"Student ID: {self.user_id}")
        print(f"Year and Section: {self.year_level} {self.section}")
        print(f"Department: {self.department}")


class Admin(User):
    def display_info(self):
        print(f"Admin: {self.name}")
        print(f"Admin ID: {self.user_id}")