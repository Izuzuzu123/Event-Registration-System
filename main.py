from backend.manager import EventManager
from backend.event import Event
from backend.users import Student
from backend.exceptions import (
    EventNotFoundError,
    EventFullError,
    DuplicateRegistrationError,
    RegistrationNotFoundError,
    ValidationError,
)

from frontend.registration_form import MinimalistEventForm

if __name__ == "__main__":
    app = MinimalistEventForm()
    app.mainloop()

if __name__ == "__main__":
    manager = EventManager()

    event1 = Event(
        1, "CCS Night", "2026-11-20",
        "9:00 PM", "5:00 AM",
        "LSPU SCC Activity Center", "CCS", 50
    )

    student1 = Student(
        "Shaira Ladeza", "2026-001",
        "2nd Year", "BSCS-2B", "CCS"
    )

    try:
        manager.add_event(event1)
        manager.view_events()

        # Search event
        manager.search_event("CCS")

        # Register student
        manager.register_student(student1, 1)

        # View registration
        manager.view_registrations()

        # Edit event
        manager.edit_event(1, venue="LSPU Main Activity Center")

        # Record attendance
        manager.time_in("2026-001", 1)
        manager.time_out("2026-001", 1)

        # View attendance
        manager.view_attendance()

    except (
        EventNotFoundError,
        EventFullError,
        DuplicateRegistrationError,
        RegistrationNotFoundError,
        ValidationError
    ) as error:
        print("Error:", error)