import glob
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

import cv2
import numpy as np
import screeninfo
from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError

from scripts.utils import set_root_position


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Declare variables
        self.input_folder_path = None
        self.output_folder_path = None

        self.true_width = None
        self.true_height = None

        # Start Application Window
        self.master = master
        self.master.title("Retrospective Photo Registration GUI")

        words = [
            "Welcome to the Retrospective Photo Registration GUI",
            "!!! Instructions !!!",
            "1. Select the directory where the input images are",
            "2. Select the directory where you want the output images saved",
            "3. Click on 4 corners of a rectangle for every image and provide the dimensions in mm",
            "4. Click on Register button and wait until the program loads the next image",
        ]

        canvas_width, canvas_height = 600, 200
        set_root_position(self.master, canvas_width, canvas_height)

        self.canvas1 = Canvas(self.master, width=canvas_width, height=canvas_height)

        word_pos = [
            (int(canvas_width // 2), 20),
            (int(canvas_width // 2), 40),
            (20, 60),
            (20, 80),
            (20, 100),
            (20, 120),
        ]
        word_anchor = [tk.CENTER, tk.CENTER, tk.NW, tk.NW, tk.NW, tk.NW]

        object_id = []
        for word, (x, y), anchor in zip(words, word_pos, word_anchor):
            id = self.canvas1.create_text(x, y, anchor=anchor, text=word)
            object_id.append(id)
        self.canvas1.pack()

        btn = Button(
            text="Click to Start",
            command=self.fileUploadWindow,
            bg="brown",
            fg="white",
            font=("cambria", 9, "bold"),
            justify="center",
        )
        self.canvas1.create_window(int(canvas_width // 2), 175, window=btn)

        self.canvas1.itemconfigure(1, font=("cambria", 12, "bold"))
        self.canvas1.itemconfigure(2, font=("cambria", 10))

        self.horizontal_ruler = cv2.imread("./resources/horizontal.png")
        self.vertical_ruler = cv2.imread("./resources/vertical.png")

    def fileUploadWindow(self):
        """Contains code to generate the second window in the application"""
        # Clear canvas for the next screen
        self.clearFrame(self.canvas1)

        # Create canvas for widgets
        self.canvas2 = Canvas(self.master, width=600, height=200)
        self.canvas2.pack()

        # Specify input images directory
        input_lbl = Label(
            self.master,
            text="Select the input directory for uncorrected images ",
            font=("Cambria", 10),
        )
        self.canvas2.create_window(10, 10, anchor=tk.NW, window=input_lbl)

        input_lbl_btn = Button(
            self.master,
            text="Choose Folder ",
            font=("Cambria", 10, "bold"),
            command=self.open_input_folder,
        )
        self.canvas2.create_window(450, 10, anchor=tk.NW, window=input_lbl_btn)

        self.input_lbl_val = Label(
            self.master, text="-", fg="red", font=("Cambria", 10)
        )
        self.canvas2.create_window(10, 35, anchor=tk.NW, window=self.input_lbl_val)

        # Specify directory to store corrected images
        output_lbl = Label(
            self.master,
            font=("Cambria", 10),
            text="Select the output directory for corrected images \n (must already exist)",
        )
        self.canvas2.create_window(10, 60, anchor=tk.NW, window=output_lbl)

        output_lbl_btn = Button(
            self.master,
            text="Choose Folder ",
            font=("Cambria", 10, "bold"),
            command=self.open_output_folder,
        )
        self.canvas2.create_window(450, 60, anchor=tk.NW, window=output_lbl_btn)

        self.output_lbl_val = Label(
            self.master, text="-", fg="red", font=("Cambria", 10)
        )
        self.canvas2.create_window(10, 90, anchor=tk.NW, window=self.output_lbl_val)

        mode_lbl = Label(self.master, font=("Cambria", 10), text="Select Mode: ")
        self.canvas2.create_window(100, 115, anchor=tk.NW, window=mode_lbl)

        self.radio_var = IntVar()
        R1 = Radiobutton(self.master, text="4 Points", variable=self.radio_var, value=1)
        self.canvas2.create_window(225, 115, anchor=tk.NW, window=R1)

        R2 = Radiobutton(self.master, text="2 Points", variable=self.radio_var, value=2)
        self.canvas2.create_window(350, 115, anchor=tk.NW, window=R2)

        upld_btn = Button(
            self.master,
            text="Register Images",
            bg="brown",
            fg="white",
            command=self.create_mask_section,
        )
        self.canvas2.create_window(300, 160, anchor=tk.CENTER, window=upld_btn)

    def create_mask_section(self):
        # Clear canvas for the next screen
        self.clearFrame(self.canvas2)

        # Paint on screen
        self.canvas3 = Canvas(self.master)
        self.canvas3.pack()

        # assuming the images have been matched
        self.input_images = iter(self.input_images)

        # show the first image
        self.next_img()

        self.canvas3.update()

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

    def open_input_folder(self):
        """Input directory selection"""
        self.input_folder_path = filedialog.askdirectory()
        self.input_images = sorted(
            glob.glob(os.path.join(self.input_folder_path, "*.*"))
        )

        self.input_lbl_val["text"] = self.input_folder_path

    def open_output_folder(self):
        """Output directory selection"""
        self.output_folder_path = filedialog.askdirectory()
        self.output_lbl_val["text"] = self.output_folder_path

    def next_img(self):
        try:
            self.input_image = next(self.input_images)
        except StopIteration:
            messagebox.showinfo(
                title="End of Images",
                message="No More Images to Process\n Quit Program",
            )

            self.master.destroy()
            return

        input_path, input_ext = os.path.splitext(self.input_image)
        _, input_name = os.path.split(input_path)
        self.output_image = os.path.join(
            self.output_folder_path, input_name + "_deformed" + input_ext
        )

        self.pos_tuple = []

        # Open image
        try:
            self.img_fullres = Image.open(self.input_image)
            self.img_fullres = ImageOps.exif_transpose(self.img_fullres)
        except UnidentifiedImageError:
            self.next_img()

        # get width and height of image
        width, height = self.img_fullres.width, self.img_fullres.height

        # Resize so if fits on screen
        screen_res = 512
        self.scale_down_factor_screen = screen_res / np.min(np.array([width, height]))

        new_im_width = int(width * self.scale_down_factor_screen)
        new_im_height = int(height * self.scale_down_factor_screen)

        img_screen = self.img_fullres.resize(
            (new_im_width, new_im_height), Image.ANTIALIAS
        )

        img_screen = ImageTk.PhotoImage(img_screen)

        # Paint on screen
        self.canvas3.config(height=new_im_height + 150, width=new_im_width)
        self.canvas3.image = img_screen
        self.canvas3.create_image(0, 0, anchor="nw", image=img_screen)
        self.canvas3.pack()

        self.canvas3.update()
        canvas_width = self.canvas3.winfo_width()
        canvas_height = self.canvas3.winfo_height()

        if self.radio_var.get() == 1:
            w = Label(self.master, text="Width (mm): ", font=("Cambria", 10, "bold"))
            self.e1 = Entry(self.master, width=10)
            self.e1.var = tk.DoubleVar()
            self.e1["textvariable"] = self.e1.var
            self.e1.var.set(0)

            self.canvas3.create_window(
                canvas_width // 2, canvas_height - 105, anchor=tk.NE, window=w
            )
            self.canvas3.create_window(
                canvas_width // 2,
                canvas_height - 105,
                anchor=tk.NW,
                window=self.e1,
            )

            h = Label(self.master, text="Height (mm): ", font=("Cambria", 10, "bold"))
            self.e2 = Entry(self.master, width=10)
            self.e2.var = tk.DoubleVar()
            self.e2["textvariable"] = self.e2.var
            self.e2.var.set(0)

            self.canvas3.create_window(
                canvas_width // 2, canvas_height - 80, anchor=tk.NE, window=h
            )
            self.canvas3.create_window(
                canvas_width // 2,
                canvas_height - 80,
                anchor=tk.NW,
                window=self.e2,
            )
        else:
            w = Label(
                self.master,
                text="Ruler Length (in mm): ",
                font=("Cambria", 10, "bold"),
            )
            self.e1 = Entry(self.master, width=10)
            self.e1.var = tk.DoubleVar()
            self.e1["textvariable"] = self.e1.var
            self.e1.var.set(0)

            self.canvas3.create_window(
                canvas_width // 2, canvas_height - 105, anchor=tk.NE, window=w
            )
            self.canvas3.create_window(
                canvas_width // 2,
                canvas_height - 105,
                anchor=tk.NW,
                window=self.e1,
            )

        self.b1 = Button(
            self.master,
            text="Register",
            command=lambda: [self.perform_registration(), self.activate_next()],
            bg="brown",
            fg="white",
            font=("cambria", 9, "bold"),
        )
        self.canvas3.create_window(
            canvas_width // 2, canvas_height - 40, anchor=tk.NE, window=self.b1
        )

        self.b2 = Button(
            self.master,
            text="Next",
            command=self.next_img,
            font=("cambria", 9, "bold"),
        )
        self.b2.configure(relief=tk.SUNKEN, state=tk.DISABLED)
        self.canvas3.create_window(
            canvas_width // 2, canvas_height - 40, anchor=tk.NW, window=self.b2
        )

        self.canvas3.bind("<Button-1>", self.click)

    def activate_next(self):
        self.b2.configure(relief=tk.RAISED, state=tk.ACTIVE, bg="brown", fg="white")

    def perform_registration(self):
        """This function performs the registration and close the GUI automatically"""

        if self.radio_var.get() == 1:
            # TODO code for 4 button clicks
            # take only the first 4 points
            self.pos_tuple = self.pos_tuple[:4]

            true_width = float(self.e1.get())
            true_height = float(self.e2.get())

        else:
            # TODO code for 2 button clicks
            self.pos_tuple = self.pos_tuple[:2]

            # We pretend the user clicked on the 4 corners of the image
            # and make the true_width and true_height proportional to the provided length
            pix_dist = (
                np.sqrt(
                    (self.pos_tuple[0][0] - self.pos_tuple[1][0]) ** 2
                    + (self.pos_tuple[0][1] - self.pos_tuple[1][1]) ** 2
                )
                / self.scale_down_factor_screen
            )
            pix_siz = float(self.e1.get()) / pix_dist
            true_width = pix_siz * self.img_fullres.size[0]
            true_height = pix_siz * self.img_fullres.size[1]
            self.pos_tuple = [
                [0, 0],
                [
                    0,
                    self.img_fullres.size[1] * self.scale_down_factor_screen - 1,
                ],
                [
                    self.img_fullres.size[0] * self.scale_down_factor_screen - 1,
                    0,
                ],
                [
                    self.img_fullres.size[0] * self.scale_down_factor_screen - 1,
                    self.img_fullres.size[1] * self.scale_down_factor_screen - 1,
                ],
            ]

        reference_pixel_size = 0.1

        centers_target = np.array(self.pos_tuple) / self.scale_down_factor_screen
        centers_target = centers_target[:, np.newaxis, :]

        # Now we only have to compute the final transform. The only caveat is the ordering of the corners...
        # We reorder then to NW, NE, SW, SE
        centers_target_reordered = np.zeros_like(centers_target)

        cost = centers_target[:, 0, 0] + centers_target[:, 0, 1]
        idx = np.argmin(cost)
        centers_target_reordered[0, 0, :] = centers_target[idx, 0, :]
        centers_target[idx, 0, :] = 0

        cost = -centers_target[:, 0, 0] + centers_target[:, 0, 1]
        cost[cost == 0] = 1e10
        idx = np.argmin(cost)
        centers_target_reordered[1, 0, :] = centers_target[idx, 0, :]
        centers_target[idx, 0, :] = 0

        cost = centers_target[:, 0, 0] - centers_target[:, 0, 1]
        cost[cost == 0] = 1e10
        idx = np.argmin(cost)
        centers_target_reordered[2, 0, :] = centers_target[idx, 0, :]
        centers_target[idx, 0, :] = 0

        cost = -centers_target[:, 0, 0] - centers_target[:, 0, 1]
        cost[cost == 0] = 1e10
        idx = np.argmin(cost)
        centers_target_reordered[3, 0, :] = centers_target[idx, 0, :]
        centers_target[idx, 0, :] = 0

        # We now define the target coordinates using the reerence resolution
        ref_coords = np.zeros_like(centers_target)

        ref_coords[0, 0, 0] = 0
        ref_coords[0, 0, 1] = 0

        ref_coords[1, 0, 0] = np.round(true_width / reference_pixel_size) - 1
        ref_coords[1, 0, 1] = 0

        ref_coords[2, 0, 0] = 0
        ref_coords[2, 0, 1] = np.round(true_height / reference_pixel_size) - 1

        ref_coords[3, 0, 0] = np.round(true_width / reference_pixel_size) - 1
        ref_coords[3, 0, 1] = np.round(true_height / reference_pixel_size) - 1

        PAD = 10.0 / reference_pixel_size  # pad 10mm (in pixels)
        ref_coords = ref_coords + PAD

        # We compute the final perspective transform
        M2, _ = cv2.findHomography(centers_target_reordered, ref_coords)
        self.deformed_image = cv2.warpPerspective(
            np.asarray(self.img_fullres),
            M2,
            (
                (PAD + ref_coords[1, 0, 0]).astype(int) + 1,
                (PAD + ref_coords[2, 0, 1]).astype(int) + 1,
            ),
        )

        image_with_ruler = np.zeros(
            (
                self.deformed_image.shape[0] + self.horizontal_ruler.shape[0],
                self.deformed_image.shape[1] + self.vertical_ruler.shape[1],
                3,
            ),
            dtype="uint8",
        )

        image_with_ruler[
            0 : self.deformed_image.shape[0],
            0 : self.deformed_image.shape[1],
            :,
        ] = cv2.cvtColor(self.deformed_image, cv2.COLOR_RGB2BGR)
        image_with_ruler[
            self.deformed_image.shape[0] :, 0 : -self.vertical_ruler.shape[1], :
        ] = self.horizontal_ruler[:, 0 : self.deformed_image.shape[1], :]
        image_with_ruler[
            0 : self.deformed_image.shape[0], -self.vertical_ruler.shape[1] :, :
        ] = self.vertical_ruler[0 : self.deformed_image.shape[0], :, :]

        cv2.imwrite(self.output_image, image_with_ruler)

    def click(self, event):
        """Replacement mouse handler inside Canvas, draws a blue ball on each click"""

        # Save the coordinates to a list
        print("Canvas: mouse clicked at ", event.x, event.y)
        self.pos_tuple.append([event.x, event.y])

        # Place a blue dot at every click of mouse
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        self.canvas3.create_oval(x1, y1, x2, y2, outline="blue", fill="blue", width=5)


if __name__ == "__main__":
    app = Application(Tk())
    app.mainloop()
