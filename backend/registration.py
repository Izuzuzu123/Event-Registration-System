from datetime import datetime


class Registration:
    def __init__(self, student, event):
        self.student = student
        self.event = event
        self.registration_time = datetime.now()
        self.attendance = None

    def display_registration(self):
        print(f"\nStudent: {self.student.name}")
        print(f"Student ID: {self.student.user_id}")
        print(f"Event: {self.event.name}")
        print(
            "Registered at:",
            self.registration_time.strftime("%Y-%m-%d %H:%M")
        )