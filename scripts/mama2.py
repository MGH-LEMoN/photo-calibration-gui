import glob
import os
import tkinter as tk
from tkinter import *

import numpy as np
from PIL import Image, ImageTk


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        win = master

        win.geometry('800x500')  # set window size
        win.resizable(0, 0)  # fix window

        self.panel = tk.Canvas(win)
        self.panel.pack()

        self.images = sorted(
            glob.glob(
                '/space/calico/1/users/Harsha/photo-calibration-gui/unk_input/*.JPG'
            ))

        self.images = iter(self.images)  # make an iterator

        self.btn = tk.Button(text='Next image', command=self.next_img)
        self.btn.pack()

        # show the first image
        self.next_img()

        self.panel.update()

    def next_img(self):
        try:
            img = next(self.images)  # get the next image from the iterator
            print(os.path.split(img)[1])
        except StopIteration:
            self.btn['text'] = 'Stop'
            return  # if there are no more images, do nothing

        # load the image and display it
        img = Image.open(img)

        # get width and height of image
        width, height = img.width, img.height

        # Resize so it fits on screen
        screen_res = 256
        scale_down_factor_screen = screen_res / np.min(
            np.array([width, height]))

        new_im_width = int(width * scale_down_factor_screen)
        new_im_height = int(height * scale_down_factor_screen)

        img_screen = img.resize((new_im_width, new_im_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_screen)

        # panel.img = img  # keep a reference so it's not garbage collected
        self.panel.image = img
        # panel['image'] = img
        self.panel.create_image(0, 0, anchor='nw', image=self.panel.image)


if __name__ == '__main__':
    win = Application(Tk())
    win.mainloop()
