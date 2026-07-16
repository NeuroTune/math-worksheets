#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:33:55 2022

@author: taksoy
"""



#Import the required libraries
from tkinter import *
#from PIL import ImageTK,Image


root=Tk()
root.title('Math Worksheets')
root.geometry("400x400")



options=["Select Math worksheet", "Addition", "Substraction", "Multiplication"]
clicked1=StringVar()
clicked1.set(options[0])
drop1=OptionMenu(root,clicked1,*options)
drop1.pack()
operation=clicked1.get()



options2=["How many digits?","1","2","3"]
clicked2=StringVar()
#clicked2.set(options2[0])
drop2=OptionMenu(root,clicked2,*options2)
drop2.pack()
digits=clicked2.get()

root.mainloop()




from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
 
from random import seed
from random import randint
seed()

#digits=1
#digits=2
#digits=3



#operation='addition'
#operation='substraction'
#operation='multiplication'


if digits=='1':
#one digit 
    m1=1
    m2=10
    dd= '/ One Digit'
    
if digits=="2":
#two digit
    m1=10
    m2=100
    dd= '/ Two Digits'
    
if digits =="3":
#three digit
    m1=100
    m2=1000
    dd= '/Three Digits'
    
if digits =="4":
#three digit
    m1=1000
    m2=10000
    dd= '/ Four Digits'
    

q1a=randint(m1,m2)
q1b=randint(m1,q1a)


q2a=randint(m1,m2)
q2b=randint(m1,q2a)

q3a=randint(m1,m2)
q3b=randint(m1,q3a)

q4a=randint(m1,m2)
q4b=randint(m1,q4a)

q5a=randint(m1,m2)
q5b=randint(m1,q5a)

q6a=randint(m1,m2)
q6b=randint(m1,q6a)

q7a=randint(m1,m2)
q7b=randint(m1,q7a)

q8a=randint(m1,m2)
q8b=randint(m1,q8a)

q9a=randint(m1,m2)
q9b=randint(m1,q9a)

q10a=randint(m1,m2)
q10b=randint(m1,q10a)

q11a=randint(m1,m2)
q11b=randint(m1,q11a)

q12a=randint(m1,m2)
q12b=randint(m1,q12a)

q13a=randint(m1,m2)
q13b=randint(m1,q13a)

q14a=randint(m1,m2)
q14b=randint(m1,q14a)

q15a=randint(m1,m2)
q15b=randint(m1,q15a)

q16a=randint(m1,m2)
q16b=randint(m1,q16a)

q17a=randint(m1,m2)
q17b=randint(m1,q17a)

q18a=randint(m1,m2)
q18b=randint(m1,q18a)


if operation=='Addition':
    sign='     +'
    title='Addition'
    Ans1=q1a+q1b
    Ans2=q2a+q2b
    Ans3=q3a+q3b
    Ans4=q4a+q4b
    Ans5=q5a+q5b
    Ans6=q6a+q6b
    Ans7=q7a+q7b
    Ans8=q8a+q8b
    Ans9=q9a+q9b
    Ans10=q10a+q10b
    Ans11=q11a+q11b
    Ans12=q12a+q12b
    Ans13=q13a+q13b
    Ans14=q14a+q14b
    Ans15=q15a+q15b
    Ans16=q16a+q16b
    Ans17=q17a+q17b
    Ans18=q18a+q18b
    
    
    
if operation=='substraction':
    sign='     -'
    title='Substraction'
    Ans1=q1a-q1b
    Ans2=q2a-q2b
    Ans3=q3a-q3b
    Ans4=q4a-q4b
    Ans5=q5a-q5b
    Ans6=q6a-q6b
    Ans7=q7a-q7b
    Ans8=q8a-q8b
    Ans9=q9a-q9b
    Ans10=q10a-q10b
    Ans11=q11a-q11b
    Ans12=q12a-q12b
    Ans13=q13a-q13b
    Ans14=q14a-q14b
    Ans15=q15a-q15b
    Ans16=q16a-q16b
    Ans17=q17a-q17b
    Ans18=q18a-q18b
    
    
if operation=='multiplication':
    sign='     x'
    title='Multiplication'
    Ans1=q1a*q1b
    Ans2=q2a*q2b
    Ans3=q3a*q3b
    Ans4=q4a*q4b
    Ans5=q5a*q5b
    Ans6=q6a*q6b
    Ans7=q7a*q7b
    Ans8=q8a*q8b
    Ans9=q9a*q9b
    Ans10=q10a*q10b
    Ans11=q11a*q11b
    Ans12=q12a*q12b
    Ans13=q13a*q13b
    Ans14=q14a*q14b
    Ans15=q15a*q15b
    Ans16=q16a*q16b
    Ans17=q17a*q17b
    Ans18=q18a*q18b
    
    





def form(path):
    my_canvas = canvas.Canvas(path, pagesize=letter)
    my_canvas.setFont('Helvetica-Bold', 16)
    
    x = my_canvas._pagesize[0] / 2
    my_canvas.drawCentredString(x, 740 , 'MATH WORKSHEETS')
    my_canvas.drawCentredString(x, 720, title + dd)
    


    my_canvas.setLineWidth(1)
    
#Title Line    
    my_canvas.line(100, 700, 500, 700)
   # my_canvas.drawString(10, 700, '700')

#Border dark lines
    my_canvas.line(10, 780, 10, 10)
    my_canvas.line(600, 780, 600, 10)
    my_canvas.line(10, 780, 600, 780) #up
   # my_canvas.drawString(10, 780, '780')
    my_canvas.line(10, 10, 600, 10)  #down
    #my_canvas.drawString(10, 10, '10')
    
#Border fine lines    
    my_canvas.setLineWidth(.3)
    my_canvas.line(13, 780, 13, 10) #left
    my_canvas.line(597, 780, 597, 10) #right
    my_canvas.line(10, 777, 600, 777) #up
    my_canvas.line(10, 13, 600, 13)  #down



#Questions

    my_canvas.setFont('Helvetica', 12)
    my_canvas.setLineWidth(0.5)


    my_canvas.drawString(30, 670, '1)'  )
    my_canvas.drawString(90, 670,  str(q1a)) 
    my_canvas.drawString(90, 650,  str(q1b)+sign)
    my_canvas.line(70, 645, 140, 645)  #down
    
    my_canvas.drawString(210, 670, '2)')
    my_canvas.drawString(270, 670,  str(q2a)) 
    my_canvas.drawString(270, 650,  str(q2b)+ sign)
    my_canvas.line(250, 645, 320, 645)  #down
        
    my_canvas.drawString(420, 670, '3)')
    my_canvas.drawString(480, 670,  str(q3a)) 
    my_canvas.drawString(480, 650,  str(q3b)+sign)
    my_canvas.line(460, 645, 530, 645)  #down
    
    
    
    my_canvas.drawString(30, 555, '4)')
    my_canvas.drawString(90, 555,  str(q4a)) 
    my_canvas.drawString(90, 535,  str(q4b)+ sign)
    my_canvas.line(70, 530, 140, 530)  #down
    
    my_canvas.drawString(210, 555, '5)')
    my_canvas.drawString(270, 555,  str(q5a)) 
    my_canvas.drawString(270, 535,  str(q5b)+ sign)
    my_canvas.line(250, 530, 320, 530)  #down
    
    my_canvas.drawString(420, 555, '6)')
    my_canvas.drawString(480, 555,  str(q6a)) 
    my_canvas.drawString(480, 535,  str(q6b)+sign)
    my_canvas.line(460, 530, 530, 530)  #down
    
    

    my_canvas.drawString(30, 440, '7)')
    my_canvas.drawString(90, 440,  str(q7a)) 
    my_canvas.drawString(90, 420,  str(q7b)+sign)
    my_canvas.line(70, 415, 140, 415)  #down
    
    my_canvas.drawString(210, 440, '8)')
    my_canvas.drawString(270, 440,  str(q8a)) 
    my_canvas.drawString(270, 420,  str(q8b)+ sign)
    my_canvas.line(250, 415, 320, 415)  #down
    
    my_canvas.drawString(420, 440, '9)')
    my_canvas.drawString(480, 440,  str(q9a)) 
    my_canvas.drawString(480, 420,  str(q9b)+ sign)
    my_canvas.line(460, 415, 530, 415)  #down
    
    

    my_canvas.drawString(30, 325, '10)')
    my_canvas.drawString(90, 325,  str(q10a)) 
    my_canvas.drawString(90, 305,  str(q10b)+ sign)
    my_canvas.line(70, 300, 140, 300)  #down
    
    my_canvas.drawString(210, 325, '11)')
    my_canvas.drawString(270, 325,  str(q11a)) 
    my_canvas.drawString(270, 305,  str(q11b)+ sign)
    my_canvas.line(250, 300, 320, 300)  #down
    
    my_canvas.drawString(420, 325, '12)')
    my_canvas.drawString(480, 325,  str(q12a)) 
    my_canvas.drawString(480, 305,  str(q12b)+ sign)
    my_canvas.line(460, 300, 530, 300)  #down



    my_canvas.drawString(30, 210, '13)')
    my_canvas.drawString(90, 210,  str(q13a)) 
    my_canvas.drawString(90, 190,  str(q13b)+ sign)
    my_canvas.line(70, 185, 140, 185)  #down
    
    my_canvas.drawString(210, 210, '14)')
    my_canvas.drawString(270, 210,  str(q14a)) 
    my_canvas.drawString(270, 190,  str(q14b)+ sign)
    my_canvas.line(250, 185, 320, 185)  #down
    
    my_canvas.drawString(420, 210, '15)')
    my_canvas.drawString(480, 210,  str(q15a)) 
    my_canvas.drawString(480, 190,  str(q15b)+sign)
    my_canvas.line(460, 185, 530, 185)  #down

    

    my_canvas.drawString(30, 95, '16)')
    my_canvas.drawString(90, 95,  str(q16a)) 
    my_canvas.drawString(90, 75,  str(q16b)+ sign)
    my_canvas.line(70, 70, 140, 70)  #down
    
    my_canvas.drawString(210, 95, '17)')
    my_canvas.drawString(270, 95,  str(q17a)) 
    my_canvas.drawString(270, 75,  str(q17b)+ sign)
    my_canvas.line(250, 70, 320, 70)  #down
    
    my_canvas.drawString(420, 95, '18)')
    my_canvas.drawString(480, 95,  str(q18a)) 
    my_canvas.drawString(480, 75,  str(q18b)+ sign)
    my_canvas.line(460, 70, 530, 70)  #down
    
    
    
#Horizantal Lines
    my_canvas.setFont('Helvetica', 12)
    my_canvas.setLineWidth(.3)
        

    my_canvas.line(10, 585, 600, 585)
    #my_canvas.drawString(10, 585, '585')

    my_canvas.line(10, 470, 600, 470)
    #my_canvas.drawString(10, 470, '470')


    my_canvas.line(10, 355, 600, 355)
    #my_canvas.drawString(10, 355, '355')

    
    my_canvas.line(10, 240, 600, 240)
   # my_canvas.drawString(10, 240, '240')

    my_canvas.line(10, 125, 600, 125)
    #my_canvas.drawString(10, 125, '125')


#Answer sheet
    my_canvas.setFont('Helvetica', 6)

    my_canvas.drawString(15,15, '1)'+ str(Ans1) +'    2)' +str(Ans2)+ '    3)'+ str(Ans3) + '    4'+str(Ans4)+'    5)'+str(Ans5)+'    6)'+str(Ans6)+
                        '    7)'+ str(Ans7) +'    8)' +str(Ans8)+ '    9)'+ str(Ans9) + '    10'+str(Ans10)+'    11)'+str(Ans11)+'    12)'+str(Ans12) +
                        '    13)'+ str(Ans13) +'    14)' +str(Ans14)+ '    15)'+ str(Ans15) + '    16'+str(Ans16)+'    17)'+str(Ans17)+'    18)'+str(Ans18))


    my_canvas.save()
if __name__ == '__main__':
    form('canvas_form.pdf')