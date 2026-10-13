from datetime import datetime

from backend.exceptions import ValidationError


class Attendance:
    def __init__(self, registration):
        self.registration = registration
        self.time_in = None
        self.time_out = None

    def record_time_in(self):
        if self.time_in is not None:
            raise ValidationError("Time-in has already been recorded.")

        self.time_in = datetime.now()
        print("Time-in recorded successfully.")

    def record_time_out(self):
        if self.time_in is None:
            raise ValidationError("Record time-in first.")

        if self.time_out is not None:
            raise ValidationError("Time-out has already been recorded.")

        self.time_out = datetime.now()
        print("Time-out recorded successfully.")

    def display_attendance(self):
        student = self.registration.student

        print(f"\nStudent: {student.name}")
        print(f"Event: {self.registration.event.name}")
        print("Time-in:", self.time_in or "Not recorded")
        print("Time-out:", self.time_out or "Not recorded")