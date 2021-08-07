import glob
import os
import time
from tkinter import *
from tkinter import filedialog, ttk

import cv2
import numpy as np


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Photo Registration GUI')

        # Create canvas for widgets
        self.canvas1 = Canvas(master, width=400, height=350)
        self.canvas1.pack()

        self.label1 = Label(master,
                            text='Welcome to the\n Photo Registration GUI')
        self.label1.config(font=('cambria', 14))
        self.canvas1.create_window(175, 25, window=self.label1)

        self.label_inst = Label(master, text='!!! Instructions !!!')
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
            master,
            wraplength=325,
            text=
            '3. Select the directory where you want the output images saved')
        self.inst_3.config(font=('cambria', 10))
        self.canvas1.create_window(175, 140, window=self.inst_3)

        self.inst_6 = Label(
            master,
            wraplength=325,
            text=
            '6. Click on Perform Calibration and wait until the program quits automatically'
        )
        self.inst_6.config(font=('cambria', 10))
        self.canvas1.create_window(175, 220, window=self.inst_6)

        self.btn = Button(text='Click to Start',
                          command=self.showimage,
                          bg='brown',
                          fg='white',
                          font=('cambria', 9, 'bold'))
        self.canvas1.create_window(175, 275, window=self.btn)

        # self.button.pack()
        self.value = None
        # self.after(3000, self.getvalue)

    def getvalue(self):
        self.value = "haha"

    def printvalue(self):
        print(self.value)

    def showimage(self):
        # Clear canvas for the next screen
        self.clearFrame(self.canvas1)

        self.master.geometry('600x200')
        root = self.master

        npz_lbl = Label(root,
                        text='Upload the calibration file (*.npz file)',
                        font=('Cambria', 10))
        npz_lbl.grid(row=0, column=0, padx=20)

        npz_btn = Button(root,
                         text='Choose File',
                         font=('Cambria', 10, 'bold'),
                         command=self.open_npz_file)
        npz_btn.grid(row=0, column=1, padx=20)

        input_lbl = Label(
            root,
            text='Select the input directory for corrected images ',
            font=('Cambria', 10))
        input_lbl.grid(row=1, column=0, padx=20)

        input_lbl_btn = Button(root,
                               text='Choose Folder ',
                               font=('Cambria', 10, 'bold'),
                               command=self.open_input_folder)
        input_lbl_btn.grid(row=1, column=1, padx=20)

        output_lbl = Label(
            root,
            font=('Cambria', 10),
            text='Select the output directory for corrected images ')
        output_lbl.grid(row=2, column=0, padx=20)

        output_lbl_btn = Button(root,
                                text='Choose Folder ',
                                font=('Cambria', 10, 'bold'),
                                command=self.open_output_folder)
        output_lbl_btn.grid(row=2, column=1, padx=20)

        upld = Button(
            root,
            text='Upload Files',
            command=self.uploadFiles,
        )
        upld.grid(row=4, columnspan=3, pady=10)

    def clearFrame(self, frame):
        # destroy all widgets from frame
        for widget in frame.winfo_children():
            widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        frame.pack_forget()

    def open_npz_file(self):
        self.npz_file_path = filedialog.askopenfilename(
            filetypes=[('Image Files', '*.npz')])

    def open_input_folder(self):
        self.input_folder_path = filedialog.askdirectory()

    def open_output_folder(self):
        self.output_folder_path = filedialog.askdirectory()

    def uploadFiles(self):
        root = self.master
        pb1 = ttk.Progressbar(root,
                              orient=HORIZONTAL,
                              length=300,
                              mode='determinate')
        pb1.grid(row=5, columnspan=3, pady=10)

        input_images = sorted(
            glob.glob(os.path.join(self.input_folder_path, '*.*')))

        for input_image in input_images:
            root.update_idletasks()
            pb1['value'] += 100 / len(input_images)
            try:
                self.registration(self.npz_file_path, input_image,
                                  self.output_folder_path)
            except:
                print(f'failed on {input_image}')
            time.sleep(1)
        pb1.destroy()

        Label(root, text='File Uploaded Successfully!',
              foreground='green').grid(row=5, columnspan=3, pady=10)

        # close gui
        root.quit()
        root.destroy()  # this solves the problem in Eugenio's linux machine...

    def registration(self, model_file, input_image, output_dir):
        # Constants
        DEBUG = True
        sift_res = 1024  # resolution at which SIFT operates;  TODO: make consistent with that of main.py
        reference_pixel_size = 0.1  # resolution of the final, perspective corrected image (in mm)

        # def registration(centers, radii, true_width, true_height, template_path):

        # TODO: get these file names with a GUI (possibly a directory, looping over images in the directory)
        # model_file = '/tmp/model.npz'
        # input_image = './data/test.jpg'
        # output_image = '/tmp/perspective_corrected.jpg'

        input_path, input_ext = os.path.splitext(input_image)
        _, input_name = os.path.split(input_path)
        output_image = input_name + '_corrected' + input_ext

        output_image = os.path.join(output_dir, output_image)

        # assert isinstance(centers, np.ndarray)
        # assert isinstance(radii, np.ndarray)
        # assert isinstance(true_width, float)
        # assert isinstance(true_height, float)
        # assert isinstance(template_path, str)

        # Read data from model file
        variables = np.load(model_file, allow_pickle=True)
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

        # Read in new image to process
        target = cv2.imread(input_image, cv2.IMREAD_GRAYSCALE)
        target_fullsize_rgb = cv2.imread(input_image)

        # Resize image so smaller dimension is sift_res
        factor = sift_res / np.min(target.shape)
        new_target_size = np.round(np.flip(target.shape) * factor).astype(int)
        target = cv2.resize(target,
                            dsize=new_target_size,
                            interpolation=cv2.INTER_AREA)

        # Detect keypoints with SIFT
        sift = cv2.SIFT_create()
        kp_target, des_target = sift.detectAndCompute(target, None)

        if DEBUG:

            import matplotlib.pyplot as plt

            kp_im_template = template.copy()
            kp_im_template = cv2.drawKeypoints(
                template,
                kp_template,
                kp_im_template,
                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            kp_im_target = target.copy()
            kp_im_target = cv2.drawKeypoints(
                target,
                kp_target,
                kp_im_target,
                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            plt.figure(), plt.imshow(
                kp_im_template, aspect='equal'), plt.title(
                    'Key points in template image'), plt.show()
            plt.figure(), plt.imshow(kp_im_target, aspect='equal'), plt.title(
                'Key points in target image'), plt.show()

        # Keypoint Matching
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)  # Brute force is fine

        # Match and extract points
        matches = bf.match(des_template, des_target)
        matches = sorted(matches, key=lambda x: x.distance)
        template_pts = np.float32(
            [kp_template[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        target_pts = np.float32([kp_target[m.trainIdx].pt
                                 for m in matches]).reshape(-1, 1, 2)

        # Fit transform and apply to corner
        M, _ = cv2.findHomography(template_pts, target_pts, cv2.RANSAC, 5.0)
        centers_target = cv2.perspectiveTransform(centers.reshape(-1, 1, 2), M)

        if DEBUG:
            img = cv2.drawMatches(
                template,
                kp_template,
                target,
                kp_target,
                matches,
                None,
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            plt.figure(), plt.imshow(
                img,
                aspect='equal'), plt.title('Matching key points'), plt.show()
            img = cv2.polylines(target, [np.int32(centers_target)], True, 55,
                                3, cv2.LINE_AA)
            plt.figure(), plt.imshow(
                img,
                aspect='equal'), plt.title('Detected corners'), plt.show()

        # Now that we have detected the centers of the corners, we go back to the original coordinates
        centers_target = centers_target / factor
        target = target_fullsize_rgb

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
        deformed_image = cv2.warpPerspective(
            target, M2, (ref_coords[1, 0, 0].astype(int) + 1,
                         ref_coords[2, 0, 1].astype(int) + 1))

        cv2.imwrite(output_image,
                    cv2.cvtColor(deformed_image, cv2.COLOR_RGB2BGR))

        if DEBUG:
            plt.figure(), plt.imshow(
                deformed_image, aspect='equal'), plt.title(
                    'Perspective / pixel size corrected image'), plt.show()


if __name__ == '__main__':
    app = Application(Tk())
    app.mainloop()
