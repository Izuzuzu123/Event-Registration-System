from backend.exceptions import (
    EventNotFoundError, EventFullError, DuplicateRegistrationError, 
    RegistrationNotFoundError, ValidationError
)
from backend.registration import Registration
from backend.attendance import Attendance

class EventManager:
    def __init__(self):
        self.events = []
        self.registrations = []

    def add_event(self, event):
        for existing in self.events:
            if existing.event_id == event.event_id:
                raise ValidationError("Event ID already exists.")
        self.events.append(event)

    def view_events(self):
        if not self.events:
            print("No events available.")
            return
        for event in self.events:
            event.display_event()

    def search_event(self, keyword):
        keyword = keyword.strip().lower()
        results = [
            event for event in self.events
            if keyword in event.name.lower() or keyword in event.department.lower() or keyword in event.venue.lower()
        ]
        return results

    def find_event(self, event_id):
        for event in self.events:
            if event.event_id == event_id:
                return event
        raise EventNotFoundError("Event does not exist.")

    def edit_event(self, event_id, **updates):
        event = self.find_event(event_id)
        new_capacity = updates.get("capacity", event.capacity)
        registered_count = sum(1 for reg in self.registrations if reg.event.event_id == event_id)
        
        if not isinstance(new_capacity, int) or new_capacity <= 0:
            raise ValidationError("Capacity must be a positive integer.")
        if new_capacity < registered_count:
            raise ValidationError("Capacity cannot be less than current registrations.")
        
        event.update_details(**updates)

    def delete_event(self, event_id):
        event = self.find_event(event_id)
        has_registrations = any(reg.event.event_id == event_id for reg in self.registrations)
        if has_registrations:
            raise ValidationError("Cannot delete an event with registrations.")
        self.events.remove(event)

    def register_student(self, student, event_id):
        event = self.find_event(event_id)
        for reg in self.registrations:
            if reg.student.user_id == student.user_id and reg.event.event_id == event_id:
                raise DuplicateRegistrationError("Student is already registered for this event.")
        
        count = sum(1 for reg in self.registrations if reg.event.event_id == event_id)
        if count >= event.capacity:
            raise EventFullError("Event is already full.")

        registration = Registration(student, event)
        self.registrations.append(registration)
        return registration

    def view_registrations(self):
        if not self.registrations:
            print("No registrations yet.")
            return
        for reg in self.registrations:
            reg.display_registration()

    def cancel_registration(self, student_id, event_id):
        for reg in self.registrations:
            if reg.student.user_id == student_id and reg.event.event_id == event_id:
                if reg.attendance is not None:
                    raise ValidationError("Cannot cancel after attendance has started.")
                self.registrations.remove(reg)
                return
        raise RegistrationNotFoundError("Matching registration was not found.")

    def time_in(self, student_id, event_id):
        registration = self._find_registration(student_id, event_id)
        if registration.attendance is None:
            registration.attendance = Attendance(registration)
        registration.attendance.record_time_in()

    def time_out(self, student_id, event_id):
        registration = self._find_registration(student_id, event_id)
        if registration.attendance is None:
            raise ValidationError("Time-in must be recorded first.")
        registration.attendance.record_time_out()

    def _find_registration(self, student_id, event_id):
        for reg in self.registrations:
            if reg.student.user_id == student_id and reg.event.event_id == event_id:
                return reg
        raise RegistrationNotFoundError("Student is not registered for this event.")

    def view_attendance(self):
        found = False
        for reg in self.registrations:
            if reg.attendance is not None:
                reg.display_attendance()
                found = True
        if not found:
            print("No attendance records yet.")