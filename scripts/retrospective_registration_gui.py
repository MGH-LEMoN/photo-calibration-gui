import glob
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from registration import registration


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Declare variables
        self.input_folder_path = None
        self.output_folder_path = None

        self.true_width = None
        self.true_height = None
        self.scale_down_factor_screen = None
        self.pos_tuple = None

        # Staer Application Window
        self.master = master
        self.master.title('Retrospective photo Registration GUI')

        # Create canvas for widgets
        self.canvas1 = Canvas(master, width=400, height=350)
        self.canvas1.pack()

        self.label1 = Label(self.master,
                            text='Welcome to the *retrospective*\n Photo Registration GUI')
        self.label1.config(font=('cambria', 14))
        self.canvas1.create_window(175, 25, window=self.label1)

        self.label_inst = Label(self.master, text='!!! Instructions !!!')
        self.label_inst.config(font=('cambria', 12, 'bold'))
        self.canvas1.create_window(175, 75, window=self.label_inst)

        self.inst_1 = Label(
            master, text='1. Select the directory \n where the input images are')
        self.inst_1.config(font=('cambria', 10))
        self.canvas1.create_window(175, 100, window=self.inst_1)

        self.inst_2 = Label(
            master, text='2. Select the directory where \n you want the output images saved')
        self.inst_2.config(font=('cambria', 10))
        self.canvas1.create_window(175, 135, window=self.inst_2)

        self.inst_3 = Label(
            self.master,
            wraplength=325,
            text=
            '3. Click on 4 corners of a rectangle \n for every image and \n provide the dimensions in mm')
        self.inst_3.config(font=('cambria', 10))
        self.canvas1.create_window(175, 175, window=self.inst_3)

        self.inst_6 = Label(
            self.master,
            wraplength=325,
            text=
            '4. Click on Register buttom and \n wait until the program loads the next image'
        )
        self.inst_6.config(font=('cambria', 10))
        self.canvas1.create_window(175, 225, window=self.inst_6)

        self.btn = Button(text='Click to Start',
                          command=self.fileUploadWindow_new,
                          bg='brown',
                          fg='white',
                          font=('cambria', 9, 'bold'))
        self.canvas1.create_window(175, 275, window=self.btn)

    def fileUploadWindow(self):
        """Contains code to generate the second window in the application
        """
        # Clear canvas for the next screen
        self.clearFrame(self.canvas1)

        # Set window size
        self.master.geometry('600x200')

        # Specify input images directory
        input_lbl = Label(
            self.master,
            text='Select the input directory for uncorrected images ',
            font=('Cambria', 10))
        input_lbl.grid(row=0, column=0, padx=20)

        input_lbl_btn = Button(self.master,
                               text='Choose Folder ',
                               font=('Cambria', 10, 'bold'),
                               command=self.open_input_folder)
        input_lbl_btn.grid(row=0, column=1, padx=20)

        # Specify directory to store corrected images
        output_lbl = Label(
            self.master,
            font=('Cambria', 10),
            text='Select the output directory for corrected images (must already exist)')
        output_lbl.grid(row=1, column=0, padx=20)

        output_lbl_btn = Button(self.master,
                                text='Choose Folder ',
                                font=('Cambria', 10, 'bold'),
                                command=self.open_output_folder)
        output_lbl_btn.grid(row=1, column=1, padx=20)

        upld = Button(
            self.master,
            text='Register Images',
            bg='brown',
            fg='white',
            command=self.performRegistration1,
        )
        upld.grid(row=3, columnspan=3, pady=10)


    def fileUploadWindow_new(self):
        """Contains code to generate the second window in the application
        """
        # Clear canvas for the next screen
        self.clearFrame(self.canvas1)

        # Create canvas for widgets
        self.canvas2 = Canvas(self.master, width=600, height=205)
        self.canvas2.pack()

        # Specify input images directory
        input_lbl = Label(
            self.master,
            text='Select the input directory for uncorrected images ',
            font=('Cambria', 10))
        self.canvas2.create_window(10, 10, anchor=tk.NW, window=input_lbl)

        input_lbl_btn = Button(self.master,
                               text='Choose Folder ',
                               font=('Cambria', 10, 'bold'),
                               command=self.open_input_folder)
        self.canvas2.create_window(450, 10, anchor=tk.NW, window=input_lbl_btn)

        # Specify directory to store corrected images
        output_lbl = Label(
            self.master,
            font=('Cambria', 10),
            text='Select the output directory for corrected images \n (must already exist)')
        self.canvas2.create_window(10, 50, anchor=tk.NW, window=output_lbl)

        output_lbl_btn = Button(self.master,
                                text='Choose Folder ',
                                font=('Cambria', 10, 'bold'),
                                command=self.open_output_folder)
        self.canvas2.create_window(450, 50, anchor=tk.NW, window=output_lbl_btn)

        upld_btn = Button(
            self.master,
            text='Register Images',
            bg='brown',
            fg='white',
            command=self.performRegistration,
        )
        self.canvas2.create_window(300, 150, anchor=tk.CENTER, window=upld_btn)

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
        """Input directory selection
        """
        self.input_folder_path = filedialog.askdirectory()

    def open_output_folder(self):
        """Output directory selection
        """
        self.output_folder_path = filedialog.askdirectory()

    def performRegistration(self):

        # Clear canvas for the next screen
        self.clearFrame(self.canvas2)

        # Go over images
        input_images = sorted(
            glob.glob(os.path.join(self.input_folder_path, '*.*')))

        for input_image in input_images:

            input_path, input_ext = os.path.splitext(input_image)
            _, input_name = os.path.split(input_path)
            self.output_image = input_name + '_deformed' + input_ext
            
            self.pos_tuple =[]

            # Open image
            self.img_fullres = Image.open(input_image)

            # get width and height of image
            width, height = self.img_fullres.width, self.img_fullres.height

            # Resize so if fits on screen
            screen_res = 256
            self.scale_down_factor_screen = screen_res / np.min(np.array([width, height]))
            
            new_im_width = int(width * self.scale_down_factor_screen)
            new_im_height = int(height * self.scale_down_factor_screen)
            
            img_screen = self.img_fullres.resize((new_im_width, new_im_height), Image.ANTIALIAS)
            img_screen = ImageTk.PhotoImage(img_screen)

            # Paint on screen
            self.canvas3 = Canvas(self.master, height=new_im_height + 100, width=new_im_width)
            self.canvas3.image = img_screen
            self.canvas3.create_image(0, 0, anchor='nw', image=img_screen)
            self.canvas3.pack()

            self.canvas3.update()
            canvas_width = self.canvas3.winfo_width()
            canvas_height = self.canvas3.winfo_height()

            w = Label(self.master, text="Width: ", font=('Cambria', 10, 'bold'))
            self.e1 = Entry(self.master, width=10)
            
            self.canvas3.create_window(canvas_width // 2, canvas_height - 85, anchor=tk.NE, window=w)
            self.canvas3.create_window(canvas_width // 2, canvas_height - 85, anchor=tk.NW, window=self.e1)

            h = Label(self.master, text="Height: ", font=('Cambria', 10, 'bold'))
            self.e2 = Entry(self.master, width=10)
            self.canvas3.create_window(canvas_width // 2, canvas_height - 60, anchor=tk.NE, window=h)
            self.canvas3.create_window(canvas_width // 2, canvas_height - 60, anchor=tk.NW, window=self.e2)

            b1 = Button(self.master,
                        text='Perform Registration',
                        command=self.perform_registration,
                        bg='brown',
                        fg='white',
                        font=('cambria', 9, 'bold'))
            self.canvas3.create_window(canvas_width // 2, canvas_height - 20, anchor=tk.CENTER, window=b1)

            self.canvas3.bind("<Button-1>", self.click)

        # self.master.destroy()

    def perform_registration(self):
        """This function performs the registration and close the GUI automatically
        """
        reference_pixel_size = 0.1

        true_width = float(self.e1.get())
        true_height = float(self.e2.get())

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

        # We compute the final perspective transform
        M2, _ = cv2.findHomography(centers_target_reordered, ref_coords)
        self.deformed_image = cv2.warpPerspective(self.img_fullres, M2,
                                            (ref_coords[1, 0, 0].astype(int) + 1,
                                            ref_coords[2, 0, 1].astype(int) + 1))

        cv2.imwrite(self.output_image, cv2.cvtColor(self.deformed_image, cv2.COLOR_RGB2BGR))
    

    def click(self, event):
        """Replacement mouse handler inside Canvas, draws a blue ball on each click"""

        # Save the coordinates to a list
        print("Canvas: mouse clicked at ", event.x, event.y)
        self.pos_tuple.append([event.x , event.y])

        # Place a blue dot at every click of mouse
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        self.canvas3.create_oval(x1, y1, x2, y2, outline='blue', fill='blue', width=5)


if __name__ == '__main__':
    app = Application(Tk())
    app.mainloop()
