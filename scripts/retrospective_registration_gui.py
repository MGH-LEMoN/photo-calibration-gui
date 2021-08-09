import glob
import os
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
            master, text='1. Select the directory where the input images are')
        self.inst_1.config(font=('cambria', 10))
        self.canvas1.create_window(175, 90, window=self.inst_1)

        self.inst_2 = Label(
            master, text='2. Select the directory where you want the output images saved')
        self.inst_2.config(font=('cambria', 10))
        self.canvas1.create_window(175, 110, window=self.inst_2)

        self.inst_3 = Label(
            self.master,
            wraplength=325,
            text=
            '3. Click on 4 corners of a rectangle for every image and provide the dimensions in mm')
        self.inst_3.config(font=('cambria', 10))
        self.canvas1.create_window(175, 140, window=self.inst_3)

        self.inst_6 = Label(
            self.master,
            wraplength=325,
            text=
            '4. Click on Register buttom and wait until the program loads the next image'
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
            command=self.performRegistration,
        )
        upld.grid(row=3, columnspan=3, pady=10)

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
        """Perform registration and show progress
        """
        pb1 = ttk.Progressbar(self.master,
                              orient=HORIZONTAL,
                              length=300,
                              mode='determinate')
        pb1.grid(row=5, columnspan=3, pady=10)

        if self.input_folder_path is None:
            messagebox.showwarning("Warning",
                                   "Input Directory Cannot be Empty")

        if self.output_folder_path is None:
            messagebox.showwarning("Warning",
                                   "Output Directory Cannot be Empty")

        # Go over images
        input_images = sorted(
            glob.glob(os.path.join(self.input_folder_path, '*.*')))

        for input_image in input_images:
            self.master.update_idletasks()
            pb1['value'] += 100 / len(input_images)
            global canvas
            global e1
            global e2
            global pos_tuple
            global scale_down_factor_screen
            global img_fullres
            global deformed_image = None
            root = Tk()
            try:

                pos_tuple = []

                # Open image
                img_fullres = Image.open(input_image)
                # get width and height of image
                width, height = img.width, img.height
                # Resize so if fits on screen
                screen_res = 512
                scale_down_factor_screen  = screen_res / np.min(np.array([width, height]))
                new_im_width = int(width * scale_down_factor_screen)
                new_im_height = int(height * scale_down_factor_screen)
                img_screen = img_fullres.resize((new_im_width, new_im_height), Image.ANTIALIAS)
                img_screen = ImageTk.PhotoImage(img_screen)
                # Paint on screen

                canvas = Canvas(height=new_im_height, width=new_im_width)
                canvas.image = img_screen
                canvas.create_image(0, 0, anchor='nw', image=img_screen)
                canvas.pack()

                frame = Frame(root)
                frame.pack()

                w = Label(frame, text="Width: ", font=('Cambria', 10, 'bold'))
                e1 = Entry(frame, width=10)

                w.pack(side=LEFT)
                e1.pack(side=LEFT)

                h = Label(frame, text="Height: ", font=('Cambria', 10, 'bold'))
                e2 = Entry(frame, width=10)

                h.pack(side=LEFT)
                e2.pack(side=LEFT)

                calibFrame = Frame(root)
                b1 = Button(calibFrame,
                            text='Perform Registration',
                            command=perform_registration,
                            bg='brown',
                            fg='white',
                            font=('cambria', 9, 'bold'))
                calibFrame.pack(side=BOTTOM)
                b1.pack()

                canvas.bind("<Button-1>", click)

                cv2.imwrite(output_image, cv2.cvtColor(deformed_image, cv2.COLOR_RGB2BGR))

            except:
                print(f'failed on {input_image}')

        pb1.destroy()

        Label(self.master,
              text='Performed Registration Successfully!',
              foreground='green').grid(row=5, columnspan=3, pady=10)

        # close gui
        # self.master.quit()
        self.master.destroy()

def perform_registration():
    """This function performs the registration and close the GUI automatically
    """
    global root
    true_width = e1.get()
    true_height = e2.get()

    centers_target = np.array(pos_tuple) / scale_down_factor_screen

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
    deformed_image = cv2.warpPerspective(img_fullres, M2,
                                         (ref_coords[1, 0, 0].astype(int) + 1,
                                          ref_coords[2, 0, 1].astype(int) + 1))


def click(event):
    """Replacement mouse handler inside Canvas, draws a blue ball on each click"""

    # Save the coordinates to a list
    print("Canvas: mouse clicked at ", event.x, event.y)
    pos_tuple.append([event.x , event.y ])

    # Place a blue dot at every click of mouse
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, outline='blue', fill='blue', width=5)




if __name__ == '__main__':
    app = Application(Tk())
    app.mainloop()
