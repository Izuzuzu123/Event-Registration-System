class EventNotFoundError(Exception):
    pass


class EventFullError(Exception):
    pass


class DuplicateRegistrationError(Exception):
    pass


class RegistrationNotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass