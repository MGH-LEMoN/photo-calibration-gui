#Import tkinter library
import tkinter as tk
from tkinter import *
from tkinter import ttk

#Create an instance of Tkinter frame or window
win = Tk()
#Set the geometry of tkinter frame
# win.geometry("750x250")
# #Create a text widget and wrap by words
# text= Text(win,wrap=WORD)
# text.insert(INSERT,"Welcome to the Calibration GUI! \n !!!Instrucitons!!!\n 1. Hello how are you doing? \n 2. come on man. \n 3. Python is an interpreted, high-level and general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use of significant indentation.")

# text.pack()
# win.mainloop()

words = [
    "Welcome to the Photo Calibration GUI",
    '!!! Instructions !!!',
    '1. Upload the template using the button below',
    '2. You will see 4 card suits surrounded by circles',
    '3. Starting at the NW corner, click on the center of the suit followed by another click on the edge',
    '4. The order should be NW, SE, SW and SE',
    '5. Enter width and height (in mm) in the entry fields',
    '6. Click on Perform Calibration and wait until the program quits automatically',
]

canvas_width = 600
canvas_height = 250

w = Canvas(win, width=canvas_width, height=canvas_height)

word_pos = [(int(canvas_width // 2), 20), (int(canvas_width // 2), 40),
            (20, 60), (20, 80), (20, 100), (20, 120), (20, 140), (20, 160)]
word_anchor = [tk.CENTER, tk.CENTER, tk.NW, tk.NW, tk.NW, tk.NW, tk.NW, tk.NW]

object_id = []
for word, (x, y), anchor in zip(words, word_pos, word_anchor):
    id = w.create_text(x, y, anchor=anchor, text=word)
    object_id.append(id)
w.pack()

btn = Button(
    text='Browse Image',
    # command=self.showimage,
    bg='brown',
    fg='white',
    font=('cambria', 9, 'bold'),
    justify='center')
w.create_window(int(canvas_width // 2), 225, window=btn)

w.itemconfigure(1, font=('cambria', 12, 'bold'))
w.itemconfigure(2, font=('cambria', 10))
win.mainloop()
