import tkinter as tk
from tkinter import simpledialog, messagebox

def create_references_tab(notebook, api):
    text = api.text
    tab = tk.Frame(notebook, padx=6, pady=6)
    notebook.add(tab, text="References")

    # Headings (for TOC) – quick style buttons
    tk.Button(tab, text="H1", command=lambda: _apply_heading(text, "h1", 18)).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(tab, text="H2", command=lambda: _apply_heading(text, "h2", 14)).grid(row=0, column=1)

    # Footnote
    def footnote():
        note = simpledialog.askstring("Footnote", "Enter footnote:")
        if not note: return
        if "[Footnotes]" not in text.get("1.0","end"):
            text.insert("end","\n[Footnotes]\n")
        # count
        content = text.get("1.0","end")
        n = len([l for l in content.split("[Footnotes]")[-1].splitlines() if l.strip()]) + 1
        text.insert("insert", f"[{n}]")
        text.insert("end", f"[{n}] {note}\n")
    tk.Button(tab, text="Insert Footnote", command=footnote).grid(row=0, column=2, padx=6)

    # Citation + Bibliography
    def citation():
        c = simpledialog.askstring("Citation", "Enter citation text:")
        if not c: return
        api.bibliography.append(c)
        text.insert("insert", f"(cite {len(api.bibliography)})")
    tk.Button(tab, text="Add Citation", command=citation).grid(row=1, column=0, pady=6)

    def show_bib():
        if not api.bibliography:
            messagebox.showinfo("Bibliography", "No citations yet."); return
        text.insert("end","\nBibliography\n")
        for i, it in enumerate(api.bibliography, 1):
            text.insert("end", f"{i}. {it}\n")
    tk.Button(tab, text="Insert Bibliography", command=show_bib).grid(row=1, column=1)

    # Caption
    def caption():
        cap = simpledialog.askstring("Caption", "Enter caption:")
        if cap: text.insert("insert", f"\n[Caption] {cap}\n")
    tk.Button(tab, text="Caption", command=caption).grid(row=1, column=2)

    # TOC
    def toc():
        heads = []
        for tag in ("heading1","heading2"):
            ranges = text.tag_ranges(tag)
            for i in range(0, len(ranges), 2):
                start = ranges[i]
                line = text.get(start, f"{start} lineend").strip()
                heads.append((tag, line))
        if not heads:
            messagebox.showinfo("TOC","No headings found."); return
        out = "Table of Contents\n"
        for tag, line in heads:
            out += ("- " if tag=="heading1" else "  - ") + line + "\n"
        text.insert("1.0", out + "\n")
    tk.Button(tab, text="Generate TOC", command=toc).grid(row=2, column=0, pady=8)

def _apply_heading(text, tag, size):
    from tkinter import font
    f = font.Font(text, text.cget("font")); f.configure(size=size, weight="bold")
    text.tag_configure({"h1":"heading1","h2":"heading2"}[tag], font=f)
    try:
        s, e = text.index("sel.first"), text.index("sel.last")
        text.tag_add({"h1":"heading1","h2":"heading2"}[tag], s, e)
    except:
        pass
