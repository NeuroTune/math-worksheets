#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:33:55 2022

@author: taksoy
"""

# Import the required libraries
import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import math
from random import seed
from random import randint
from random import getrandbits
from random import choice

seed()

# Build the GUI interface
root = tk.Tk()
root.title('Math Worksheets')
root.geometry("400x400")

def getOperation(operationP): # Function to pick the operation
    global operation
    operation = clicked1.get()
    
def getDigits(digitsP): # Function to pick the number of digits
    global digits
    digits = clicked2.get()

def getQuestions(numbersP): # Function to pick the number of questions
    global questions
    questions = clicked3.get()


#Make make the dropdown MENU for each section
options = ["Select Math worksheet", "Addition", "Subtraction", "Multiplication", "Division", "Algebra"]
clicked1 = tk.StringVar()
clicked1.set(options[0])
drop1 = tk.OptionMenu(root, clicked1, *options, command = getOperation)
drop1.pack()

options2 = ["How many digits?","1","2","3", "N/A (Algebra)"]
clicked2 = tk.StringVar()
clicked2.set(options2[0])
drop2 = tk.OptionMenu(root, clicked2, *options2, command = getDigits)
drop2.pack()

options3 = ["How many questions?","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]
clicked3 = tk.StringVar()
clicked3.set(options3[0])
drop3 = tk.OptionMenu(root, clicked3, *options3, command = getQuestions)
drop3.pack()
root.mainloop()


# Function to execute the PDF generation
def generate_pdf():
    # Retrieve the current selections
    selected_op = clicked1.get()
    selected_digits = clicked2.get()
    selected_num = clicked3.get()
    
    # Simple validation check
    if "Select" in selected_op or "How many" in selected_digits:
        print("Please make all selections before generating.")
        return

    # Convert the number of questions to an integer for calculations
    num_questions = int(selected_num)
    
    print(f"Generating {num_questions} problems for {selected_op}...")
    # This is where your ReportLab 'canvas' code will go!

# Add the Generate Button to the GUI
gen_button = tk.Button(root, text="Generate PDF", command=generate_pdf, bg="green", fg="white")
gen_button.pack(pady=20)



# Define lists and variables
questionsA = []
questionsB = []
questionsAlg = []
equations = []
answers = []
questions = int(questions)

# Pick structures depending on the number of questions
if 12 < questions <= 18: structure = 3
elif 6 < questions <= 12: structure = 2
else: structure = 1
col = math.ceil(questions/structure)

# Name the title depending on the digits chosen
if digits=='1':
    dd= '/ One Digit'
if digits=="2":
    dd= '/ Two Digits'  
if digits =="3":
    dd= '/Three Digits' 
if digits =="4":
    dd= '/ Four Digits'

# Pick random numbers depending on the number of digits
if operation == 'Addition' or operation == 'Substraction' or operation == 'Multiplication':
    for i in range(questions):
        questionsA.append(randint(math.pow(10, int(digits) - 1), math.pow(10, int(digits))))
        questionsB.append(randint(math.pow(10, int(digits) - 1), math.pow(10, int(digits))))

if operation == 'Division':
    for i in range(questions):
        questionsA.append(randint(math.pow(10, int(digits) - 1), math.pow(10, int(digits))))
        if int(digits) == 1:
            questionsB.append(randint(1, 10))
        elif int(digits) == 2:
            questionsB.append(randint(1, 10))
        else:
            questionsB.append(randint(1, 50))


### Algebra ###
if operation == 'Algebra':
    title = "Algebra"
    dd = ""
    for i in range(questions):
        equation = ""
        
        # Get random values for x's and constants and make equations
        x1 = True
        x1Val = choice([-5, -4, -3, -2, -1, 1, 2, 4, 5])

        num1 = bool(getrandbits(1))
        if num1:
            num1ValPos = bool(getrandbits(1))
            num1Val = randint(1, 21)

        x2 = bool(getrandbits(1))
        if x2:
            x2Val = choice([-5, -4, -3, -2, -1, 1, 2, 4, 5])

        num2 = True
        num2ValPos = bool(getrandbits(1))
        num2Val = randint(1, 21)

        equation += str(x1Val) + "x "
        if num1: 
            if num1ValPos:
                equation += "+ " 
                equation += str(num1Val) + " "
            else:
                equation += "- " 
                equation += str(num1Val) + " "
        equation += "= "
        if x2: equation += str(x2Val) + "x "
        if num2ValPos:
            equation += "+ " 
            equation += str(num2Val) + " "
        else:
            equation += "- " 
            equation += str(num2Val) + " "
        
        # Store Equations in the questions
        questionsAlg.append(equation)
        equations.append(equation)
        
        ## SOLVE Algebra ###
        if num2ValPos: 
            num2TrueVal = num2Val 
        else: 
            num2TrueVal = num2Val * - 1

        if x2:
            x1Val += x2Val * - 1
        if num1:
            if num1ValPos:
                num2TrueVal -= num1Val
            else:
                num2TrueVal += num1Val
                
        # Store Answers
        if x1Val != 0:
            answer = num2TrueVal / x1Val
            answers.append(str(i + 1) + ") " + str(round(answer, 2)))
        elif x1Val == 0 and num2TrueVal == 0:
            answer = 'All Real Numbers'
            answers.append(str(i + 1) + ") " + answer)
        elif x1Val == 0:
            answer = 'NA'
            answers.append(str(i + 1) + ") " + answer)


### Set the sign and the title -- STORE ANSWERS 
if operation=='Addition':
    sign='+'
    title='Addition'
    for i in range(questions):
        answers.append(str(i + 1) + ") " + str(int(questionsA[i] + questionsB[i])))

if operation=='Substraction':
    sign='-'
    title='Substraction'
    for i in range(questions):
        if questionsA[i] < questionsB[i]:
            filler = questionsA[i]
            questionsA[i] = questionsB[i]
            questionsB[i] = filler
        answers.append(str(i + 1) + ") " + str(int(questionsA[i] - questionsB[i])))
        
if operation=='Multiplication':
    sign='x'
    title='Multiplication'
    for i in range(questions):
        answers.append(str(i + 1) + ") " + str(int(questionsA[i] * questionsB[i])))

if operation == 'Division':
    title = 'Division'
    for i in range(questions):
        answers.append(str(i + 1) + ") " + str(int(questionsA[i] / questionsB[i])) + "; R: " + str(questionsA[i] % questionsB[i]))



### MAKE PDF ###
def form(path):
    # Set Page Size and Path
    my_canvas = canvas.Canvas(path, pagesize=letter)
    my_canvas.setFont('Helvetica-Bold', 16)
    
    x = my_canvas._pagesize[0] / 2
    my_canvas.drawCentredString(x, 740 , 'MATH WORKSHEETS')
    my_canvas.drawCentredString(x, 720, title + dd)
    


    my_canvas.setLineWidth(1)
    
    #Title Line    
    my_canvas.line(100, 700, 500, 700)

    #Border dark lines
    my_canvas.line(10, 780, 10, 10)
    my_canvas.line(600, 780, 600, 10)
    my_canvas.line(10, 780, 600, 780)
    my_canvas.line(10, 10, 600, 10)
    
    #Border fine lines    
    my_canvas.setLineWidth(.3)
    my_canvas.line(13, 780, 13, 10) #left
    my_canvas.line(597, 780, 597, 10) #right
    my_canvas.line(10, 777, 600, 777) #up
    my_canvas.line(10, 13, 600, 13)  #down

    #Questions
    my_canvas.setFont('Helvetica', 16)
    my_canvas.setLineWidth(0.5)
    
    for i in range(questions):
        ## Make Adaptable Format for questions
        if structure == 1:
            div = 1
            xInd = 0
        elif structure == 2:
            div = 2
            xInd = 270
        else: 
            div = 3
            xInd = 180
        
        if i % div == 0:
            x = 30
        elif i % div == 1:
            x = 30 + xInd * 1
        else: x = 30 + xInd * 2
        
        if i % div == 0: y = 670 - ((i * (670 / col) / div))
        
        ## Draw Questions and Numbers
        if operation != 'Division' and operation != 'Algebra':
            my_canvas.drawString(x, y, str(i + 1) + ')'  )
            my_canvas.drawRightString(x + 98, y, str(questionsA[i]))
            my_canvas.drawRightString(x + 98, y - 20, str(questionsB[i]))
            my_canvas.drawRightString(x + 108, y - 20, sign)
            my_canvas.line(x + 40, y - 25, x + 110, y - 25)  #down
        elif operation == 'Division':
            my_canvas.drawString(x, y, str(i + 1) + ')'  )
            my_canvas.drawRightString(x + 60, y - 5, str(questionsB[i]))
            my_canvas.drawString(x + 70, y - 5 , str(questionsA[i]))
            my_canvas.line(x + 65, y + 12, x + 110, y + 12)
            my_canvas.line(x + 65, y + 12, x + 65, y - 10)
        else:
            my_canvas.drawString(x, y, str(i + 1) + ')'  )
            my_canvas.drawString(x + 30, y, equations[i])

    ### Answer sheet
    #new page    
    my_canvas.showPage()    
    my_canvas.setFont('Helvetica', 10)
    # Draw Answer Strings
    for i in range(questions):
        my_canvas.drawString(10, 770 - i * 44, str(answers[i]))


    my_canvas.save()
#Finish PDF
if __name__ == '__main__':
    form('Math_Practice.pdf')