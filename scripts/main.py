import os
from tkinter import *
from tkinter import filedialog

import numpy as np
from PIL import Image, ImageTk
from registration import registration

global pos_tuple
pos_tuple = []


def click(event):
    """Replacement mouse handler inside Canvas, draws a blue ball on each click"""

    # Save the coordinates to a list
    print("Canvas: mouse clicked at ", event.x, event.y)
    pos_tuple.append([event.x * scale_up_factor, event.y * scale_up_factor])

    # Place a blue dot at every click of mouse
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, outline='blue', fill='blue', width=5)


def clearFrame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
        widget.destroy()

    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    frame.pack_forget()


def get_euclidean(a, b):
    """Calculate Euclidean Distance between two points a and b

    Args:
        a (float): center
        b (float): edge

    Returns:
        float: radius
    """
    a = np.array(a)
    b = np.array(b)

    return np.linalg.norm(a - b)


def get_radii(point_pairs):
    """Calculate radius using (center, edge) pair

    Args:
        point_pairs (list): list of lists where each element is a [center, edge] pair

    Returns:
        list: list of radii (size if equal to len(point_pairs))
    """
    return [get_euclidean(pair[0], pair[1]) for pair in point_pairs]


def get_pairs(point_list):
    """Converts list of point clicks to pairs of points
    A pair represents (center, edge) 

    Args:
        point_list (list): list of ordered click on the template

    Returns:
        list: list of lists where each sublist represents a (center, edge) pair
    """
    n = 2
    return [point_list[i:i + n] for i in range(0, len(point_list) - n + 1, n)]


def calculate_centers_and_radii(mouse_clicks):
    """Calculate centers and radius of the balls on the template

    Args:
        mouse_clicks (list): ordered list of mouse clicks

    Returns:
        tuple: (centers, radius)
    """
    centers = mouse_clicks[::2]
    point_set = get_pairs(mouse_clicks)
    radii = get_radii(point_set)

    centers = np.array(centers)
    radii = np.array(radii)

    for idx, (center, radius) in enumerate(zip(centers, radii)):
        print(f"Center {idx}: {(center[0], center[1])}, Radius: {radius:.2f}")

    return centers, radii


def perform_calibration():
    """This function performs the calibration/registration and close the GUI automatically
    """
    global root
    true_w = e1.get()
    true_h = e2.get()

    print("Width: %s\tHeight: %s" % (true_w, true_h))

    # extract centers and radius
    centers, radii = calculate_centers_and_radii(pos_tuple)
    
    # Perform registraion
    registration(centers, radii, float(true_w), float(true_h), fln)

    # close gui
    root.quit()


def showimage():
    clearFrame(frm)

    global fln
    global canvas

    # open file upload dialog
    fln = filedialog.askopenfilename(initialdir=os.getcwd(),
                                     title='Select Image File',
                                     filetypes=[('All Files', '*.*')])
    # Open image
    img = Image.open(fln)

    # get width and height of image
    width, height = img.width, img.height
    print(f"Image Width: {width}, Height: {height}")

    scale_down_factor = 0.2  # Should be between 0 and 1

    global scale_up_factor
    scale_up_factor = np.reciprocal(scale_down_factor)

    new_im_width = int(width * scale_down_factor)
    new_im_height = int(height * scale_down_factor)

    # resize image to fit on screen
    img = img.resize((new_im_width, new_im_height), Image.ANTIALIAS)

    # print image on canvas/gui
    img = ImageTk.PhotoImage(img)

    root.geometry("")
    canvas = Canvas(height=new_im_height, width=new_im_width)
    canvas.image = img
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.pack()

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
                command=perform_calibration)
    calibFrame.pack(side=BOTTOM)
    b1.pack()

    canvas.bind("<Button-1>", click)


if __name__ == '__main__':
    root = Tk()

    # Frame for Upload Image button
    frm = Frame(root)
    frm.pack(side=TOP)

    btn = Button(frm, text='Browse Image', command=showimage)
    btn.pack(side=LEFT)

    root.title('Photo Calibration GUI')
    root.geometry('250x250')
    root.mainloop()
