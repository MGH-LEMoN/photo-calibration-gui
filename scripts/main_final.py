import os
from tkinter import *
from PIL import ImageTk, Image


global pos_tuple
pos_tuple = []


def click(event):
    """ replacement mouse handler inside Canvas, draws a red ball on each click"""

    print ("Canvas: mouse clicked at ", event.x, event.y)
    pos_tuple.append((event.x, event.y))
    print(pos_tuple)


def loadImage():
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(25,0,anchor='nw',image=filename)
    canvas.pack()


def show_entry_fields():
    print("Width: %s\tHeight: %s" % (e1.get(), e2.get()))


if __name__ == "__main__":
    root = Tk()
    root.title('Photo Calibration GUI')

    img = Image.open(os.path.join(os.getcwd(), 'data', 'template_1.png'))
    width, height = img.width, img.height
    img = img.resize((width // 6, height // 6), Image.ANTIALIAS)
    filename = ImageTk.PhotoImage(img)
    canvas = Canvas(height=height // 5, width=width // 5)

    root.geometry(f'{width // 4:d}x{height // 4:d}')

    b = Button(root, text='Please Click here to upload the reference image', command=loadImage)
    b.pack(side=TOP)

    wFrame = Frame(root)
    w = Label(wFrame, text = "Width: ") #.grid(row=0)
    e1 = Entry(wFrame)

    wFrame.pack(side=BOTTOM)
    w.pack(side=LEFT)
    e1.pack(side=LEFT)

    hFrame = Frame(root)
    h = Label(hFrame, text = "Height: ") #.grid(row=0)
    e2 = Entry(hFrame)

    hFrame.pack(side=BOTTOM)
    h.pack(side=LEFT)
    e2.pack(side=LEFT)

    calibFrame = Frame(root)
    b1 = Button(calibFrame, text='Perform Calibration', command=show_entry_fields)
    calibFrame.pack(side=BOTTOM)
    b1.pack()

    canvas.bind("<Button-1>", click)

    root.mainloop()
