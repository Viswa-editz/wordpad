import tkinter as tk
from tkinter import colorchooser

def create_design_tab(notebook, api):
    text = api.text
    tab = tk.Frame(notebook, padx=6, pady=6)
    notebook.add(tab, text="Design")

    # Page color
    tk.Button(tab, text="Page Color", command=lambda: _pick_bg(text)).grid(row=0, column=0, padx=4, pady=4)

    # Themes
    tk.Button(tab, text="Light", command=lambda: text.config(bg="white", fg="black")).grid(row=0, column=1)
    tk.Button(tab, text="Dark", command=lambda: text.config(bg="#1f1f1f", fg="#eaeaea")).grid(row=0, column=2)
    tk.Button(tab, text="Sepia", command=lambda: text.config(bg="#f4ecd8", fg="#333333")).grid(row=0, column=3)

    # Zoom
    tk.Button(tab, text="Zoom +", command=lambda: api.change_zoom(+2)).grid(row=1, column=0, pady=6)
    tk.Button(tab, text="Zoom −", command=lambda: api.change_zoom(-2)).grid(row=1, column=1)

    # Word wrap
    def toggle_wrap():
        text.config(wrap=("none" if text.cget("wrap") == "word" else "word"))
    tk.Button(tab, text="Toggle Word Wrap", command=toggle_wrap).grid(row=1, column=2, padx=6)

    # Ruler & Status
    tk.Button(tab, text="Show/Hide Ruler", command=api.toggle_ruler).grid(row=2, column=0, pady=6)
    tk.Button(tab, text="Show/Hide Status", command=api.toggle_status).grid(row=2, column=1)

def _pick_bg(text):
    c = colorchooser.askcolor()[1]
    if c: text.config(bg=c)
