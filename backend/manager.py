from backend.exceptions import (
    EventNotFoundError,
    EventFullError,
    DuplicateRegistrationError,
    RegistrationNotFoundError,
    ValidationError,
)
from backend.registration import Registration
from backend.attendance import Attendance


class EventManager:
    def __init__(self):
        self.events = []
        self.registrations = []

    # ADD EVENT
    def add_event(self, event):
        for existing in self.events:
            if existing.event_id == event.event_id:
                raise ValidationError("Event ID already exists.")

        self.events.append(event)
        print("Event added successfully.")

    # VIEW EVENTS
    def view_events(self):
        if not self.events:
            print("No events available.")
            return

        for event in self.events:
            event.display_event()

    # SEARCH FOR EITHER (NAME, DEPARTMENT, OR VENUE)
    def search_event(self, keyword):
        keyword = keyword.strip().lower()

        results = [
            event for event in self.events
            if keyword in event.name.lower()
            or keyword in event.department.lower()
            or keyword in event.venue.lower()
        ]

        if not results:
            print("No matching events found.")
        else:
            for event in results:
                event.display_event()

        return results

    # FIND EVENT BY ID
    def find_event(self, event_id):
        for event in self.events:
            if event.event_id == event_id:
                return event

        raise EventNotFoundError("Event does not exist.")

    # EDIT EVENT DETAILS
    def edit_event(self, event_id, **updates):
        event = self.find_event(event_id)

        allowed_fields = {
            "name", "date", "start_time", "end_time",
            "venue", "department", "capacity"
        }

        for field in updates:
            if field not in allowed_fields:
                raise ValidationError(f"Cannot update field: {field}")

        new_capacity = updates.get("capacity", event.capacity)

        registered_count = sum(
            1 for registration in self.registrations
            if registration.event.event_id == event_id
        )

        if not isinstance(new_capacity, int) or new_capacity <= 0:
            raise ValidationError("Capacity must be a positive integer.")

        if new_capacity < registered_count:
            raise ValidationError(
                "Capacity cannot be less than current registrations."
            )

        for field, value in updates.items():
            if field in ("name", "venue"):
                if not isinstance(value, str) or not value.strip():
                    raise ValidationError(f"{field} cannot be empty.")
                value = value.strip()

            setattr(event, field, value)

        print("Event updated successfully.")

    # DELETE EVENT
    def delete_event(self, event_id):
        event = self.find_event(event_id)

        has_registrations = any(
            registration.event.event_id == event_id
            for registration in self.registrations
        )

        if has_registrations:
            raise ValidationError(
                "Cannot delete an event with registrations. "
                "Handle the registrations first."
            )

        self.events.remove(event)
        print("Event deleted successfully.")

    # REGISTER STUDENT
    def register_student(self, student, event_id):
        event = self.find_event(event_id)

        for registration in self.registrations:
            if (
                registration.student.user_id == student.user_id
                and registration.event.event_id == event_id
            ):
                raise DuplicateRegistrationError(
                    "Student is already registered for this event."
                )

        count = sum(
            1 for registration in self.registrations
            if registration.event.event_id == event_id
        )

        if count >= event.capacity:
            raise EventFullError("Event is already full.")

        registration = Registration(student, event)
        self.registrations.append(registration)

        print("Student registered successfully.")
        return registration

    # VIEW ALL REGISTRATIONS
    def view_registrations(self):
        if not self.registrations:
            print("No registrations yet.")
            return

        for registration in self.registrations:
            registration.display_registration()

    # CANCEL REGISTRATION
    def cancel_registration(self, student_id, event_id):
        for registration in self.registrations:
            if (
                registration.student.user_id == student_id
                and registration.event.event_id == event_id
            ):
                if registration.attendance is not None:
                    raise ValidationError(
                        "Cannot cancel after attendance has started."
                    )

                self.registrations.remove(registration)
                print("Registration cancelled successfully.")
                return

        raise RegistrationNotFoundError(
            "Matching registration was not found."
        )

    # RECORD TIME-IN
    def time_in(self, student_id, event_id):
        registration = self._find_registration(student_id, event_id)

        if registration.attendance is None:
            registration.attendance = Attendance(registration)

        registration.attendance.record_time_in()

    # RECORD TIME-OUT
    def time_out(self, student_id, event_id):
        registration = self._find_registration(student_id, event_id)

        if registration.attendance is None:
            raise ValidationError("Time-in must be recorded first.")

        registration.attendance.record_time_out()

    # FIND A STUDENT'S REGISTRATION
    def _find_registration(self, student_id, event_id):
        for registration in self.registrations:
            if (
                registration.student.user_id == student_id
                and registration.event.event_id == event_id
            ):
                return registration

        raise RegistrationNotFoundError(
            "Student is not registered for this event."
        )

    # VIEW ATTENDANCE
    def view_attendance(self):
        found = False

        for registration in self.registrations:
            if registration.attendance is not None:
                registration.attendance.display_attendance()
                found = True

        if not found:
            print("No attendance records yet.")