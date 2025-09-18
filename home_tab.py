import tkinter as tk
from tkinter import ttk, font, colorchooser, simpledialog, messagebox

def _sel(text):
    try: return text.index("sel.first"), text.index("sel.last")
    except: return None, None

def create_home_tab(notebook, api):
    """
    api: object with attributes
      - text: tk.Text
      - insert_image_dialog(), insert_datetime()
    """
    text = api.text
    home = tk.Frame(notebook, padx=6, pady=6)
    notebook.add(home, text="Home")

    # --- Clipboard
    clip = tk.LabelFrame(home, text="Clipboard", padx=6, pady=6); clip.grid(row=0, column=0, sticky="w")
    tk.Button(clip, text="Cut", command=lambda: text.event_generate("<<Cut>>")).pack(side="left", padx=2)
    tk.Button(clip, text="Copy", command=lambda: text.event_generate("<<Copy>>")).pack(side="left", padx=2)
    tk.Button(clip, text="Paste", command=lambda: text.event_generate("<<Paste>>")).pack(side="left", padx=2)

    # --- Font
    fnt = tk.LabelFrame(home, text="Font", padx=6, pady=6); fnt.grid(row=0, column=1, sticky="w", padx=8)
    families = sorted(font.families())
    api.font_family = tk.StringVar(value="Segoe UI")
    api.font_size = tk.IntVar(value=12)

    ttk.Combobox(fnt, textvariable=api.font_family, values=families, width=18,
                 state="readonly").grid(row=0, column=0, padx=3)
    tk.Spinbox(fnt, from_=6, to=72, width=4, textvariable=api.font_size).grid(row=0, column=1)
    def apply_base_font(*_):
        base = font.Font(family=api.font_family.get(), size=int(api.font_size.get()))
        text.configure(font=base)
    api.font_family.trace_add("write", apply_base_font)
    api.font_size.trace_add("write", apply_base_font)

    def _tag_font(tagname, **kwargs):
        f = font.Font(text, text.cget("font"))
        for k,v in kwargs.items(): f[k] = v
        text.tag_configure(tagname, font=f)

    tk.Button(fnt, text="Bold", command=lambda: (_tag_font("bold", weight="bold"),
             text.tag_add("bold", *_sel(text)) if _sel(text)[0] else messagebox.showinfo("Select","Select text"))).grid(row=1, column=0, pady=2)
    tk.Button(fnt, text="Italic", command=lambda: (_tag_font("italic", slant="italic"),
             text.tag_add("italic", *_sel(text)) if _sel(text)[0] else messagebox.showinfo("Select","Select text"))).grid(row=1, column=1)
    tk.Button(fnt, text="Underline", command=lambda: (text.tag_configure("ul", underline=1),
             text.tag_add("ul", *_sel(text)) if _sel(text)[0] else messagebox.showinfo("Select","Select text"))).grid(row=1, column=2)
    tk.Button(fnt, text="Strike", command=lambda: (text.tag_configure("st", overstrike=1),
             text.tag_add("st", *_sel(text)) if _sel(text)[0] else messagebox.showinfo("Select","Select text"))).grid(row=1, column=3)

    tk.Button(fnt, text="Sup", command=lambda: (text.tag_configure("sup", offset=4),
             text.tag_add("sup", *_sel(text)) if _sel(text)[0] else messagebox.showinfo("Select","Select text"))).grid(row=2, column=0, pady=2)
    tk.Button(fnt, text="Sub", command=lambda: (text.tag_configure("sub", offset=-4),
             text.tag_add("sub", *_sel(text)) if _sel(text)[0] else messagebox.showinfo("Select","Select text"))).grid(row=2, column=1)

    def choose_fg():
        c = colorchooser.askcolor()[1]
        if not c: return
        tag = f"fg_{c.replace('#','')}"
        text.tag_configure(tag, foreground=c)
        s = _sel(text); 
        if s[0]: text.tag_add(tag, *s)
    def choose_bg():
        c = colorchooser.askcolor()[1]
        if not c: return
        tag = f"bg_{c.replace('#','')}"
        text.tag_configure(tag, background=c)
        s = _sel(text); 
        if s[0]: text.tag_add(tag, *s)

    tk.Button(fnt, text="Text Color", command=choose_fg).grid(row=2, column=2)
    tk.Button(fnt, text="Highlight", command=choose_bg).grid(row=2, column=3)

    # --- Paragraph
    par = tk.LabelFrame(home, text="Paragraph", padx=6, pady=6); par.grid(row=0, column=2, sticky="w")
    tk.Button(par, text="• Bullets", command=lambda: text.insert("insert linestart", "• ")).grid(row=0, column=0, padx=2)
    tk.Button(par, text="1. Number", command=lambda: text.insert("insert linestart", f"{int(text.index('insert').split('.')[0])}. ")).grid(row=0, column=1)
    def set_align(j):
        s, e = _sel(text)
        if not s: s, e = text.index("insert linestart"), text.index("insert lineend")
        tag = f"align_{j}"
        text.tag_configure(tag, justify=j)
        text.tag_add(tag, s, e)
    tk.Button(par, text="Left", command=lambda: set_align("left")).grid(row=1, column=0, pady=2)
    tk.Button(par, text="Center", command=lambda: set_align("center")).grid(row=1, column=1)
    tk.Button(par, text="Right", command=lambda: set_align("right")).grid(row=1, column=2)
    tk.Button(par, text="Justify", command=lambda: set_align("justify")).grid(row=1, column=3)

    def spacing():
        v = simpledialog.askinteger("Line spacing", "Enter extra spacing (pixels):", initialvalue=4, minvalue=0, maxvalue=40)
        if v is None: return
        text.tag_configure("pspace", spacing1=v, spacing3=v)
        s, e = _sel(text)
        (text.tag_add("pspace", s, e) if s else text.tag_add("pspace", "1.0", "end"))
    tk.Button(par, text="Line Spacing", command=spacing).grid(row=2, column=0, pady=2)

    tk.Button(par, text="Increase Indent", command=lambda: text.insert("insert linestart", "\t")).grid(row=2, column=1)
    def dec_indent():
        line = text.get("insert linestart", "insert linestart +1c")
        if line == "\t": text.delete("insert linestart", "insert linestart +1c")
    tk.Button(par, text="Decrease Indent", command=dec_indent).grid(row=2, column=2)

    # --- Insert (limited within Home)
    ins = tk.LabelFrame(home, text="Insert (quick)", padx=6, pady=6); ins.grid(row=0, column=3, sticky="w", padx=8)
    tk.Button(ins, text="Picture", command=api.insert_image_dialog).pack(side="left", padx=3)
    tk.Button(ins, text="Date/Time", command=api.insert_datetime).pack(side="left", padx=3)

    # --- Editing
    edt = tk.LabelFrame(home, text="Editing", padx=6, pady=6); edt.grid(row=0, column=4, sticky="w")
    def find_replace():
        dlg = tk.Toplevel(text); dlg.title("Find / Replace"); dlg.resizable(False, False)
        tk.Label(dlg, text="Find").grid(row=0, column=0); tk.Label(dlg, text="Replace").grid(row=1, column=0)
        sv = tk.StringVar(); rv = tk.StringVar()
        tk.Entry(dlg, textvariable=sv, width=24).grid(row=0, column=1, padx=4, pady=3)
        tk.Entry(dlg, textvariable=rv, width=24).grid(row=1, column=1, padx=4, pady=3)
        out = tk.Label(dlg, text=""); out.grid(row=2, column=0, columnspan=2)
        def do_find():
            s = sv.get()
            if not s: return
            start = "1.0"
            count = 0
            text.tag_remove("findhl", "1.0", "end")
            while True:
                pos = text.search(s, start, stopindex="end")
                if not pos: break
                last = f"{pos}+{len(s)}c"
                text.tag_add("findhl", pos, last)
                start = last; count += 1
            text.tag_configure("findhl", background="#fffd7a")
            out.config(text=f"Found {count} match(es)")
        def do_replace():
            s, r = sv.get(), rv.get()
            if not s: return
            cnt = 0; start = "1.0"
            while True:
                pos = text.search(s, start, stopindex="end")
                if not pos: break
                last = f"{pos}+{len(s)}c"
                text.delete(pos, last); text.insert(pos, r)
                start = f"{pos}+{len(r)}c"; cnt += 1
            out.config(text=f"Replaced {cnt} occurrence(s)")
        tk.Button(dlg, text="Find All", command=do_find).grid(row=3, column=0, pady=6)
        tk.Button(dlg, text="Replace All", command=do_replace).grid(row=3, column=1)
    tk.Button(edt, text="Find/Replace", command=find_replace).pack(side="left", padx=2)
    tk.Button(edt, text="Select All", command=lambda: text.tag_add("sel", "1.0", "end")).pack(side="left", padx=2)
