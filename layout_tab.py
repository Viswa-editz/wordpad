import tkinter as tk
from tkinter import simpledialog, messagebox

def create_layout_tab(notebook, api):
    text = api.text
    tab = tk.Frame(notebook, padx=6, pady=6)
    notebook.add(tab, text="Layout")

    # Margins (padding)
    tk.Button(tab, text="Narrow", command=lambda: text.config(padx=6, pady=6)).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(tab, text="Normal", command=lambda: text.config(padx=12, pady=12)).grid(row=0, column=1)
    tk.Button(tab, text="Wide", command=lambda: text.config(padx=24, pady=24)).grid(row=0, column=2)

    # Orientation & Paper Size (stored only)
    def page_setup():
        size = simpledialog.askstring("Paper size", "A4 / Letter / Legal", initialvalue=api.page_setup.get("size","A4"))
        orient = simpledialog.askstring("Orientation", "Portrait / Landscape", initialvalue=api.page_setup.get("orientation","Portrait"))
        margins = simpledialog.askstring("Margins", "top,right,bottom,left (inches)", initialvalue="1,1,1,1")
        try:
            api.page_setup = {"size": size or "A4", "orientation": orient or "Portrait",
                              "margins": tuple(float(x.strip()) for x in margins.split(","))}
            messagebox.showinfo("Saved", f"Page: {api.page_setup}")
        except Exception:
            messagebox.showwarning("Invalid", "Use format: 1,1,1,1")
    tk.Button(tab, text="Page Setup…", command=page_setup).grid(row=1, column=0, pady=8)

    # Paragraph indent (left/right)
    tk.Button(tab, text="Increase Indent", command=lambda: text.insert("insert linestart", "\t")).grid(row=2, column=0, pady=4)
    def dec_indent():
        line = text.get("insert linestart", "insert linestart +1c")
        if line == "\t": text.delete("insert linestart", "insert linestart +1c")
    tk.Button(tab, text="Decrease Indent", command=dec_indent).grid(row=2, column=1)
