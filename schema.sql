DROP DATABASE IF EXISTS event_registration;
CREATE DATABASE event_registration;
USE event_registration;

CREATE TABLE departments (
  department_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE students (
  student_id INT AUTO_INCREMENT PRIMARY KEY,
  student_number VARCHAR(20) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  year_level VARCHAR(20) NOT NULL,
  section VARCHAR(20) NOT NULL,
  department_id INT NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE events (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  event_date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  venue VARCHAR(150) NOT NULL,
  department_id INT NOT NULL,
  capacity INT NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE registrations (
  registration_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  event_id INT NOT NULL,
  registration_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (student_id, event_id),
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (event_id) REFERENCES events(event_id)
);

CREATE TABLE attendance (
  attendance_id INT AUTO_INCREMENT PRIMARY KEY,
  registration_id INT NOT NULL UNIQUE,
  time_in DATETIME NULL,
  time_out DATETIME NULL,
  FOREIGN KEY (registration_id) REFERENCES registrations(registration_id)
);

INSERT INTO departments (name) VALUES ('CCS');

INSERT INTO students (student_number, name, year_level, section, department_id)
VALUES ('2026-001', 'Shaira Ladeza', '2nd Year', 'BSCS-2B', 1);

INSERT INTO events (name, event_date, start_time, end_time, venue, department_id, capacity)
VALUES ('CCS Night', '2026-11-20', '21:00:00', '05:00:00',
        'LSPU SCC Activity Center', 1, 50);

CREATE VIEW v_events AS
SELECT
  e.event_id,
  e.name,
  e.event_date,
  e.start_time,
  e.end_time,
  e.venue,
  d.name AS department,
  e.capacity
FROM events e
JOIN departments d ON d.department_id = e.department_id;

CREATE VIEW v_students AS
SELECT
  s.student_id,
  s.student_number,
  s.name,
  s.year_level,
  s.section,
  d.name AS department
FROM students s
JOIN departments d ON d.department_id = s.department_id;

CREATE VIEW v_registrations AS
SELECT
  r.registration_id,
  s.student_number,
  s.name AS student_name,
  e.event_id,
  e.name AS event_name,
  r.registration_time
FROM registrations r
JOIN students s ON s.student_id = r.student_id
JOIN events   e ON e.event_id   = r.event_id;

CREATE VIEW v_attendance AS
SELECT
  a.attendance_id,
  s.student_number,
  s.name AS student_name,
  e.name AS event_name,
  a.time_in,
  a.time_out
FROM attendance a
JOIN registrations r ON r.registration_id = a.registration_id
JOIN students s      ON s.student_id      = r.student_id
JOIN events   e      ON e.event_id        = r.event_id;

CREATE ROLE IF NOT EXISTS 'admin_role'@'localhost';
CREATE ROLE IF NOT EXISTS 'student_role'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE ON event_registration.departments   TO 'admin_role'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON event_registration.students      TO 'admin_role'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON event_registration.events        TO 'admin_role'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON event_registration.registrations TO 'admin_role'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON event_registration.attendance    TO 'admin_role'@'localhost';
GRANT SELECT ON event_registration.v_events        TO 'admin_role'@'localhost';
GRANT SELECT ON event_registration.v_students      TO 'admin_role'@'localhost';
GRANT SELECT ON event_registration.v_registrations TO 'admin_role'@'localhost';
GRANT SELECT ON event_registration.v_attendance    TO 'admin_role'@'localhost';

GRANT SELECT ON event_registration.v_events        TO 'student_role'@'localhost';
GRANT SELECT ON event_registration.v_students      TO 'student_role'@'localhost';
GRANT SELECT ON event_registration.v_registrations TO 'student_role'@'localhost';
GRANT SELECT ON event_registration.v_attendance    TO 'student_role'@'localhost';
GRANT SELECT, INSERT, DELETE ON event_registration.registrations TO 'student_role'@'localhost';

CREATE USER IF NOT EXISTS 'event_admin'@'localhost'   IDENTIFIED BY 'admin123';
CREATE USER IF NOT EXISTS 'event_student'@'localhost' IDENTIFIED BY 'student123';

GRANT 'admin_role'@'localhost'   TO 'event_admin'@'localhost';
GRANT 'student_role'@'localhost' TO 'event_student'@'localhost';

SET DEFAULT ROLE 'admin_role'@'localhost'   TO 'event_admin'@'localhost';
SET DEFAULT ROLE 'student_role'@'localhost' TO 'event_student'@'localhost';