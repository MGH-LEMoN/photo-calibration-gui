import os
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
from registration import registration

global pos_tuple
pos_tuple = []


def get_euclidean(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.linalg.norm(a - b)


def get_radii(point_pairs):
    return [get_euclidean(pair[0], pair[1]) for pair in point_pairs] 


def get_pairs(point_list):
    n = 2
    return [point_list[i:i+n] for i in range(0, len(point_list)-n+1, n)]


def calculate_centers_and_radii(mouse_clicks):
    centers = mouse_clicks[::2]
    point_set = get_pairs(mouse_clicks)
    radii = get_radii(point_set)

    centers = np.array(centers)
    radii = np.array(radii)

    for idx, (center, radius) in enumerate(zip(centers, radii)):
        print(f"Center {idx}: {(center[0], center[1])}, Radius: {radius:.2f}")

    return centers, radii


def click(event):
    """ replacement mouse handler inside Canvas, draws a red ball on each click"""

    print ("Canvas: mouse clicked at ", event.x, event.y)
    pos_tuple.append([event.x, event.y])


def loadImage():
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(25,0,anchor='nw',image=filename)
    canvas.pack()


def show_entry_fields():
    print("Width: %s\tHeight: %s" % (e1.get(), e2.get()))
    centers, radii, true_w, true_h = calculate_centers_and_radii(pos_tuple)
    registration(centers, radii, true_w, true_h)


if __name__ == "__main__":
    root = Tk()
    root.title('Photo Calibration GUI')

    img = Image.open(os.path.join(os.getcwd(), 'data', 'template_1.png'))
    width, height = img.width, img.height
    img = img.resize((width // 5, height // 5), Image.ANTIALIAS)
    filename = ImageTk.PhotoImage(img)
    canvas = Canvas(height=height // 4, width=width // 4)

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
