import tkinter as tk

from frontend.theme import BG_MAIN, CARD_BG, TEXT_WHITE, TEXT_MUTED


class UserDashboard(tk.Toplevel):
    def __init__(self, master, student_data):
        super().__init__(master)
        self.title("Student Dashboard")
        self.geometry("900x600")
        self.configure(bg=BG_MAIN)
        self.resizable(False, False)

        self.student_data = student_data
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=CARD_BG, height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header, text="Student Dashboard",
            font=("Helvetica", 16, "bold"),
            bg=CARD_BG, fg=TEXT_WHITE
        ).pack(side="left", padx=30)

        tk.Label(
            header, text=f"Welcome, {self.student_data['name']}",
            font=("Helvetica", 10),
            bg=CARD_BG, fg=TEXT_MUTED
        ).pack(side="right", padx=30)

        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True, padx=30, pady=20)

        profile = tk.Frame(body, bg=CARD_BG)
        profile.pack(fill="x", pady=(0, 20))

        tk.Label(
            profile, text="Your Information",
            font=("Helvetica", 12, "bold"),
            bg=CARD_BG, fg=TEXT_WHITE
        ).pack(anchor="w", padx=20, pady=(15, 10))

        info_frame = tk.Frame(profile, bg=CARD_BG)
        info_frame.pack(fill="x", padx=20, pady=(0, 15))

        rows = [
            ("Student Number", self.student_data["student_number"]),
            ("Full Name", self.student_data["name"]),
            ("Year Level", self.student_data["year_level"]),
            ("Section", self.student_data["section"]),
            ("Department", self.student_data["department"]),
        ]
        for i, (label, value) in enumerate(rows):
            tk.Label(
                info_frame, text=label,
                font=("Helvetica", 9, "bold"),
                bg=CARD_BG, fg=TEXT_MUTED
            ).grid(row=i, column=0, sticky="w", pady=4, padx=(0, 20))

            tk.Label(
                info_frame, text=value,
                font=("Helvetica", 10),
                bg=CARD_BG, fg=TEXT_WHITE
            ).grid(row=i, column=1, sticky="w", pady=4)

        events = tk.Frame(body, bg=CARD_BG)
        events.pack(fill="both", expand=True)

        tk.Label(
            events, text="Available Events",
            font=("Helvetica", 12, "bold"),
            bg=CARD_BG, fg=TEXT_WHITE
        ).pack(anchor="w", padx=20, pady=(15, 10))

        tk.Label(
            events,
            text="No events available at the moment.\n"
                 "Check back later for upcoming events.",
            font=("Helvetica", 10),
            bg=CARD_BG, fg=TEXT_MUTED,
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))