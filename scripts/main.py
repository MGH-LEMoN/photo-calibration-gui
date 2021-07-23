import os
from tkinter import *
from tkinter import filedialog

import numpy as np
from PIL import Image, ImageTk
# from registration import registration
import cv2

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

    # close gui
    root.quit()
    root.destroy()  # this solves the problem in Eugenio's linux machine...

    print("Width: %s\tHeight: %s" % (true_w, true_h))

    # extract centers and radius
    centers, radii = calculate_centers_and_radii(pos_tuple)

    # Perform registration
    # registration(centers, radii, float(true_w), float(true_h), fln)

    centers = centers * scale_down_factor_sift
    radii = radii * scale_down_factor_sift * 0.9  # we don't want to detect keypoints on the circle
    sift = cv2.SIFT_create()
    template = np.array(img_sift.convert('LA'))[:, :, 0]
    kp_template, des_template = sift.detectAndCompute(template, None)

    # Keep only keypoints within radius
    kp_tmp = []
    des_tmp = np.zeros(shape=(0, des_template.shape[1]), dtype='float32')
    for c in range(4):
        for i in range(len(kp_template)):
            dist = np.sqrt(np.sum((kp_template[i].pt - centers[c, :])**2))
            if dist < (radii[c]):
                # kp_tmp.append(kp_template[i])

                temp = (kp_template[i].pt, kp_template[i].size, kp_template[i].angle, kp_template[i].response, kp_template[i].octave, kp_template[i].class_id)
                kp_tmp.append(temp)

                des_tmp = np.vstack((des_tmp, des_template[i, :]))

    kp_template = kp_tmp
    des_template = des_tmp

    # TODO: Harsha, please select output file with a dialog
    # Also: we don't really need to save the image, but we do it for visualization purposes
    model_file = '/tmp/model.npz'

    np.savez(model_file, img_template=template, kp_template=kp_template, des_template=des_template, true_w=true_w, true_h=true_h, centers=centers)

    if True:  # TODO:  if DEBUG or something like that?

        import matplotlib.pyplot as plt

        # A bit silly, but we need to reassemble the key points (which we split for saving to disk)
        kp = []
        for point in kp_template:
            temp = cv2.KeyPoint(x=point[0][0], y=point[0][1], size=point[1], angle=point[2], response=point[3],
                                octave=point[4], class_id=point[5])
            kp.append(temp)

        kp_im_template = template.copy()
        kp_im_template = cv2.drawKeypoints(
            template,
            kp,
            kp_im_template,
            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        plt.figure(), plt.imshow(kp_im_template, aspect='equal'), plt.title(
            'Key points in template image'), plt.show()






def showimage():
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

    sift_res = 1024  #TODO: move definition elsewhere?
    screen_res = 512
    # scale_down_factor = 0.2  # Should be between 0 and 1
    global scale_down_factor_sift  # Eugenio
    scale_down_factor_sift = sift_res / np.min(np.array([width, height]))
    global scale_down_factor_screen  # Eugenio
    scale_down_factor_screen = screen_res / np.min(np.array([width, height]))

    global scale_up_factor
    scale_up_factor = np.reciprocal(scale_down_factor_screen)

    # resize image to fit on screen
    new_im_width = int(width * scale_down_factor_sift)
    new_im_height = int(height * scale_down_factor_sift)
    global img_sift
    img_sift = img.resize((new_im_width, new_im_height), Image.ANTIALIAS)

    # resize image to fit on screen
    new_im_width = int(width * scale_down_factor_screen)
    new_im_height = int(height * scale_down_factor_screen)
    img = img.resize((new_im_width, new_im_height), Image.ANTIALIAS)

    # print image on canvas/gui
    img = ImageTk.PhotoImage(img)

    # Clear canvas for the next screen
    clearFrame(canvas1)

    # New canvas
    canvas = Canvas(height=new_im_height, width=new_im_width)
    canvas.image = img
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.pack()

    frame = Frame(root)
    frame.pack()

    w = Label(frame, text="Width: ", font=('Cambria', 10, 'bold'))
    global e1
    e1 = Entry(frame, width=10)

    w.pack(side=LEFT)
    e1.pack(side=LEFT)

    h = Label(frame, text="Height: ", font=('Cambria', 10, 'bold'))
    global e2
    e2 = Entry(frame, width=10)

    h.pack(side=LEFT)
    e2.pack(side=LEFT)

    calibFrame = Frame(root)
    b1 = Button(calibFrame,
                text='Perform Calibration',
                command=perform_calibration,
                bg='brown',
                fg='white',
                font=('cambria', 9, 'bold'))
    calibFrame.pack(side=BOTTOM)
    b1.pack()

    canvas.bind("<Button-1>", click)


if __name__ == '__main__':
    root = Tk()
    root.title('Photo Calibration GUI')

    # Create canvas for widgets
    canvas1 = Canvas(root, width=350, height=350)
    canvas1.pack()

    label1 = Label(root, text='Welcome to the Photo Calibration GUI')
    label1.config(font=('cambria', 14))
    canvas1.create_window(175, 25, window=label1)

    label_inst = Label(root, text='!!! Instructions !!!')
    label_inst.config(font=('cambria', 12, 'bold'))
    canvas1.create_window(175, 60, window=label_inst)

    inst_1 = Label(root, text='1. Upload the template using the button below')
    inst_1.config(font=('cambria', 10))
    canvas1.create_window(175, 80, window=inst_1)

    inst_2 = Label(root,
                   text='2. You will see 4 card suits surrounded by circles')
    inst_2.config(font=('cambria', 10))
    canvas1.create_window(175, 100, window=inst_2)

    inst_3 = Label(
        root,
        wraplength=325,
        text=
        '3. Starting at the NW corner, click on the center of the suit followed by another click on the edge'
    )
    inst_3.config(font=('cambria', 10))
    canvas1.create_window(175, 130, window=inst_3)

    inst_4 = Label(root,
                   wraplength=325,
                   text='4. The order should be NW, SE, SW and SE')
    inst_4.config(font=('cambria', 10))
    canvas1.create_window(175, 160, window=inst_4)

    inst_5 = Label(
        root,
        wraplength=325,
        text='5. Enter width and height (in mm) in the entry fields')
    inst_5.config(font=('cambria', 10))
    canvas1.create_window(175, 185, window=inst_5)

    inst_6 = Label(
        root,
        wraplength=325,
        text=
        '6. Click on Perform Calibration and wait until the program quits automatically'
    )
    inst_6.config(font=('cambria', 10))
    canvas1.create_window(175, 220, window=inst_6)

    btn = Button(text='Browse Image',
                 command=showimage,
                 bg='brown',
                 fg='white',
                 font=('cambria', 9, 'bold'))
    canvas1.create_window(175, 275, window=btn)

    root.mainloop()
