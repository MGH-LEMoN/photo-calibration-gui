import time
from tkinter import *
from tkinter import filedialog, messagebox, ttk

from train_segmentation_model import train_segmentation


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

        # Create canvas for widgets
        self.canvas1 = Canvas(master, width=400, height=350)
        self.canvas1.pack()

        self.label1 = Label(self.master,
                            text='Welcome to the\n Train Segmentation GUI')
        self.label1.config(font=('cambria', 14))
        self.canvas1.create_window(175, 25, window=self.label1)

        self.label_inst = Label(self.master, text='!!! Instructions !!!')
        self.label_inst.config(font=('cambria', 12, 'bold'))
        self.canvas1.create_window(175, 75, window=self.label_inst)

        self.inst_2 = Label(
            master, text='1. Select the directory where the input images are')
        self.inst_2.config(font=('cambria', 10))
        self.canvas1.create_window(175, 90, window=self.inst_2)

        self.inst_3 = Label(
            self.master,
            wraplength=325,
            text=
            '2. Select the directory where you want the output images saved')
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

        # Set window size
        self.master.geometry('600x200')

        # Specify calibration file
        npz_lbl = Label(
            self.master,
            text='Select directory to save output file (*.npy file)',
            font=('Cambria', 10))
        npz_lbl.grid(row=0, column=0, padx=20)

        npz_btn = Button(self.master,
                         text='Choose Folder',
                         font=('Cambria', 10, 'bold'),
                         command=self.open_output_folder)
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
            'Select the output directory for corrected images \n (must already exist)'
        )
        output_lbl.grid(row=2, column=0, padx=20)

        output_lbl_btn = Button(self.master,
                                text='Choose Folder ',
                                font=('Cambria', 10, 'bold'),
                                command=self.open_mask_folder)
        output_lbl_btn.grid(row=2, column=1, padx=20)

        upld = Button(self.master,
                      text='Train Segmentation',
                      bg='brown',
                      fg='white',
                      command=self.pseudo_train_segmentation)
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

    def open_output_folder(self):
        """File open dialog to save the training segmentation output file
        """
        self.output_folder_path = filedialog.askdirectory()

    def open_input_folder(self):
        """Input directory selection
        """
        self.input_folder_path = filedialog.askdirectory()

    def open_mask_folder(self):
        """Output directory selection
        """
        self.mask_folder_path = filedialog.askdirectory()

    def pseudo_train_segmentation(self):
        if train_segmentation(self.input_folder_path, self.mask_folder_path,
                              self.output_folder_path):
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
