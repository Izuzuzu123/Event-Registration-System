from backend.exceptions import ValidationError


class Event:
    def __init__(
        self, event_id, name, date, start_time,
        end_time, venue, department, capacity
    ):
        if not name.strip() or not venue.strip():
            raise ValidationError("Event name and venue are required.")

        if not isinstance(capacity, int) or capacity <= 0:
            raise ValidationError("Capacity must be a positive integer.")

        self.event_id = event_id
        self.name = name.strip()
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.venue = venue.strip()
        self.department = department
        self.capacity = capacity

    def display_event(self):
        print(f"\nEvent ID: {self.event_id}")
        print(f"Event: {self.name}")
        print(f"Date: {self.date}")
        print(f"Time: {self.start_time} - {self.end_time}")
        print(f"Venue: {self.venue}")
        print(f"Department: {self.department}")
        print(f"Capacity: {self.capacity}")