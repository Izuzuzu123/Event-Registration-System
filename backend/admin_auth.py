import hmac
import os
from backend.exceptions import AuthenticationError

class AdminAuthenticator:
    def __init__(self, email=None, password=None):
        self._email = email if email is not None else os.getenv("EVENT_ADMIN_EMAIL")
        self._password = password if password is not None else os.getenv("EVENT_ADMIN_PASSWORD")

        if not self._email or not self._password:
            raise ValueError("Set EVENT_ADMIN_EMAIL and EVENT_ADMIN_PASSWORD environment variables.")

    def authenticate(self, email, password):
        email_ok = hmac.compare_digest(str(email).strip().lower(), self._email.strip().lower())
        password_ok = hmac.compare_digest(str(password), self._password)
        if not (email_ok and password_ok):
            raise AuthenticationError("Invalid admin email or password.")
        return True