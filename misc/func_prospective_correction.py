import argparse
import glob
import os
import sys

import cv2
import numpy as np

from registration import registration


def prospective_correction(args):
    """Perform registration and show progress"""
    npz_file_path = args.npz_file
    input_folder_path = args.in_dir
    output_folder_path = args.out_dir

    if not os.path.isfile(args.npz_file):
        raise Exception("Warning", "Calibration File not Found")

    if not os.path.isdir(input_folder_path):
        raise Exception("Warning", "Input Directory Cannot be Empty")

    if not os.path.isdir(output_folder_path):
        raise Exception("Warning", "Output Directory Cannot be Empty")

    # Read data from model file
    variables = np.load(npz_file_path, allow_pickle=True)
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

    input_images = sorted(glob.glob(os.path.join(input_folder_path, "*.*")))

    horizontal_ruler = cv2.imread("./resources/horizontal.png")
    vertical_ruler = cv2.imread("./resources/vertical.png")

    for input_image in input_images:
        try:
            registration(
                true_width,
                true_height,
                template,
                des_template,
                centers,
                kp_template,
                input_image,
                output_folder_path,
                horizontal_ruler,
                vertical_ruler,
            )
        except:
            print(f"failed on {input_image}")

    print("Performed Registration Successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--in_dir", type=str, dest="in_dir", default=None)
    parser.add_argument(
        "--calibration_file", type=str, dest="npz_file", default=None
    )
    parser.add_argument("--out_dir", type=str, dest="out_dir", default=None)

    # If running the code in debug mode
    gettrace = getattr(sys, "gettrace", None)

    if gettrace():
        sys.argv = [
            "func_retrospective_correction.py",
            "--in_img",
            "/space/calico/1/users/Harsha/photo-calibration-gui/misc/prospective_correction_input/",
            "--calibration_file",
            "/space/calico/1/users/Harsha/photo-calibration-gui/misc/calibration.npz",
            "--out_dir",
            "/space/calico/1/users/Harsha/photo-calibration-gui/misc/prospective_correction_output/",
        ]

    args = parser.parse_args()

    prospective_correction(args)

    # example call:
    # fspython func_prospective_correction.py \
    #   --in_img /space/calico/1/users/Harsha/photo-calibration-gui/misc/prospective_correction_input/ \
    #   --calibration_file /space/calico/1/users/Harsha/photo-calibration-gui/misc/cal_output/output_npz \
    #   --out_dir /space/calico/1/users/Harsha/photo-calibration-gui/misc/deformed/
