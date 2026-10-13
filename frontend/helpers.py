import tkinter as tk

from frontend.theme import (
    CARD_BG, INPUT_BG, INPUT_FG, INPUT_BORDER,
    TEXT_WHITE, TEXT_MUTED, BTN_BG, BTN_FG, BTN_HOVER,
)


def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg=TEXT_MUTED)

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=INPUT_FG)

    def on_focus_out(event):
        if not entry.get().strip():
            entry.insert(0, placeholder)
            entry.config(fg=TEXT_MUTED)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def make_entry(parent, placeholder):
    entry = tk.Entry(
        parent, font=("Helvetica", 11),
        bg=INPUT_BG, fg=INPUT_FG,
        insertbackground=TEXT_WHITE, relief="flat"
    )
    entry.pack(fill="x", pady=(4, 12), ipady=7)
    add_placeholder(entry, placeholder)
    return entry


def field_label(parent, text):
    tk.Label(
        parent, text=text,
        font=("Helvetica", 9, "bold"),
        bg=CARD_BG, fg=TEXT_WHITE
    ).pack(anchor="w")


def styled_button(parent, text, command, width=None):
    btn = tk.Button(
        parent, text=text,
        font=("Helvetica", 11, "bold"),
        bg=BTN_BG, fg=BTN_FG,
        activebackground=BTN_HOVER, activeforeground=BTN_FG,
        relief="flat", cursor="hand2",
        command=command
    )
    if width:
        btn.config(width=width)
    btn.pack(fill="x", ipady=8, pady=(4, 0))
    return btn