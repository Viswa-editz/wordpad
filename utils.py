import os, datetime
from tkinter import simpledialog, messagebox
from PIL import Image

APP_TITLE = "PyWordPad"
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

def center_window(win, w=1100, h=750):
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - w) // 2, (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

def save_pil(img: Image.Image, prefix="img") -> str:
    name = f"{prefix}_{int(datetime.datetime.now().timestamp())}.png"
    path = os.path.join(MEDIA_DIR, name)
    img.save(path)
    return path

def ask_number(title, prompt, initial=1, minv=1, maxv=100):
    try:
        v = simpledialog.askinteger(title, prompt, initialvalue=initial, minvalue=minv, maxvalue=maxv)
        return v
    except Exception:
        messagebox.showerror("Error", "Invalid number.")
        return None
