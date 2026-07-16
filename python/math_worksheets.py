import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import math, os, time, platform, subprocess
from random import seed, randint, getrandbits, choice

seed()

# --- STYLING CONSTANTS ---
BG_COLOR = "#F5F7F8"      
ACCENT_COLOR = "#46E553"  
TEXT_COLOR = "#26218E"    
BTN_TEXT = "#9D20AB"      

def generate_worksheet():
    # 1. Pull data from GUI
    operation = clicked1.get()
    digits_str = clicked2.get()
    num_questions_str = clicked3.get()

    # 2. Validation - Check if user left placeholders selected
    if "Select" in operation or "digits" in digits_str or "questions" in num_questions_str:
        status_label.config(text="✖ Error: Please make all selections!", foreground="#EF4444")
        return

    questions = int(num_questions_str)
    questionsA, questionsB, answers, equations = [], [], [], []
    
    # Structure/Layout logic
    if questions > 12: structure = 3
    elif questions > 6: structure = 2
    else: structure = 1
    col = math.ceil(questions / structure)

    title = operation
    dd = f"/ {digits_str} Digits" if digits_str.isdigit() else ""
    sign = ""

    # 3. Math Logic
    for i in range(questions):
        if operation in ['Addition', 'Subtraction', 'Multiplication', 'Division']:
            d = int(digits_str)
            a = randint(10**(d-1), (10**d)-1)
            b = randint(10**(d-1), (10**d)-1)
            
            if operation == 'Addition':
                sign = '+'; answers.append(f"{i+1}) {a + b}")
            elif operation == 'Subtraction':
                sign = '-'; 
                if a < b: a, b = b, a  # Keep answers positive
                answers.append(f"{i+1}) {a - b}")
            elif operation == 'Multiplication':
                sign = 'x'; answers.append(f"{i+1}) {a * b}")
            elif operation == 'Division':
                b_div = randint(1, 10 if d <= 2 else 50)
                questionsA.append(a); questionsB.append(b_div)
                answers.append(f"{i+1}) {a // b_div} R: {a % b_div}")
                continue # Skip the general append below
            
            questionsA.append(a); questionsB.append(b)

        elif operation == 'Algebra':
            x1Val = choice([-5, -4, -3, -2, -1, 1, 2, 4, 5])
            num1Val = randint(1, 21)
            num1Pos = bool(getrandbits(1))
            resVal = randint(20, 100)
            
            eq = f"{x1Val}x {'+' if num1Pos else '-'} {num1Val} = {resVal}"
            equations.append(eq)
            
            # Algebra Solver: (resVal - num1Val) / x1Val
            true_num1 = num1Val if num1Pos else -num1Val
            sol = round((resVal - true_num1) / x1Val, 2)
            answers.append(f"{i+1}) x = {sol}")

    # 4. Create PDF
    timestamp = time.strftime("%H%M%S")
    path = f"Worksheet_{timestamp}.pdf"
    
    try:
        my_canvas = canvas.Canvas(path, pagesize=letter)
        my_canvas.setFont('Helvetica-Bold', 18)
        mid_x = letter[0] / 2
        
        my_canvas.drawCentredString(mid_x, 750, 'MATH WORKSHEETS')
        my_canvas.setFont('Helvetica', 14)
        my_canvas.drawCentredString(mid_x, 730, f"{title}{dd}")
        my_canvas.line(100, 715, 500, 715)

        my_canvas.setFont('Helvetica', 14)
        for i in range(questions):
            x = 50 + (i % structure) * (500 / structure)
            y = 650 - (i // structure) * 85
            
            my_canvas.drawString(x, y, f"{i+1})")
            if operation == 'Algebra':
                my_canvas.drawString(x + 30, y, equations[i])
            elif operation == 'Division':
                my_canvas.drawString(x + 30, y, f"{questionsB[i]} | {questionsA[i]}")
            else:
                my_canvas.drawRightString(x + 100, y, str(questionsA[i]))
                my_canvas.drawRightString(x + 100, y - 20, f"{sign} {questionsB[i]}")
                my_canvas.line(x + 50, y - 25, x + 110, y - 25)

        # Answer Page
        my_canvas.showPage()
        my_canvas.setFont('Helvetica-Bold', 16)
        my_canvas.drawCentredString(mid_x, 750, "Answer Key")
        my_canvas.setFont('Helvetica', 12)
        for idx, ans in enumerate(answers):
            my_canvas.drawString(70, 710 - (idx * 25), ans)

        my_canvas.save()
        
        # 5. Universal Popup Logic
        if platform.system() == 'Darwin':       # Mac
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(path)
        else:                                   # Linux
            subprocess.call(('xdg-open', path))

        status_label.config(text=f"✔ Created: {path}", foreground="#10B981")
        
    except Exception as e:
        status_label.config(text=f"✖ Error: {str(e)}", foreground="#EF4444")

# --- UI WINDOW SETUP ---
root = tk.Tk()
root.title('Math Worksheet Pro')
root.geometry("460x600")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use('clam')

main_frame = tk.Frame(root, bg=BG_COLOR, padx=40, pady=40)
main_frame.pack(expand=True, fill="both")

tk.Label(main_frame, text="Worksheet Generator", bg=BG_COLOR, 
         fg=TEXT_COLOR, font=("Arial", 22, "bold")).pack(pady=(0, 10))

tk.Label(main_frame, text="Configure your math practice below", 
         bg=BG_COLOR, fg="#6B7280", font=("Arial", 10)).pack(pady=(0, 30))

# --- DROPDOWNS ---
def create_menu(label_text, var, options):
    tk.Label(main_frame, text=label_text, bg=BG_COLOR, fg="#4B5563", 
             font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
    menu = ttk.OptionMenu(main_frame, var, var.get(), *options)
    menu.pack(fill="x", ipady=8, pady=(0, 10))

clicked1 = tk.StringVar(value="Select Math worksheet")
create_menu("Select Operation", clicked1, ["Addition", "Subtraction", "Multiplication", "Division", "Algebra"])

clicked2 = tk.StringVar(value="How many digits?")
create_menu("Difficulty (Digits)", clicked2, ["1", "2", "3", "4", "N/A"])

clicked3 = tk.StringVar(value="How many questions?")
create_menu("Quantity", clicked3, [str(i) for i in range(1, 19)])

# --- ACTION BUTTON ---
gen_btn = tk.Button(main_frame, text="Generate PDF", command=generate_worksheet,
                    bg=ACCENT_COLOR, fg=BTN_TEXT, font=("Arial", 13, "bold"),
                    activebackground="#4338CA", activeforeground="white",
                    cursor="hand2", bd=0, relief="flat", padx=20, pady=12)
gen_btn.pack(fill="x", pady=(30, 10))

status_label = ttk.Label(main_frame, text="Ready to create your next worksheet", 
                         font=("Arial", 9), foreground="#9CA3AF")
status_label.pack(pady=10)

root.mainloop()