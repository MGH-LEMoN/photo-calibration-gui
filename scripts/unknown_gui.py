import glob
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog

import numpy as np
import skimage
import skimage.io as io
from PIL import Image, ImageTk

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Declare variables
        self.input_folder_path = None
        self.output_folder_path = None
        self.npz_file_path = None

        # Staer Application Window
        self.master = master
        self.master.title('Train Segmentation GUI')

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.x = self.y = 0

        # self.topx = 0
        # self.topy = 0

        # self.botx = 0
        # self.boty = 0

        # self.rect_id = None

        # self.rect_list = list()
        # self.rect_main_data = list()

        # Create canvas for widgets
        self.canvas1 = Canvas(master, width=400, height=350)
        self.canvas1.pack()

        self.label1 = Label(self.master, text='Welcome to the\n Unknown GUI')
        self.label1.config(font=('cambria', 14))
        self.canvas1.create_window(175, 25, window=self.label1)

        self.label_inst = Label(self.master, text='!!! Instructions !!!')
        self.label_inst.config(font=('cambria', 12, 'bold'))
        self.canvas1.create_window(175, 75, window=self.label_inst)

        self.inst_2 = Label(
            master, text='1. Select the directory where the input images are')
        self.inst_2.config(font=('cambria', 10))
        self.canvas1.create_window(175, 90, window=self.inst_2)

        self.inst_3 = Label(self.master,
                            wraplength=325,
                            text='2. Select the directory where the masks are')
        self.inst_3.config(font=('cambria', 10))
        self.canvas1.create_window(175, 110, window=self.inst_3)

        self.inst_1 = Label(master,
                            text='3. Select the path to the output file')
        self.inst_1.config(font=('cambria', 10))
        self.canvas1.create_window(175, 140, window=self.inst_1)

        self.inst_6 = Label(
            self.master,
            wraplength=325,
            text=
            '4. Click on Perform Calibration and wait until the program quits automatically'
        )
        self.inst_6.config(font=('cambria', 10))
        self.canvas1.create_window(175, 220, window=self.inst_6)

        self.btn = Button(text='Click to Start',
                          command=self.fileUploadWindow,
                          bg='brown',
                          fg='white',
                          font=('cambria', 9, 'bold'))
        self.canvas1.create_window(175, 275, window=self.btn)

    def fileUploadWindow(self):
        """Contains code to generate the second window in the application
        """
        # Clear canvas for the next screen
        self.clearFrame(self.canvas1)

        # Create canvas for widgets
        self.canvas2 = Canvas(self.master, width=600, height=300)
        self.canvas2.pack()

        # Specify input images directory
        input_lbl = Label(self.master,
                          text='Select the directory with input images',
                          font=('Cambria', 10))
        self.canvas2.create_window(10, 10, anchor=tk.NW, window=input_lbl)

        input_lbl_btn = Button(self.master,
                               text='Choose Folder ',
                               font=('Cambria', 10, 'bold'),
                               command=self.open_input_folder)
        self.canvas2.create_window(450, 10, anchor=tk.NW, window=input_lbl_btn)

        # Specify directory with masks
        mask_lbl = Label(self.master,
                         font=('Cambria', 10),
                         text='Select the directory with masks')
        self.canvas2.create_window(10, 50, anchor=tk.NW, window=mask_lbl)

        mask_lbl_btn = Button(self.master,
                              text='Choose Folder ',
                              font=('Cambria', 10, 'bold'),
                              command=self.open_mask_folder)
        self.canvas2.create_window(450, 50, anchor=tk.NW, window=mask_lbl_btn)

        # Specify directory to store updates masks
        output_lbl = Label(self.master,
                           font=('Cambria', 10),
                           text='Select the directory to store output masks')
        self.canvas2.create_window(10, 90, anchor=tk.NW, window=output_lbl)

        output_lbl_btn = Button(self.master,
                                text='Choose Folder ',
                                font=('Cambria', 10, 'bold'),
                                command=self.open_output_folder)
        self.canvas2.create_window(450,
                                   90,
                                   anchor=tk.NW,
                                   window=output_lbl_btn)

        upld_btn = Button(self.master,
                          text='Click here',
                          bg='brown',
                          fg='white',
                          command=self.performRegistration)
        self.canvas2.create_window(300, 150, anchor=tk.CENTER, window=upld_btn)

    def performRegistration(self):

        # Clear canvas for the next screen
        self.clearFrame(self.canvas2)

        # Go over images
        input_images = sorted(
            glob.glob(os.path.join(self.input_folder_path, '*.*')))

        # Go over masks
        mask_images = sorted(
            glob.glob(os.path.join(self.mask_folder_path, '*.*')))

        for input_image, mask_image in zip(input_images, mask_images):

            self.current_image = input_image
            self.current_mask = mask_image

            try:
                self.clearFrame(self.canvas3)
            except Exception as e:
                pass

            input_path, input_ext = os.path.splitext(input_image)
            _, input_name = os.path.split(input_path)
            self.output_image = input_name + '_deformed' + input_ext

            # Open image
            # self.img_fullres = Image.open(input_image)
            # Open image
            self.image = skimage.io.imread(input_image)

            # Open mask
            self.mask = skimage.io.imread(mask_image)

            self.mask = self.mask > 128

            # check with E about this
            masked_image = self.image[:,:,0] * self.mask

            # Open mask
            self.img_fullres = Image.fromarray(masked_image)

            # get width and height of image
            width, height = self.img_fullres.width, self.img_fullres.height

            # Resize so it fits on screen
            screen_res = 256
            self.scale_down_factor_screen = screen_res / np.min(
                np.array([width, height]))

            new_im_width = int(width * self.scale_down_factor_screen)
            new_im_height = int(height * self.scale_down_factor_screen)

            img_screen = self.img_fullres.resize((new_im_width, new_im_height),
                                                 Image.ANTIALIAS)
            img_screen = ImageTk.PhotoImage(img_screen)

            # Paint on screen
            self.canvas3 = Canvas(self.master,
                                  height=new_im_height + 100,
                                  width=new_im_width)
            self.canvas3.image = img_screen
            self.canvas3.create_image(0, 0, anchor='nw', image=self.canvas3.image)
            self.canvas3.pack()

            self.topx = 0
            self.topy = 0

            self.botx = 0
            self.boty = 0

            self.rect_id = None

            self.rect_list = list()
            self.rect_main_data = list()

            self.canvas3.update()
            canvas_width = self.canvas3.winfo_width()
            canvas_height = self.canvas3.winfo_height()

            b1 = Button(self.master,
                        text='Perform Registration',
                        command=self.perform_registration,
                        bg='brown',
                        fg='white',
                        font=('cambria', 9, 'bold'))
            self.canvas3.create_window(canvas_width // 2,
                                       canvas_height - 20,
                                       anchor=tk.CENTER,
                                       window=b1)

            self.rect_id = self.canvas3.create_rectangle(self.topx, self.topy, self.topx, self.topy, dash=(2,2), fill='', outline='red')

            self.canvas3.bind('<Button-1>', self.get_mouse_posn)
            self.canvas3.bind('<B1-Motion>', self.update_sel_rect)
            self.canvas3.bind('<ButtonRelease-1>', self.draw_rect)
            self.canvas3.bind('<Double-3>', self.onClear) 

            self.canvas3.update()

        self.master.destroy()


    def perform_registration(self):
        print(self.rect_list)

        for idx, rect_coords in enumerate(self.rect_list):
            self.rect_list[idx] = np.array(np.array(rect_coords) // self.scale_down_factor_screen, dtype='int')

        print(self.rect_list)

        binary_mask = np.zeros_like(self.image)
        # for every rectangle: # assuming a single channel
        for idx, rectangle in enumerate(self.rect_list, 1):

            # Find all unique indices of label image inside rectangle (> 0)
            x1, y1, x2, y2 = rectangle
            # rectangle_image = self.image[y1:y2, x1:x2]
            # uniq_idxs = rectangle_image[rectangle_image > 0]

            # create binary mask with all regions of label image wtih such indices
            binary_mask[y1:y2+1, x1:x2+1] = idx

            # set pixesl of mask to r in result
            am = np.ma.masked_where(self.image > 0, self.image)

            binary_mask = binary_mask * am.mask

        np.save(os.path.join(self.output_folder_path, 'some_mask.npy'), binary_mask)


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

    def open_output_folder(self):
        """File open dialog to save the training segmentation output file
        """
        self.output_folder_path = filedialog.askdirectory()

    def open_input_folder(self):
        """Input directory selection
        """
        self.input_folder_path = filedialog.askdirectory()

    def open_mask_folder(self):
        """Input directory selection
        """
        self.mask_folder_path = filedialog.askdirectory()

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas3.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)  # Update selection rect.

    def draw_rect(self, event):
        draw_data = self.canvas3.create_rectangle(self.topx, self.topy, self.botx, self.boty, outline="green", fill="")
        self.rect_list.append((self.topx, self.topy, self.botx, self.boty))
        self.rect_main_data.append(draw_data)

    def onClear(self, event):
        # event.widget.delete('all')

        if (len(self.rect_main_data) > 0):
            for rect in self.rect_main_data:
                self.canvas3.delete(rect)
        
        self.rect_main_data.clear()
        self.rect_list.clear()
       
        self.topx = 0
        self.topy = 0

        self.botx = 0
        self.boty = 0

        self.canvas3.create_image(0, 0, anchor='nw', image=self.canvas3.image)
        self.rect_id = self.canvas3.create_rectangle(self.topx, self.topy, self.topx, self.topy, dash=(2,2), fill='', outline='red')
        
    def pseudo_apply_segmentation(self):
        if apply_segmentation(self.input_folder_path, self.output_folder_path,
                              self.npy_file_path):
            npz_lbl = Label(
                self.master,
                text='Training Successful!! \n Window will close in 5 seconds',
                font=('Cambria', 10),
                fg='green')
            npz_lbl.grid(row=5, columnspan=3, padx=20)

            time.sleep(2)
            self.master.destroy()
        else:
            npz_lbl = Label(self.master,
                            text='Training Failed!!!\n Please check',
                            font=('Cambria', 10),
                            fg='red')
            npz_lbl.grid(row=5, columnspan=3, padx=10)


if __name__ == '__main__':
    app = Application(Tk())
    app.mainloop()
