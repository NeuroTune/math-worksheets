#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import math
import os
import sys
import tempfile
import subprocess
from random import seed, randint, getrandbits, choice

seed()

# ── Helpers ───────────────────────────────────────────────────────────────────

def rand_range(d):
    lo = int(10 ** (int(d) - 1))
    hi = int(10 ** int(d))
    return randint(lo, hi)

def open_pdf(path):
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])

def generate_pdf(operation, digits, questions):
    questions = int(questions)
    questionsA, questionsB, equations, answers = [], [], [], []

    if 12 < questions <= 18:   structure = 3
    elif 6 < questions <= 12:  structure = 2
    else:                       structure = 1
    col = math.ceil(questions / structure)

    digit_labels = {"1": "/ One Digit", "2": "/ Two Digits", "3": "/ Three Digits", "4": "/ Four Digits"}
    dd   = digit_labels.get(str(digits), "")
    sign = ""

    if operation in ('Addition', 'Substraction', 'Multiplication'):
        for _ in range(questions):
            questionsA.append(rand_range(digits))
            questionsB.append(rand_range(digits))

    if operation == 'Division':
        for _ in range(questions):
            questionsA.append(rand_range(digits))
            divisor_max = 10 if int(digits) <= 2 else 50
            questionsB.append(randint(1, divisor_max))

    if operation == 'Algebra':
        title, dd = "Algebra", ""
        for i in range(questions):
            equation = ""
            x1Val   = choice([-5,-4,-3,-2,-1,1,2,4,5])
            has_num1 = bool(getrandbits(1))
            num1Val  = randint(1, 21) if has_num1 else 0
            num1Pos  = bool(getrandbits(1)) if has_num1 else True
            has_x2   = bool(getrandbits(1))
            x2Val    = choice([-5,-4,-3,-2,-1,1,2,4,5]) if has_x2 else 0
            num2Val  = randint(1, 21)
            num2Pos  = bool(getrandbits(1))

            equation += f"{x1Val}x "
            if has_num1:
                equation += ("+ " if num1Pos else "- ") + f"{num1Val} "
            equation += "= "
            if has_x2:
                equation += f"{x2Val}x "
            equation += ("+ " if num2Pos else "- ") + f"{num2Val} "
            equations.append(equation)

            num2True  = num2Val if num2Pos else -num2Val
            lhs_x     = x1Val - (x2Val if has_x2 else 0)
            rhs_const = num2True - (num1Val if (has_num1 and num1Pos) else (-num1Val if has_num1 else 0))
            if lhs_x != 0:
                answers.append(f"{i+1}) {round(rhs_const / lhs_x, 2)}")
            elif rhs_const == 0:
                answers.append(f"{i+1}) All Real Numbers")
            else:
                answers.append(f"{i+1}) No Solution")

    if operation == 'Addition':
        sign, title = '+', 'Addition'
        for i in range(questions):
            answers.append(f"{i+1}) {int(questionsA[i] + questionsB[i])}")

    if operation == 'Substraction':
        sign, title = '-', 'Subtraction'
        for i in range(questions):
            if questionsA[i] < questionsB[i]:
                questionsA[i], questionsB[i] = questionsB[i], questionsA[i]
            answers.append(f"{i+1}) {int(questionsA[i] - questionsB[i])}")

    if operation == 'Multiplication':
        sign, title = 'x', 'Multiplication'
        for i in range(questions):
            answers.append(f"{i+1}) {int(questionsA[i] * questionsB[i])}")

    if operation == 'Division':
        title = 'Division'
        for i in range(questions):
            answers.append(f"{i+1}) {int(questionsA[i] / questionsB[i])}; R: {questionsA[i] % questionsB[i]}")

    # ── Draw PDF ──
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False, prefix='Math_Worksheet_') as tmp:
        tmp_path = tmp.name

    c = canvas.Canvas(tmp_path, pagesize=letter)
    c.setFont('Helvetica-Bold', 16)
    cx = c._pagesize[0] / 2
    c.drawCentredString(cx, 740, 'MATH WORKSHEETS')
    c.drawCentredString(cx, 720, f"{title} {dd}")

    c.setLineWidth(1)
    c.line(100, 700, 500, 700)
    for x0,y0,x1,y1 in [(10,780,10,10),(600,780,600,10),(10,780,600,780),(10,10,600,10)]:
        c.line(x0,y0,x1,y1)
    c.setLineWidth(.3)
    for x0,y0,x1,y1 in [(13,780,13,10),(597,780,597,10),(10,777,600,777),(10,13,600,13)]:
        c.line(x0,y0,x1,y1)

    c.setFont('Helvetica', 16)
    c.setLineWidth(0.5)
    xInd = {1:0, 2:270, 3:180}[structure]
    y = 670

    for i in range(questions):
        div     = structure
        col_idx = i % div
        if col_idx == 0:
            x = 30
            y = 670 - ((i // div) * (670 / col))
        else:
            x = 30 + xInd * col_idx

        if operation not in ('Division','Algebra'):
            c.drawString(x, y, f"{i+1})")
            c.drawRightString(x+98, y,    str(questionsA[i]))
            c.drawRightString(x+98, y-20, str(questionsB[i]))
            c.drawRightString(x+108,y-20, sign)
            c.line(x+40, y-25, x+110, y-25)
        elif operation == 'Division':
            c.drawString(x, y, f"{i+1})")
            c.drawRightString(x+60, y-5, str(questionsB[i]))
            c.drawString(x+70,  y-5,     str(questionsA[i]))
            c.line(x+65, y+12, x+110, y+12)
            c.line(x+65, y+12, x+65,  y-10)
        else:
            c.drawString(x, y, f"{i+1})")
            c.drawString(x+30, y, equations[i])

    c.showPage()
    c.setFont('Helvetica', 10)
    for i in range(questions):
        c.drawString(10, 770 - i*44, answers[i])

    c.save()
    open_pdf(tmp_path)


# ── Custom Dropdown (works on macOS where OptionMenu ignores colors) ──────────

class CustomDropdown(tk.Frame):
    """A fully custom dropdown that respects colors on all platforms."""

    BG      = "#1e1e2e"
    CARD    = "#2a2a3d"
    HOVER   = "#33334d"
    ACCENT  = "#7c6af7"
    TEXT    = "#e0e0f0"
    SUBTEXT = "#9090b0"
    BORDER  = "#4a4a6a"

    def __init__(self, parent, options, placeholder="Select…", **kwargs):
        super().__init__(parent, bg=self.CARD, **kwargs)
        self._choices     = options
        self._placeholder = placeholder
        self._selected    = tk.StringVar(value=placeholder)
        self._popup       = None

        # The visible "button" row
        self._row = tk.Frame(self, bg=self.CARD,
                             highlightbackground=self.BORDER,
                             highlightthickness=1)
        self._row.pack(fill="x")

        self._lbl = tk.Label(self._row, textvariable=self._selected,
                             bg=self.CARD, fg=self.SUBTEXT,
                             font=("Helvetica", 12), anchor="w",
                             padx=10, pady=8)
        self._lbl.pack(side="left", fill="x", expand=True)

        tk.Label(self._row, text="▾", bg=self.CARD, fg=self.SUBTEXT,
                 font=("Helvetica", 12), padx=8).pack(side="right")

        self._row.bind("<Button-1>", self._toggle)
        self._lbl.bind("<Button-1>", self._toggle)
        for child in self._row.winfo_children():
            child.bind("<Button-1>", self._toggle)

    def get(self):
        return self._selected.get()

    def _toggle(self, event=None):
        if self._popup and self._popup.winfo_exists():
            self._popup.destroy()
            self._popup = None
            return
        self._open_popup()

    def _open_popup(self):
        self.update_idletasks()
        x = self._row.winfo_rootx()
        y = self._row.winfo_rooty() + self._row.winfo_height()
        w = self._row.winfo_width()

        pop = tk.Toplevel(self)
        pop.wm_overrideredirect(True)
        item_h = 36
        max_visible = 18
        popup_h = min(len(self._choices) * item_h, max_visible * item_h)
        pop.geometry(f"{w}x{popup_h}+{x}+{y}")
        pop.configure(bg=self.BORDER)
        self._popup = pop

        canvas_ = tk.Canvas(pop, bg=self.CARD, highlightthickness=0)
        scrollbar = tk.Scrollbar(pop, orient="vertical", command=canvas_.yview)
        canvas_.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(canvas_, bg=self.CARD)
        canvas_.create_window((0, 0), window=frame, anchor="nw")

        for opt in self._choices:
            row = tk.Frame(frame, bg=self.CARD, cursor="hand2")
            row.pack(fill="x")
            lbl = tk.Label(row, text=opt, bg=self.CARD, fg=self.TEXT,
                           font=("Helvetica", 12), anchor="w",
                           padx=12, pady=6)
            lbl.pack(fill="x")

            def _select(o=opt, p=pop):
                self._selected.set(o)
                self._lbl.config(fg=self.TEXT)
                p.destroy()
                self._popup = None

            def _enter(e, r=row, l=lbl):
                r.config(bg=self.HOVER); l.config(bg=self.HOVER)
            def _leave(e, r=row, l=lbl):
                r.config(bg=self.CARD); l.config(bg=self.CARD)

            row.bind("<Button-1>", lambda e, s=_select: s())
            lbl.bind("<Button-1>", lambda e, s=_select: s())
            row.bind("<Enter>", _enter); row.bind("<Leave>", _leave)
            lbl.bind("<Enter>", _enter); lbl.bind("<Leave>", _leave)

        frame.update_idletasks()
        canvas_.config(scrollregion=canvas_.bbox("all"))

        if len(self._choices) > max_visible:
            scrollbar.pack(side="right", fill="y")
        canvas_.pack(side="left", fill="both", expand=True)

        # Close if clicked outside
        pop.bind("<FocusOut>", lambda e: pop.destroy() if pop.winfo_exists() else None)
        pop.focus_set()


# ── Main App ──────────────────────────────────────────────────────────────────

class App(tk.Tk):
    BG      = "#1e1e2e"
    CARD    = "#2a2a3d"
    ACCENT  = "#7c6af7"
    TEXT    = "#e0e0f0"
    SUBTEXT = "#9090b0"
    SUCCESS = "#4ade80"
    ERROR   = "#f87171"

    def __init__(self):
        super().__init__()
        self.title("Math Worksheets")
        self.geometry("440x530")
        self.resizable(False, False)
        self.configure(bg=self.BG)
        self._generated = 0
        self._build_ui()

    def _build_ui(self):
        # ── Header ──
        tk.Label(self, text="📐  Math Worksheets",
                 bg=self.BG, fg=self.TEXT,
                 font=("Helvetica", 22, "bold")).pack(pady=(30, 4))
        tk.Label(self, text="Generate printable PDF practice sheets",
                 bg=self.BG, fg=self.SUBTEXT,
                 font=("Helvetica", 11)).pack(pady=(0, 20))

        # ── Card ──
        card = tk.Frame(self, bg=self.CARD, padx=30, pady=24)
        card.pack(padx=30, fill="x")

        lbl_style = {"bg": self.CARD, "fg": self.SUBTEXT,
                     "font": ("Helvetica", 9, "bold"), "anchor": "w"}

        # Operation
        tk.Label(card, text="OPERATION", **lbl_style).pack(fill="x", pady=(0, 4))
        self.op_dd = CustomDropdown(card,
            ["Addition","Subtraction","Multiplication","Division","Algebra"],
            placeholder="Select operation")
        self.op_dd.pack(fill="x", pady=(0, 14))

        # Digits
        tk.Label(card, text="NUMBER OF DIGITS", **lbl_style).pack(fill="x", pady=(0, 4))
        self.dig_dd = CustomDropdown(card, ["1","2","3","N/A (Algebra)"],
                                     placeholder="Select digits")
        self.dig_dd.pack(fill="x", pady=(0, 14))

        # Questions
        tk.Label(card, text="NUMBER OF QUESTIONS", **lbl_style).pack(fill="x", pady=(0, 4))
        self.q_dd = CustomDropdown(card, [str(i) for i in range(1, 19)],
                                   placeholder="Select questions")
        self.q_dd.pack(fill="x")

        # ── Status ──
        self.status_var = tk.StringVar()
        tk.Label(self, textvariable=self.status_var,
                 bg=self.BG, fg=self.ERROR,
                 font=("Helvetica", 11)).pack(pady=(12, 0))

        # ── Generate button ──
        self.btn = tk.Button(
            self,
            text="⚡  Generate Worksheet",
            command=self._on_generate,
            bg="#5c4ef0",       # solid deep purple — won't be overridden
            fg="#ffffff",
            activebackground="#4a3ed0",
            activeforeground="#ffffff",
            font=("Helvetica", 14, "bold"),
            relief="flat", bd=0,
            padx=20, pady=12,
            cursor="hand2",
        )
        self.btn.pack(pady=(8, 6), padx=30, fill="x")

        # ── Counter ──
        self.count_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.count_var,
                 bg=self.BG, fg=self.SUCCESS,
                 font=("Helvetica", 11)).pack()

    def _on_generate(self):
        operation = self.op_dd.get()
        digits    = self.dig_dd.get()
        questions = self.q_dd.get()

        if operation == "Select operation":
            self.status_var.set("⚠  Please select an operation.")
            return
        if operation != "Algebra" and digits in ("Select digits", "N/A (Algebra)"):
            self.status_var.set("⚠  Please select number of digits.")
            return
        if questions == "Select questions":
            self.status_var.set("⚠  Please select number of questions.")
            return

        op_key  = "Substraction" if operation == "Subtraction" else operation
        dig_key = "1" if digits == "N/A (Algebra)" else digits

        self.status_var.set("")
        self.btn.config(text="Generating…", state="disabled")
        self.update()

        try:
            generate_pdf(op_key, dig_key, questions)
            self._generated += 1
            plural = "s" if self._generated > 1 else ""
            self.count_var.set(f"✓  {self._generated} worksheet{plural} generated this session")
        except Exception as e:
            self.status_var.set(f"Error: {e}")
        finally:
            self.btn.config(text="⚡  Generate Worksheet", state="normal")


if __name__ == "__main__":
    App().mainloop()