import os
from tkinter import *

import numpy as np
from PIL import Image, ImageTk
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
    return [point_list[i:i + n] for i in range(0, len(point_list) - n + 1, n)]


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

    print("Canvas: mouse clicked at ", event.x, event.y)

    pos_tuple.append([event.x * scale_up_factor, event.y * scale_up_factor])


def loadImage():
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(0, 0, anchor='nw', image=filename)
    canvas.pack()


def show_entry_fields():
    true_w = e1.get()
    true_h = e2.get()

    print("Width: %s\tHeight: %s" % (true_w, true_h))
    centers, radii = calculate_centers_and_radii(pos_tuple)
    registration(centers, radii, float(true_w), float(true_h))


if __name__ == "__main__":
    root = Tk()
    root.title('Photo Calibration GUI')

    img = Image.open(os.path.join(os.getcwd(), 'data', 'template_1.png'))
    width, height = img.width, img.height
    print(f"Image Width: {width}, Height: {height}")

    scale_down_factor = 0.2  # Should be between 0 and 1
    scale_up_factor = np.reciprocal(scale_down_factor)

    new_im_width = int(width * scale_down_factor) 
    new_im_height = int(height * scale_down_factor)

    canvas_width = int(width * (scale_down_factor + 0.05))
    canvas_height = int(height * (scale_down_factor + 0.05))

    img = img.resize((new_im_width, new_im_height), Image.ANTIALIAS)
    
    filename = ImageTk.PhotoImage(img)
    canvas = Canvas(height=canvas_height, width=canvas_width)

    root.geometry(f'{canvas_width:d}x{canvas_height:d}')

    b = Button(root,
               text='Please Click here to upload the reference image',
               command=loadImage)
    b.pack(side=TOP)

    wFrame = Frame(root)
    w = Label(wFrame, text="Width: ")  #.grid(row=0)
    e1 = Entry(wFrame)

    wFrame.pack(side=BOTTOM)
    w.pack(side=LEFT)
    e1.pack(side=LEFT)

    hFrame = Frame(root)
    h = Label(hFrame, text="Height: ")  #.grid(row=0)
    e2 = Entry(hFrame)

    hFrame.pack(side=BOTTOM)
    h.pack(side=LEFT)
    e2.pack(side=LEFT)

    calibFrame = Frame(root)
    b1 = Button(calibFrame,
                text='Perform Calibration',
                command=show_entry_fields)
    calibFrame.pack(side=BOTTOM)
    b1.pack()

    canvas.bind("<Button-1>", click)

    root.mainloop()
