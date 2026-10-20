from abc import ABC, abstractmethod
import re
from backend.exceptions import ValidationError

VALID_YEAR_LEVELS = ("First Year", "Second Year", "Third Year", "Fourth Year")
VALID_PROGRAMS = ("BSCS", "BSIT")
SECTION_PATTERN = re.compile(r"^[1-4][A-Z]$")

class User(ABC):
    def __init__(self, name: str, user_id: str):
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Full name is required.")
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValidationError("Student number / user ID is required.")
        self._name = name.strip()
        self._user_id = user_id.strip()

    @property
    def name(self):
        return self._name

    @property
    def user_id(self):
        return self._user_id

    @abstractmethod
    def display_info(self):
        pass

class Student(User):
    def __init__(self, name: str, user_id: str, year_level: str, section: str, program: str, department: str = "College of Computer Studies"):
        super().__init__(name, user_id)
        if year_level not in VALID_YEAR_LEVELS:
            raise ValidationError("Year level must be First Year, Second Year, Third Year, or Fourth Year.")
        if program not in VALID_PROGRAMS:
            raise ValidationError("Program must be BSCS or BSIT.")
        if not isinstance(section, str) or not SECTION_PATTERN.fullmatch(section.strip()):
            raise ValidationError("Section must contain one digit (1-4) followed by one capital letter, e.g. 2B.")
        if not isinstance(department, str) or not department.strip():
            raise ValidationError("Department is required.")

        self._year_level = year_level
        self._section = section.strip()
        self._program = program
        self._department = department.strip()

    @property
    def year_level(self):
        return self._year_level

    @property
    def section(self):
        return self._section

    @property
    def program(self):
        return self._program

    @property
    def department(self):
        return self._department

    def display_info(self):
        print(f"Student: {self.name}")
        print(f"Student Number: {self.user_id}")
        print(f"Year Level: {self.year_level}")
        print(f"Section: {self.section}")
        print(f"Program: {self.program}")
        print(f"Department: {self.department}")

class Admin(User):
    def display_info(self):
        print(f"Admin: {self.name}")
        print(f"Admin ID: {self.user_id}")