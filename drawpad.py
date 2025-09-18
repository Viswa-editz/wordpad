from tkinter import Toplevel, Frame, Button, Canvas, LEFT, TOP, BOTH, colorchooser
from PIL import Image, ImageDraw
from utils import save_pil

class DrawPad:
    def __init__(self, parent, on_save_path):
        self.on_save_path = on_save_path
        self.win = Toplevel(parent)
        self.win.title("Paint Drawing")
        self.win.geometry("800x600")

        bar = Frame(self.win); bar.pack(side=TOP, fill="x")
        Button(bar, text="Pen", command=lambda: self.set_tool("pen")).pack(side=LEFT)
        Button(bar, text="Eraser", command=lambda: self.set_tool("eraser")).pack(side=LEFT)
        Button(bar, text="Color", command=self.pick_color).pack(side=LEFT)
        Button(bar, text="Clear", command=lambda: self.canvas.delete("all")).pack(side=LEFT)
        Button(bar, text="Save & Insert", command=self.save_and_insert).pack(side=LEFT)
        Button(bar, text="Close", command=self.win.destroy).pack(side=LEFT)

        self.canvas = Canvas(self.win, bg="white"); self.canvas.pack(fill=BOTH, expand=True)
        self.tool, self.color, self.size = "pen", "#000000", 3
        self.strokes, self.current = [], []

        self.canvas.bind("<ButtonPress-1>", self.down)
        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind("<ButtonRelease-1>", self.up)

    def set_tool(self, t): self.tool = t
    def pick_color(self):
        c = colorchooser.askcolor()[1]
        if c: self.color = c

    def down(self, e): self.current = [(e.x, e.y)]
    def move(self, e):
        if not self.current: return
        x0, y0 = self.current[-1]
        if self.tool == "pen":
            self.canvas.create_line(x0, y0, e.x, e.y, width=self.size, capstyle='round', smooth=True, fill=self.color)
        else:
            s = max(4, self.size)
            self.canvas.create_oval(e.x-s, e.y-s, e.x+s, e.y+s, fill="white", outline="white")
        self.current.append((e.x, e.y))
    def up(self, e):
        if self.current:
            self.strokes.append({"tool": self.tool, "color": self.color, "w": self.size, "pts": list(self.current)})
            self.current = []

    def save_and_insert(self):
        w, h = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        img = Image.new("RGB", (w, h), "white")
        d = ImageDraw.Draw(img)
        for s in self.strokes:
            if len(s["pts"]) < 2: continue
            col = "white" if s["tool"] == "eraser" else s["color"]
            d.line(s["pts"], fill=col, width=s["w"] * (2 if s["tool"] == "eraser" else 1))
        path = save_pil(img, prefix="draw")
        if callable(self.on_save_path): self.on_save_path(path)
        self.win.destroy()
