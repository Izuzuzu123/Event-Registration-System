from flask import Flask, render_template, request, redirect, flash, session, url_for
from backend.Database import Database
from backend.users import Student
from backend.exceptions import ValidationError, AuthenticationError
from backend.admin_auth import AdminAuthenticator

app = Flask(__name__)
app.secret_key = "super_secret_key_for_sessions"

@app.route("/")
def index():
    return render_template("index.html")

# NEW ROUTE: User Event List
@app.route("/events")
def user_events():
    # Fetch events from MySQL
    db = Database()
    db.cursor.execute("SELECT event_id, name, event_date, start_time, end_time, venue, capacity FROM v_events")
    events = db.cursor.fetchall()
    db.close()
    
    return render_template("events.html", events=events)

# REGISTRATION FORM
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        student_id = request.form.get("student_id")
        year = request.form.get("year")
        section = request.form.get("section")
        program = request.form.get("program")
        dept = request.form.get("dept")

        try:
            student = Student(name=name, user_id=student_id, year_level=year, section=section, program=program, department=dept)
        except ValidationError as e:
            flash(str(e), "error")
            return redirect("/register")

        try:
            db = Database()
            if db.student_exists(student_id):
                db.close()
                flash("Student number already exists.", "error")
                return redirect("/register")
            
            db.save_student(student)
            db.close()
            flash("Registration saved! You can now log in.", "success")
            return redirect(url_for("user_events")) 
        except Exception as e:
            flash(f"Database Error: {e}", "error")
            return redirect("/register")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            auth = AdminAuthenticator(email="admin@gmail.com", password="admin123")
            auth.authenticate(username, password)
            session["user"] = "Admin"
            session["role"] = "admin"
            return redirect(url_for("admin_dashboard"))
        except AuthenticationError as e:
            flash(str(e), "error")

    return render_template("login.html")

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    
    db = Database()
    db.cursor.execute("SELECT student_number, name, year_level, section FROM v_students")
    students = db.cursor.fetchall()
    db.close()

    return render_template("admin_dashboard.html", students=students)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)