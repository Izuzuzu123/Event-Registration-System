import os
import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "event_admin"),
            password=os.getenv("DB_PASSWORD", "admin123"), 
            database=os.getenv("DB_NAME", "event_registration"),
        )
        self.cursor = self.conn.cursor()

    def close(self):
        if getattr(self, "cursor", None):
            self.cursor.close()
        if getattr(self, "conn", None) and self.conn.is_connected():
            self.conn.close()

    def get_or_create_department(self, name):
        name = name.strip()
        self.cursor.execute("SELECT department_id FROM departments WHERE name = %s", (name,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        self.cursor.execute("INSERT INTO departments (name) VALUES (%s)", (name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def student_exists(self, student_number):
        self.cursor.execute("SELECT student_id FROM students WHERE student_number = %s", (student_number,))
        return self.cursor.fetchone() is not None

    def save_student(self, student):
        department_id = self.get_or_create_department(student.department)
        self.cursor.execute(
            """INSERT INTO students
               (student_number, name, year_level, section, department_id)
               VALUES (%s, %s, %s, %s, %s)""",
            (student.user_id, student.name, student.year_level, student.section, department_id)
        )
        self.conn.commit()