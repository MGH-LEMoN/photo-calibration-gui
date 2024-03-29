import glob
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np

from old_gui.backend.functions import set_root_position
from old_gui.backend.registration import registration


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Declare variables
        self.input_folder_path = None
        self.output_folder_path = None
        self.npz_file_path = None

        # Start Application Window
        self.master = master
        self.master.title("Photo Registration GUI")

        words = [
            "Welcome to the Photo Registration GUI",
            "!!! Instructions !!!",
            "1. Select the path to the calibration output file",
            "2. Select the directory where the input images are",
            "3. Select the directory where you want the output images saved",
            "4. Click on Perform Calibration and wait until the program quits automatically",
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

        canvas_width, canvas_height = 700, 200
        set_root_position(self.master, canvas_width, canvas_height)

        # Create canvas for widgets
        self.canvas2 = Canvas(self.master, width=canvas_width, height=canvas_height)
        self.canvas2.pack()

        # Specify calibration file
        npz_lbl = Label(
            self.master,
            text="Upload the calibration file (*.npz file)",
            font=("Cambria", 10),
        )
        self.canvas2.create_window(10, 15, anchor=tk.W, window=npz_lbl)

        npz_btn = Button(
            self.master,
            text="Choose File",
            font=("Cambria", 10, "bold"),
            command=self.open_npz_file,
        )
        self.canvas2.create_window(500, 15, anchor=tk.W, window=npz_btn)

        self.npz_lbl_val = Label(self.master, text="-", fg="red", font=("Cambria", 10))
        self.canvas2.create_window(10, 30, anchor=tk.W, window=self.npz_lbl_val)

        # Specify input images directory
        input_lbl = Label(
            self.master,
            text="Select the input directory for uncorrected images ",
            font=("Cambria", 10),
        )
        self.canvas2.create_window(10, 55, anchor=tk.W, window=input_lbl)

        input_lbl_btn = Button(
            self.master,
            text="Choose Folder ",
            font=("Cambria", 10, "bold"),
            command=self.open_input_folder,
        )
        self.canvas2.create_window(500, 55, anchor=tk.W, window=input_lbl_btn)

        self.input_lbl_val = Label(
            self.master, text="-", fg="red", font=("Cambria", 10)
        )
        self.canvas2.create_window(10, 70, anchor=tk.W, window=self.input_lbl_val)

        # Specify directory to store corrected images
        output_lbl = Label(
            self.master,
            font=("Cambria", 10),
            text="Select the output directory for corrected images \n (must already exist)",
        )
        self.canvas2.create_window(10, 100, anchor=tk.W, window=output_lbl)

        output_lbl_btn = Button(
            self.master,
            text="Choose Folder ",
            font=("Cambria", 10, "bold"),
            command=self.open_output_folder,
        )
        self.canvas2.create_window(500, 100, anchor=tk.W, window=output_lbl_btn)

        self.output_lbl_val = Label(
            self.master, text="-", fg="red", font=("Cambria", 10)
        )
        self.canvas2.create_window(10, 120, anchor=tk.W, window=self.output_lbl_val)

        upld = Button(
            self.master,
            text="Register Images",
            bg="brown",
            fg="white",
            command=self.performRegistration,
        )
        self.canvas2.create_window(350, 160, anchor=tk.CENTER, window=upld)

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

    def open_npz_file(self):
        """File open dialog to choose the calibration file"""
        self.npz_file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.npz")]
        )
        self.npz_lbl_val["text"] = self.npz_file_path

    def open_input_folder(self):
        """Input directory selection"""
        self.input_folder_path = filedialog.askdirectory()
        self.input_lbl_val["text"] = self.input_folder_path

    def open_output_folder(self):
        """Output directory selection"""
        self.output_folder_path = filedialog.askdirectory()
        self.output_lbl_val["text"] = self.output_folder_path

    def performRegistration(self):
        """Perform registration and show progress"""
        pb1 = ttk.Progressbar(
            self.master, orient=HORIZONTAL, length=300, mode="determinate"
        )
        pb1.grid(row=5, columnspan=3, pady=10)

        if self.npz_file_path is None:
            messagebox.showwarning("Warning", "Calibration File not Found")

        if self.input_folder_path is None:
            messagebox.showwarning("Warning", "Input Directory Cannot be Empty")

        if self.output_folder_path is None:
            messagebox.showwarning("Warning", "Output Directory Cannot be Empty")

        # Read data from model file
        variables = np.load(self.npz_file_path, allow_pickle=True)
        true_width = variables["true_w"].astype("float")
        true_height = variables["true_h"].astype("float")
        template = variables["img_template"]
        kp_template_tmp = variables["kp_template"]
        des_template = variables["des_template"]
        centers = variables["centers"]

        # reassemble the key points (which we split for saving to disk)
        kp_template = []
        for point in kp_template_tmp:
            temp = cv2.KeyPoint(
                x=point[0][0],
                y=point[0][1],
                size=point[1],
                angle=point[2],
                response=point[3],
                octave=point[4],
                class_id=point[5],
            )
            kp_template.append(temp)

        input_images = sorted(glob.glob(os.path.join(self.input_folder_path, "*.*")))

        for input_image in input_images:
            self.master.update_idletasks()
            pb1["value"] += 100 / len(input_images)
            try:
                registration(
                    true_width,
                    true_height,
                    template,
                    des_template,
                    centers,
                    kp_template,
                    input_image,
                    self.output_folder_path,
                    self.horizontal_ruler,
                    self.vertical_ruler,
                )
            except:
                print(f"failed on {input_image}")
        pb1.destroy()

        Label(
            self.master, text="Performed Registration Successfully!", foreground="green"
        ).grid(row=5, columnspan=3, pady=10)

        # close gui
        # self.master.quit()
        self.master.destroy()


if __name__ == "__main__":
    app = Application(Tk())
    app.mainloop()
