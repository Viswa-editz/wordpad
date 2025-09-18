import os, datetime, webbrowser
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
from drawpad import DrawPad

def create_insert_tab(notebook, api):
    text = api.text
    tab = tk.Frame(notebook, padx=6, pady=6)
    notebook.add(tab, text="Insert")

    # Picture
    def insert_picture():
        path = filedialog.askopenfilename(title="Select image",
                    filetypes=[("Images","*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if not path: return
        try:
            img = Image.open(path)
            img.thumbnail((800, 800))
            ph = ImageTk.PhotoImage(img)
            (api._img_refs if hasattr(api, "_img_refs") else setattr(api, "_img_refs", []) or api._img_refs).append(ph)
            text.image_create("insert", image=ph)
            text.insert("insert", "\n")
        except Exception as e:
            messagebox.showerror("Insert error", str(e))
    tk.Button(tab, text="Picture", command=insert_picture).grid(row=0, column=0, padx=4, pady=4)

    # Paint Drawing
    tk.Button(tab, text="Paint Drawing", command=lambda: DrawPad(text, api.insert_image_from_path)).grid(row=0, column=1, padx=4)

    # Date / Time
    def insert_datetime():
        text.insert("insert", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    tk.Button(tab, text="Date/Time", command=insert_datetime).grid(row=0, column=2, padx=4)

    # Object (attach a file as clickable path)
    def insert_object():
        p = filedialog.askopenfilename(title="Attach object")
        if not p: return
        label = os.path.basename(p)
        start = text.index("insert")
        text.insert("insert", f"[Open: {label}]")
        end = text.index("insert")
        tag = f"obj_{start.replace('.','_')}"
        text.tag_add(tag, start, end)
        text.tag_config(tag, foreground="blue", underline=1)
        text.tag_bind(tag, "<Button-1>", lambda e, path=p: webbrowser.open(f"file:///{path}"))
    tk.Button(tab, text="Object", command=insert_object).grid(row=0, column=3, padx=4)
