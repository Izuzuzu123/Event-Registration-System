from backend.exceptions import ValidationError

class Event:
    def __init__(self, event_id, name, date, start_time, end_time, venue, department, capacity):
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Event name is required.")
        if not isinstance(venue, str) or not venue.strip():
            raise ValidationError("Venue is required.")
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
            raise ValidationError("Capacity must be a positive integer.")
        if not department or not str(department).strip():
            raise ValidationError("Department is required.")

        self._event_id = event_id
        self._name = name.strip()
        self._date = date
        self._start_time = start_time
        self._end_time = end_time
        self._venue = venue.strip()
        self._department = str(department).strip()
        self._capacity = capacity

    @property
    def event_id(self):
        return self._event_id

    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._date

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def venue(self):
        return self._venue

    @property
    def department(self):
        return self._department

    @property
    def capacity(self):
        return self._capacity

    def update_details(self, **updates):
        allowed = {"name", "date", "start_time", "end_time", "venue", "department", "capacity"}
        unknown = set(updates) - allowed
        if unknown:
            raise ValidationError(f"Cannot update field(s): {', '.join(sorted(unknown))}")
        for field in ("name", "venue", "department"):
            if field in updates:
                value = updates[field]
                if not isinstance(value, str) or not value.strip():
                    raise ValidationError(f"{field.replace('_', ' ').title()} is required.")
                updates[field] = value.strip()
        if "capacity" in updates:
            capacity = updates["capacity"]
            if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
                raise ValidationError("Capacity must be a positive integer.")
        for field, value in updates.items():
            setattr(self, "_" + field, value)

    def display_event(self):
        print(f"\nEvent ID: {self.event_id}")
        print(f"Event: {self.name}")
        print(f"Date: {self.date}")
        print(f"Time: {self.start_time} - {self.end_time}")
        print(f"Venue: {self.venue}")
        print(f"Department: {self.department}")
        print(f"Capacity: {self.capacity}")