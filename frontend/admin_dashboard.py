import tkinter as tk
from tkinter import ttk

from frontend.theme import BG_MAIN, CARD_BG, TEXT_WHITE, TEXT_MUTED, INPUT_BG


class AdminDashboard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Admin Dashboard")
        self.geometry("1000x650")
        self.configure(bg=BG_MAIN)
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=CARD_BG, height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header, text="Admin Dashboard",
            font=("Helvetica", 16, "bold"),
            bg=CARD_BG, fg=TEXT_WHITE
        ).pack(side="left", padx=30)

        tk.Label(
            header, text="Manage events, students, and registrations",
            font=("Helvetica", 10),
            bg=CARD_BG, fg=TEXT_MUTED
        ).pack(side="right", padx=30)

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook", background=BG_MAIN, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=CARD_BG, foreground=TEXT_MUTED,
            padding=[20, 10], borderwidth=0,
            font=("Helvetica", 10, "bold"),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", INPUT_BG)],
            foreground=[("selected", TEXT_WHITE)],
        )

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=30, pady=20)

        notebook.add(self._events_tab(notebook), text="Events")
        notebook.add(self._students_tab(notebook), text="Students")
        notebook.add(self._registrations_tab(notebook), text="Registrations")

    def _events_tab(self, parent):
        frame = tk.Frame(parent, bg=CARD_BG)
        self._table(
            frame,
            columns=("ID", "Event", "Date", "Venue", "Department", "Capacity"),
            rows=[
                ("1", "CCS Night", "2026-11-20",
                 "LSPU SCC Activity Center", "CCS", "50"),
            ],
        )
        return frame

    def _students_tab(self, parent):
        frame = tk.Frame(parent, bg=CARD_BG)
        self._table(
            frame,
            columns=("Student #", "Name", "Year", "Section", "Department"),
            rows=[
                ("2026-001", "Shaira Ladeza", "2nd Year", "BSCS-2B", "CCS"),
            ],
        )
        return frame

    def _registrations_tab(self, parent):
        frame = tk.Frame(parent, bg=CARD_BG)
        self._table(
            frame,
            columns=("Student #", "Student", "Event", "Registered At"),
            rows=[
                ("2026-001", "Shaira Ladeza", "CCS Night", "2026-10-13 10:00"),
            ],
        )
        return frame

    def _table(self, parent, columns, rows):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="w", width=150)

        for row in rows:
            tree.insert("", "end", values=row)

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)