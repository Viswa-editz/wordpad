import os, pickle, datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from PIL import Image, ImageTk

from auth import init_db, register_user, find_by_password
from utils import APP_TITLE, center_window
from home_tab import create_home_tab
from insert_tab import create_insert_tab
from design_tab import create_design_tab
from layout_tab import create_layout_tab
from references_tab import create_references_tab

class EditorAPI:
    """Exposes the editor surface to tabs."""
    def __init__(self, text, status, root):
        self.text, self.status, self.root = text, status, root
        self._img_refs = []
        self.font_family = tk.StringVar(value="Segoe UI")
        self.font_size = tk.IntVar(value=12)
        self.page_setup = {"size":"A4","orientation":"Portrait","margins":(1,1,1,1)}
        self.bibliography = []
        self._ruler = None
        self._status_visible = True

    # helpers used by tabs
    def insert_image_from_path(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((800, 800))
            ph = ImageTk.PhotoImage(img)
            self._img_refs.append(ph)
            self.text.image_create("insert", image=ph)
            self.text.insert("insert","\n")
        except Exception as e:
            messagebox.showerror("Insert error", str(e))

    def insert_image_dialog(self):
        p = filedialog.askopenfilename(title="Select image", filetypes=[("Images","*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if p: self.insert_image_from_path(p)

    def insert_datetime(self):
        self.text.insert("insert", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    def change_zoom(self, delta):
        new = max(6, min(72, self.font_size.get() + delta))
        self.font_size.set(new)
        base = font.Font(family=self.font_family.get(), size=new)
        self.text.configure(font=base)
        self.status.config(text=f"Zoom {new}pt")

    def toggle_ruler(self):
        if self._ruler and self._ruler.winfo_exists():
            self._ruler.destroy(); self._ruler = None
            return
        self._ruler = tk.Canvas(self.root, height=20, bg="#f3f3f3"); self._ruler.pack(fill="x", side="top")
        w = self._ruler.winfo_reqwidth()
        for i in range(0, 2000, 50):
            x = i // 2
            self._ruler.create_line(x, 0, x, 20)
            self._ruler.create_text(x+5, 10, text=str(i//10), anchor="w", font=("Segoe UI", 8))

    def toggle_status(self):
        self._status_visible = not self._status_visible
        self.status.pack_forget()
        if self._status_visible:
            self.status.pack(side="bottom", fill="x")

class LoginWindow:
    def __init__(self, root):
        self.root = root
        init_db()
        root.title(f"{APP_TITLE} - Login")
        root.geometry("380x240"); root.resizable(False, False)
        frm = tk.Frame(root, padx=16, pady=12); frm.pack(expand=True, fill="both")
        tk.Label(frm, text=APP_TITLE, font=("Segoe UI", 14, "bold")).pack(pady=(0,8))
        tk.Label(frm, text="Enter password to login (or create new account)").pack()
        self.pw = tk.StringVar()
        tk.Entry(frm, textvariable=self.pw, show="*", width=30).pack(pady=(6,8))
        tk.Button(frm, text="Login (password only)", width=30, command=self.login).pack(pady=(4,6))
        tk.Button(frm, text="Create New Account", width=30, command=self.register).pack()

    def login(self):
        pwd = self.pw.get().strip()
        if not pwd: messagebox.showwarning("Missing","Enter password"); return
        matches = find_by_password(pwd)
        if not matches: messagebox.showerror("No match","No account with that password."); return
        if len(matches) > 1:
            names = ", ".join(m["name"] for m in matches)
            name = tk.simpledialog.askstring("Pick account", f"Multiple accounts match.\nNames: {names}\nType exact name:")
            if not name: return
            user = next((m for m in matches if m["name"] == name), None)
            if not user: messagebox.showerror("No match","Name not found."); return
        else:
            user = matches[0]
        self.open_editor(user["name"])

    def register(self):
        name = tk.simpledialog.askstring("Name","Enter name:")
        age  = tk.simpledialog.askstring("Age","Enter age:")
        pwd  = tk.simpledialog.askstring("Password","Set password:", show="*")
        cpwd = tk.simpledialog.askstring("Confirm","Confirm password:", show="*")
        if not name or not pwd or pwd != cpwd:
            messagebox.showerror("Error","Invalid details or passwords do not match."); return
        ok, msg = register_user(name, age or "", pwd)
        messagebox.showinfo("Info", msg)
        if ok: self.open_editor(name)

    def open_editor(self, username):
        self.root.destroy()
        win = tk.Tk()
        EditorWindow(win, username)
        win.mainloop()

class EditorWindow:
    def __init__(self, win, username):
        self.win = win
        win.title(f"{APP_TITLE} - {username}")
        center_window(win)
        # ribbon (notebook) on top
        self.ribbon = ttk.Notebook(win)
        self.ribbon.pack(side="top", fill="x")

        # text area
        self.text = tk.Text(win, wrap="word", undo=True, font=("Consolas", 12))
        self.text.pack(fill="both", expand=True)

        # status bar
        self.status = tk.Label(win, text="Ready", anchor="w")
        self.status.pack(side="bottom", fill="x")

        # API for tabs
        self.api = EditorAPI(self.text, self.status, win)

        # tabs
        create_home_tab(self.ribbon, self.api)
        create_insert_tab(self.ribbon, self.api)
        create_design_tab(self.ribbon, self.api)
        create_layout_tab(self.ribbon, self.api)
        create_references_tab(self.ribbon, self.api)

        # file menu
        menubar = tk.Menu(win)
        filem = tk.Menu(menubar, tearoff=0)
        filem.add_command(label="New", command=self.new_doc)
        filem.add_command(label="Open…", command=self.open_doc)
        filem.add_command(label="Save As…", command=self.save_doc)
        filem.add_separator(); filem.add_command(label="Exit", command=win.destroy)
        menubar.add_cascade(label="File", menu=filem)
        win.config(menu=menubar)

    # simple save/load to .pypad (pickle)
    def save_doc(self):
        p = filedialog.asksaveasfilename(defaultextension=".pypad", filetypes=[("PyWordPad","*.pypad")])
        if not p: return
        data = {
            "text": self.text.get("1.0","end"),
            "page_setup": self.api.page_setup,
            "theme": {"bg": self.text.cget("bg"), "fg": self.text.cget("fg")}
        }
        with open(p, "wb") as f: pickle.dump(data, f)
        self.status.config(text=f"Saved: {p}")

    def open_doc(self):
        p = filedialog.askopenfilename(filetypes=[("PyWordPad","*.pypad")])
        if not p: return
        with open(p, "rb") as f:
            data = pickle.load(f)
        self.text.delete("1.0","end")
        self.text.insert("1.0", data.get("text",""))
        th = data.get("theme")
        if th: self.text.config(bg=th["bg"], fg=th["fg"])
        self.api.page_setup = data.get("page_setup", self.api.page_setup)
        self.status.config(text=f"Opened: {p}")

    def new_doc(self):
        if tk.messagebox.askyesno("New", "Clear current document?"):
            self.text.delete("1.0","end")
            self.status.config(text="New document")
