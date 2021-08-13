import glob
import os
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

win = tk.Tk()
win.geometry('800x500')  # set window size
win.resizable(0, 0)  # fix window

# panel = tk.Label(win)
panel = tk.Canvas(win)
panel.pack()

images = sorted(
    glob.glob(
        '/space/calico/1/users/Harsha/photo-calibration-gui/unk_input/*.JPG'))

images = iter(images)  # make an iterator


def next_img():
    try:
        img = next(images)  # get the next image from the iterator
        print(os.path.split(img)[1])
    except StopIteration:
        btn['text'] = 'Stop'
        btn.pack()
        return  # if there are no more images, do nothing

    # load the image and display it
    img = Image.open(img)

    # get width and height of image
    width, height = img.width, img.height

    # Resize so it fits on screen
    screen_res = 256
    scale_down_factor_screen = screen_res / np.min(np.array([width, height]))

    new_im_width = int(width * scale_down_factor_screen)
    new_im_height = int(height * scale_down_factor_screen)

    img_screen = img.resize((new_im_width, new_im_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img_screen)

    # panel.img = img  # keep a reference so it's not garbage collected
    panel.image = img
    # panel['image'] = img
    panel.create_image(0, 0, anchor='nw', image=panel.image)


btn = tk.Button(text='Next image', command=next_img)
btn.pack()

# show the first image
next_img()

win.mainloop()
