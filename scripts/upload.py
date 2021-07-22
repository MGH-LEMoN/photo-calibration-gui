import os
from tkinter import *
from tkinter import filedialog
import tkinter
from PIL import Image, ImageTk
import numpy as np
from registration import registration

global pos_tuple
pos_tuple = []


def click(event):
    """ replacement mouse handler inside Canvas, draws a red ball on each click"""

    print("Canvas: mouse clicked at ", event.x, event.y)

    pos_tuple.append([event.x * scale_up_factor, event.y * scale_up_factor])


def clearFrame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
       widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    frame.pack_forget()


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


def show_entry_fields():
    global root
    true_w = e1.get()
    true_h = e2.get()

    print("Width: %s\tHeight: %s" % (true_w, true_h))
    centers, radii = calculate_centers_and_radii(pos_tuple)
    registration(centers, radii, float(true_w), float(true_h), fln)

    root.quit()


def showimage():
    clearFrame(frm)
    
    global fln
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File',
    filetypes=[('All Files', '*.*')])
    img = Image.open(fln)
    
    width, height = img.width, img.height
    print(f"Image Width: {width}, Height: {height}")

    scale_down_factor = 0.2  # Should be between 0 and 1

    global scale_up_factor
    scale_up_factor = np.reciprocal(scale_down_factor)

    new_im_width = int(width * scale_down_factor) 
    new_im_height = int(height * scale_down_factor)

    # canvas_width = int(width * (scale_down_factor + 0.05))
    # canvas_height = int(height * (scale_down_factor + 0.05))

    img = img.resize((new_im_width, new_im_height), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img

    wFrame = Frame(root)
    w = Label(wFrame, text="Width: ")  #.grid(row=0)
    global e1
    e1 = Entry(wFrame)

    wFrame.pack(side=BOTTOM)
    w.pack(side=LEFT)
    e1.pack(side=LEFT)

    hFrame = Frame(root)
    h = Label(hFrame, text="Height: ")  #.grid(row=0)
    global e2
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

    lbl.bind("<Button-1>", click)


root = Tk()
root.title('Photo Calibration GUI')

frm = Frame(root)
frm.pack(side=TOP)

lbl = Label(root)
lbl.pack()

btn = Button(frm, text='Browse Image', command=showimage)
btn.pack(side=LEFT)



root.mainloop()