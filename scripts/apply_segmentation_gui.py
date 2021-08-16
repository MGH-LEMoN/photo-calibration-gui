import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog

from apply_segmentation_model import apply_segmentation


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Declare variables
        self.input_folder_path = None
        self.output_folder_path = None
        self.npz_file_path = None

        # Start Application Window
        self.master = master
        self.master.title('Train Segmentation GUI')

        words = [
            "Welcome to the Apply Segmentation GUI", '!!! Instructions !!!',
            '1. Select the directory with input images',
            '2. Select the directory where you want the output images saved',
            '3. Select the path to the output file',
            '4. Click on Apply Segmentation and wait until the program quits automatically'
        ]

        canvas_width, canvas_height = 600, 250

        self.canvas1 = Canvas(self.master,
                              width=canvas_width,
                              height=canvas_height)

        word_pos = [(int(canvas_width // 2), 20), (int(canvas_width // 2), 40),
                    (20, 60), (20, 80), (20, 100), (20, 120)]
        word_anchor = [tk.CENTER, tk.CENTER, tk.NW, tk.NW, tk.NW, tk.NW]

        object_id = []
        for word, (x, y), anchor in zip(words, word_pos, word_anchor):
            id = self.canvas1.create_text(x, y, anchor=anchor, text=word)
            object_id.append(id)
        self.canvas1.pack()

        btn = Button(text='Click to Start',
                     command=self.fileUploadWindow,
                     bg='brown',
                     fg='white',
                     font=('cambria', 9, 'bold'),
                     justify='center')
        self.canvas1.create_window(int(canvas_width // 2), 225, window=btn)

        self.canvas1.itemconfigure(1, font=('cambria', 12, 'bold'))
        self.canvas1.itemconfigure(2, font=('cambria', 10))

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
        output_lbl = Label(self.master,
                           font=('Cambria', 10),
                           text='Select the input directory for *.npy file \n')
        output_lbl.grid(row=2, column=0, padx=20)

        output_lbl_btn = Button(self.master,
                                text='Choose Folder ',
                                font=('Cambria', 10, 'bold'),
                                command=self.open_npy_file)
        output_lbl_btn.grid(row=2, column=1, padx=20)

        upld = Button(self.master,
                      text='Apply Segmentation',
                      bg='brown',
                      fg='white',
                      command=self.pseudo_apply_segmentation)
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

    def open_npy_file(self):
        """File open dialog to choose the calibration file
        """
        self.npy_file_path = filedialog.askopenfilename(
            filetypes=[('Image Files', '*.npy')])

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
