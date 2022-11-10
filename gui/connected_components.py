import glob
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

import numpy as np
from skimage.io import imread
from PIL import Image, ImageTk
from skimage.measure import label as bwlabel

from scripts.utils import set_root_position


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Start Application Window
        self.master = master
        self.master.title("Connected Components GUI")

        words = [
            "Welcome to the Connected Components GUI",
            "!!! Instructions !!!",
            "1. Select the directory with input images",
            "2. Select the directory with input masks",
            "3. Select the directory where you want the output masks saved",
            "4. For each image, select slices in order",
            "5. When finished processing the images, the program quits automatically",
        ]

        canvas_width, canvas_height = 600, 250
        set_root_position(self.master, canvas_width, canvas_height)

        self.canvas1 = Canvas(
            self.master, width=canvas_width, height=canvas_height
        )

        word_pos = [
            (int(canvas_width // 2), 20),
            (int(canvas_width // 2), 40),
            (20, 60),
            (20, 80),
            (20, 100),
            (20, 120),
            (20, 140),
        ]
        word_anchor = [tk.CENTER, tk.CENTER, tk.NW, tk.NW, tk.NW, tk.NW, tk.NW]

        object_id = []
        for word, (x, y), anchor in zip(words, word_pos, word_anchor):
            id = self.canvas1.create_text(x, y, anchor=anchor, text=word)
            object_id.append(id)
        self.canvas1.pack()

        btn = Button(
            text="Click to Start",
            command=self.folderSelectionWindow,
            bg="brown",
            fg="white",
            font=("cambria", 9, "bold"),
            justify="center",
        )
        self.canvas1.create_window(int(canvas_width // 2), 225, window=btn)

        self.canvas1.itemconfigure(1, font=("cambria", 12, "bold"))
        self.canvas1.itemconfigure(2, font=("cambria", 10))

    def folderSelectionWindow(self):
        """Contains code to generate the second window in the application"""
        # Clear canvas for the next screen
        self.clearFrame(self.canvas1)

        canvas_width, canvas_height = 700, 200
        set_root_position(self.master, canvas_width, canvas_height)

        # Create canvas for widgets
        self.canvas2 = Canvas(
            self.master, width=canvas_width, height=canvas_height
        )
        self.canvas2.pack()

        # Specify input images directory
        input_lbl = Label(
            self.master,
            text="Select the directory with input images",
            font=("Cambria", 10),
        )
        self.canvas2.create_window(10, 15, anchor=tk.W, window=input_lbl)

        input_lbl_btn = Button(
            self.master,
            text="Choose Folder ",
            font=("Cambria", 10, "bold"),
            command=self.select_input_folder,
        )
        self.canvas2.create_window(500, 15, anchor=tk.W, window=input_lbl_btn)

        self.input_lbl_val = Label(
            self.master, text="-", fg="red", font=("Cambria", 10)
        )
        self.canvas2.create_window(
            10, 30, anchor=tk.W, window=self.input_lbl_val
        )

        # Specify directory with masks
        mask_lbl = Label(
            self.master,
            font=("Cambria", 10),
            text="Select the directory with masks",
        )
        self.canvas2.create_window(10, 55, anchor=tk.W, window=mask_lbl)

        mask_lbl_btn = Button(
            self.master,
            text="Choose Folder ",
            font=("Cambria", 10, "bold"),
            command=self.select_mask_folder,
        )
        self.canvas2.create_window(500, 55, anchor=tk.W, window=mask_lbl_btn)

        self.mask_lbl_val = Label(
            self.master, text="-", fg="red", font=("Cambria", 10)
        )
        self.canvas2.create_window(
            10, 70, anchor=tk.W, window=self.mask_lbl_val
        )

        # Specify directory to store updated masks
        output_lbl = Label(
            self.master,
            font=("Cambria", 10),
            text="Select the directory to store output masks",
        )
        self.canvas2.create_window(10, 100, anchor=tk.W, window=output_lbl)

        output_lbl_btn = Button(
            self.master,
            text="Choose Folder ",
            font=("Cambria", 10, "bold"),
            command=self.select_output_folder,
        )
        self.canvas2.create_window(500, 100, anchor=tk.W, window=output_lbl_btn)

        self.output_lbl_val = Label(
            self.master, text="-", fg="red", font=("Cambria", 10)
        )
        self.canvas2.create_window(
            10, 120, anchor=tk.W, window=self.output_lbl_val
        )

        upld_btn = Button(
            self.master,
            text="Click here",
            bg="brown",
            fg="white",
            command=self.display_image_for_slice_selection,
        )
        self.canvas2.create_window(350, 160, anchor=tk.CENTER, window=upld_btn)

    def display_image_for_slice_selection(self):
        # Clear canvas for the next screen
        self.clearFrame(self.canvas2)

        # Paint on screen
        self.canvas3 = Canvas(self.master)
        self.canvas3.pack()

        # assuming the images have been matched
        self.image_mask_pair = iter(zip(self.input_images, self.mask_images))

        # show the first image
        self.next_img()

        self.canvas3.update()

    def next_img(self):
        try:
            self.current_image, self.current_mask = next(self.image_mask_pair)
        except StopIteration:
            messagebox.showinfo(
                title="End of Images",
                message="No More Images to Process\n Quit Program",
            )

            self.master.destroy()
            return

        # Open image
        self.image = imread(self.current_image)

        # Open mask
        self.mask = imread(self.current_mask, as_gray=True)
        self.mask = self.mask > np.max(self.mask) / 2

        # Create connected components
        self.connected_components = bwlabel(self.mask)

        # check with E about this
        masked_image = self.image * self.mask[:, :, np.newaxis]

        # Open mask
        self.img_fullres = Image.fromarray(masked_image)

        # get width and height of image
        im_width, im_height = self.img_fullres.width, self.img_fullres.height

        # Resize so it fits on screen
        screen_res = 512
        self.scale_down_factor_screen = screen_res / np.min(
            np.array([im_width, im_height])
        )

        new_im_width = int(im_width * self.scale_down_factor_screen)
        new_im_height = int(im_height * self.scale_down_factor_screen)

        img_screen = self.img_fullres.resize(
            (new_im_width, new_im_height), Image.ANTIALIAS
        )
        img_screen = ImageTk.PhotoImage(img_screen)

        self.canvas3.config(width=new_im_width, height=new_im_height + 150)
        self.canvas3.image = img_screen
        self.canvas3.create_image(0, 0, anchor="nw", image=self.canvas3.image)

        self.topx, self.topy = 0, 0
        self.botx, self.boty = 0, 0

        self.rect_id = None

        self.rect_list = list()
        self.rect_main_data = list()

        self.canvas3.update()
        canvas_width = self.canvas3.winfo_width()
        canvas_height = self.canvas3.winfo_height()

        self.b1 = Button(
            self.master,
            text="Create Mask",
            command=self.create_mask,
            bg="brown",
            fg="white",
            font=("cambria", 9, "bold"),
        )
        self.canvas3.create_window(
            canvas_width // 2, canvas_height - 50, anchor=tk.NE, window=self.b1
        )

        self.b2 = Button(
            self.master,
            text="Next Image",
            command=self.next_img,
            bg="brown",
            fg="white",
            font=("cambria", 9, "bold"),
        )
        self.canvas3.create_window(
            canvas_width // 2, canvas_height - 50, anchor=tk.NW, window=self.b2
        )

        self.rect_id = self.canvas3.create_rectangle(
            self.topx,
            self.topy,
            self.botx,
            self.boty,
            dash=(2, 2),
            fill="",
            outline="red",
        )

        self.canvas3.bind("<Button-1>", self.get_mouse_posn)
        self.canvas3.bind("<B1-Motion>", self.update_sel_rect)
        self.canvas3.bind("<ButtonRelease-1>", self.draw_rect)
        self.canvas3.bind("<Double-3>", self.onClear)

        self.canvas3.update()

    def create_mask(self):
        for idx, rect_coords in enumerate(self.rect_list):
            self.rect_list[idx] = np.array(
                np.array(rect_coords) // self.scale_down_factor_screen,
                dtype="int",
            )

        binary_mask = np.zeros(self.image.shape[0:2])
        for idx, rectangle in enumerate(self.rect_list, 1):
            # Find all unique indices of label image inside rectangle (> 0)
            x1, y1, x2, y2 = rectangle

            if x1 > x2:
                x1, x2 = x2, x1

            if y1 > y2:
                y1, y2 = y2, y1

            # create binary mask with all regions of label image wtih such indices
            unique = np.unique(self.connected_components[y1:y2, x1:x2])
            unique = unique[unique > 0]

            for val in unique:
                binary_mask[self.connected_components == val] = idx

        input_path, _ = os.path.splitext(self.current_image)
        _, input_name = os.path.split(input_path)
        self.output_mask = input_name + "_mask"

        np.save(os.path.join(self.output_folder, self.output_mask), binary_mask)

    def clearFrame(self, frame):
        """clears the previous frame

        Args:
            frame (Tk.Frame): Previous Frame Object
        """
        # destroy all widgets from frame
        for widget in frame.winfo_children():
            widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        frame.pack_forget()

    def select_input_folder(self):
        """Input directory selection"""
        self.input_folder = filedialog.askdirectory()
        self.input_lbl_val["text"] = self.input_folder

        self.input_images = sorted(
            glob.glob(os.path.join(self.input_folder, "*.*"))
        )

    def select_mask_folder(self):
        """Mask directory selection"""
        self.mask_folder = filedialog.askdirectory()
        self.mask_lbl_val["text"] = self.mask_folder

        self.mask_images = sorted(
            glob.glob(os.path.join(self.mask_folder, "*.*"))
        )

    def select_output_folder(self):
        """Output directory selection to save the masks"""
        self.output_folder = filedialog.askdirectory()
        self.output_lbl_val["text"] = self.output_folder

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas3.coords(
            self.rect_id, self.topx, self.topy, self.botx, self.boty
        )  # Update selection rect.

    def draw_rect(self, event):
        draw_data = self.canvas3.create_rectangle(
            self.topx, self.topy, self.botx, self.boty, outline="green", fill=""
        )
        self.rect_list.append((self.topx, self.topy, self.botx, self.boty))
        self.rect_main_data.append(draw_data)

    def onClear(self, event):
        # event.widget.delete('all')

        if len(self.rect_main_data) > 0:
            for rect in self.rect_main_data:
                self.canvas3.delete(rect)

        self.rect_main_data.clear()
        self.rect_list.clear()

        self.topx, self.topy = 0, 0
        self.botx, self.boty = 0, 0

        self.canvas3.create_image(0, 0, anchor="nw", image=self.canvas3.image)
        self.rect_id = self.canvas3.create_rectangle(
            self.topx,
            self.topy,
            self.botx,
            self.boty,
            dash=(2, 2),
            fill="",
            outline="red",
        )


if __name__ == "__main__":
    app = Application(Tk())
    app.mainloop()
