import tkinter as tk
from tkinter import messagebox

from frontend.theme import (
    BG_MAIN, CARD_BG, TEXT_WHITE, TEXT_MUTED,
    INPUT_BG, INPUT_BORDER, BTN_BG, BTN_FG, BTN_HOVER,
)
from frontend.helpers import make_entry, field_label
from frontend.user_dashboard import UserDashboard
from frontend.admin_dashboard import AdminDashboard


class MinimalistEventForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Event Registration")
        self.geometry("1100x750")
        self.configure(bg=BG_MAIN)
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        card = tk.Frame(self, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=INPUT_BORDER)
        card.place(relx=0.5, rely=0.5, anchor="center", width=900, height=680)

        container = tk.Frame(card, bg=CARD_BG)
        container.pack(fill="both", expand=True, padx=50, pady=40)

        tk.Label(
            container,
            text="Sign up for our event",
            font=("Helvetica", 22, "bold"),
            bg=CARD_BG, fg=TEXT_WHITE
        ).pack(anchor="w")

        desc_text = (
            "Complete the registration form to secure your spot and gain\n"
            "access to discussions and Q&A. We look forward to seeing you there."
        )
        tk.Label(
            container,
            text=desc_text,
            font=("Helvetica", 10),
            bg=CARD_BG, fg=TEXT_MUTED,
            justify="left"
        ).pack(anchor="w", pady=(8, 25))

        columns = tk.Frame(container, bg=CARD_BG)
        columns.pack(fill="both", expand=True)

        left = tk.Frame(columns, bg=CARD_BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))

        right = tk.Frame(columns, bg=CARD_BG)
        right.pack(side="right", fill="both", expand=True, padx=(20, 0))

        field_label(left, "Full Name *")
        self.full_name_entry = make_entry(left, "Ex. Juan Dela Cruz")

        field_label(left, "Student Number *")
        self.student_number_entry = make_entry(left, "Ex. 2026-001")

        field_label(left, "Year Level *")
        self.year_level_entry = make_entry(left, "Ex. 2nd Year")

        field_label(left, "Section *")
        self.section_entry = make_entry(left, "Ex. BSCS-2B")

        field_label(left, "Department *")
        self.department_entry = make_entry(left, "Ex. CCS")

        tk.Label(
            right, text="Event Details",
            font=("Helvetica", 12, "bold"),
            bg=CARD_BG, fg=TEXT_WHITE
        ).pack(anchor="w", pady=(0, 12))

        event_box = tk.Frame(right, bg=INPUT_BG)
        event_box.pack(fill="x")

        info_rows = [
            ("Event", "CCS Night"),
            ("Date", "2026-11-20"),
            ("Time", "9:00 PM - 5:00 AM"),
            ("Venue", "LSPU SCC Activity Center"),
            ("Department", "CCS"),
            ("Capacity", "50 slots"),
        ]
        for label, value in info_rows:
            row = tk.Frame(event_box, bg=INPUT_BG)
            row.pack(fill="x", padx=15, pady=6)

            tk.Label(
                row, text=label,
                font=("Helvetica", 9, "bold"),
                bg=INPUT_BG, fg=TEXT_MUTED
            ).pack(anchor="w")

            tk.Label(
                row, text=value,
                font=("Helvetica", 10),
                bg=INPUT_BG, fg=TEXT_WHITE
            ).pack(anchor="w")

        button_row = tk.Frame(container, bg=CARD_BG)
        button_row.pack(fill="x", pady=(25, 0))

        tk.Button(
            button_row, text="Next",
            font=("Helvetica", 11, "bold"),
            bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_HOVER, activeforeground=BTN_FG,
            relief="flat", cursor="hand2",
            command=self._on_submit
        ).pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 6))

        tk.Button(
            button_row, text="Admin Login",
            font=("Helvetica", 11, "bold"),
            bg=INPUT_BG, fg=TEXT_WHITE,
            activebackground=INPUT_BORDER, activeforeground=TEXT_WHITE,
            relief="flat", cursor="hand2",
            command=self._open_admin
        ).pack(side="right", fill="x", expand=True, ipady=10, padx=(6, 0))

    def _on_submit(self):
        name = self.full_name_entry.get().strip()
        student_number = self.student_number_entry.get().strip()
        year_level = self.year_level_entry.get().strip()
        section = self.section_entry.get().strip()
        department = self.department_entry.get().strip()

        if name in ("", "Ex. Juan Dela Cruz"):
            messagebox.showerror("Incomplete", "Please enter your full name.")
            return

        if student_number in ("", "Ex. 2026-001"):
            messagebox.showerror("Incomplete", "Please enter your student number.")
            return

        if year_level in ("", "Ex. 2nd Year"):
            messagebox.showerror("Incomplete", "Please enter your year level.")
            return

        if section in ("", "Ex. BSCS-2B"):
            messagebox.showerror("Incomplete", "Please enter your section.")
            return

        if department in ("", "Ex. CCS"):
            messagebox.showerror("Incomplete", "Please enter your department.")
            return

        student_data = {
            "name": name,
            "student_number": student_number,
            "year_level": year_level,
            "section": section,
            "department": department,
        }

        messagebox.showinfo(
            "Success",
            f"Registration recorded!\n\n"
            f"Name: {name}\n"
            f"Student Number: {student_number}\n"
            f"Year Level: {year_level}\n"
            f"Section: {section}\n"
            f"Department: {department}"
        )

        self.withdraw()
        UserDashboard(self, student_data)

    def _open_admin(self):
        AdminDashboard(self)