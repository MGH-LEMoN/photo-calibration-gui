import glob
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np

from registration import registration


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Declare variables
        self.input_folder_path = None
        self.output_folder_path = None
        self.npz_file_path = None

        # Staer Application Window
        self.master = master
        self.master.title('Photo Registration GUI')

        # Create canvas for widgets
        self.canvas1 = Canvas(master, width=400, height=350)
        self.canvas1.pack()

        self.label1 = Label(self.master,
                            text='Welcome to the\n Photo Registration GUI')
        self.label1.config(font=('cambria', 14))
        self.canvas1.create_window(175, 25, window=self.label1)

        self.label_inst = Label(self.master, text='!!! Instructions !!!')
        self.label_inst.config(font=('cambria', 12, 'bold'))
        self.canvas1.create_window(175, 75, window=self.label_inst)

        self.inst_1 = Label(
            master, text='1. Select the path to the calibration output file')
        self.inst_1.config(font=('cambria', 10))
        self.canvas1.create_window(175, 90, window=self.inst_1)

        self.inst_2 = Label(
            master, text='2. Select the directory where the input images are')
        self.inst_2.config(font=('cambria', 10))
        self.canvas1.create_window(175, 110, window=self.inst_2)

        self.inst_3 = Label(
            self.master,
            wraplength=325,
            text=
            '3. Select the directory where you want the output images saved')
        self.inst_3.config(font=('cambria', 10))
        self.canvas1.create_window(175, 140, window=self.inst_3)

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

        # Set window size
        self.master.geometry('600x200')

        # Specify calibration file
        npz_lbl = Label(self.master,
                        text='Upload the calibration file (*.npz file)',
                        font=('Cambria', 10))
        npz_lbl.grid(row=0, column=0, padx=20)

        npz_btn = Button(self.master,
                         text='Choose File',
                         font=('Cambria', 10, 'bold'),
                         command=self.open_npz_file)
        npz_btn.grid(row=0, column=1, padx=20)

        # Specify input images directory
        input_lbl = Label(
            self.master,
            text='Select the input directory for uncorrected images ',
            font=('Cambria', 10))
        input_lbl.grid(row=1, column=0, padx=20)

        input_lbl_btn = Button(self.master,
                               text='Choose Folder ',
                               font=('Cambria', 10, 'bold'),
                               command=self.open_input_folder)
        input_lbl_btn.grid(row=1, column=1, padx=20)

        # Specify directory to store corrected images
        output_lbl = Label(
            self.master,
            font=('Cambria', 10),
            text=
            'Select the output directory for corrected images (must already exist)'
        )
        output_lbl.grid(row=2, column=0, padx=20)

        output_lbl_btn = Button(self.master,
                                text='Choose Folder ',
                                font=('Cambria', 10, 'bold'),
                                command=self.open_output_folder)
        output_lbl_btn.grid(row=2, column=1, padx=20)

        upld = Button(
            self.master,
            text='Register Images',
            bg='brown',
            fg='white',
            command=self.performRegistration,
        )
        upld.grid(row=4, columnspan=3, pady=10)

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
        """File open dialog to choose the calibration file
        """
        self.npz_file_path = filedialog.askopenfilename(
            filetypes=[('Image Files', '*.npz')])

    def open_input_folder(self):
        """Input directory selection
        """
        self.input_folder_path = filedialog.askdirectory()

    def open_output_folder(self):
        """Output directory selection
        """
        self.output_folder_path = filedialog.askdirectory()

    def performRegistration(self):
        """Perform registration and show progress
        """
        pb1 = ttk.Progressbar(self.master,
                              orient=HORIZONTAL,
                              length=300,
                              mode='determinate')
        pb1.grid(row=5, columnspan=3, pady=10)

        if self.npz_file_path is None:
            messagebox.showwarning("Warning", "Calibration File not Found")

        if self.input_folder_path is None:
            messagebox.showwarning("Warning",
                                   "Input Directory Cannot be Empty")

        if self.output_folder_path is None:
            messagebox.showwarning("Warning",
                                   "Output Directory Cannot be Empty")

        # Read data from model file
        variables = np.load(self.npz_file_path, allow_pickle=True)
        true_width = variables['true_w'].astype('float')
        true_height = variables['true_h'].astype('float')
        template = variables['img_template']
        kp_template_tmp = variables['kp_template']
        des_template = variables['des_template']
        centers = variables['centers']

        # reassemble the key points (which we split for saving to disk)
        kp_template = []
        for point in kp_template_tmp:
            temp = cv2.KeyPoint(x=point[0][0],
                                y=point[0][1],
                                size=point[1],
                                angle=point[2],
                                response=point[3],
                                octave=point[4],
                                class_id=point[5])
            kp_template.append(temp)

        input_images = sorted(
            glob.glob(os.path.join(self.input_folder_path, '*.*')))

        for input_image in input_images:
            self.master.update_idletasks()
            pb1['value'] += 100 / len(input_images)
            try:
                # registration(self.npz_file_path, input_image,
                #              self.output_folder_path)
                registration(true_width, true_height, template, des_template,
                             centers, kp_template, input_image,
                             self.output_folder_path)
            except:
                print(f'failed on {input_image}')
        pb1.destroy()

        Label(self.master,
              text='Performed Registration Successfully!',
              foreground='green').grid(row=5, columnspan=3, pady=10)

        # close gui
        # self.master.quit()
        self.master.destroy()


if __name__ == '__main__':
    app = Application(Tk())
    app.mainloop()
