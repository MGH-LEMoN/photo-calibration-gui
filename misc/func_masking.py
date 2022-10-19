import os
import re
import sys
from argparse import ArgumentParser, ArgumentTypeError

import cv2
import numpy as np
from skimage.io import imread
from skimage.measure import label as bwlabel


def chunkwise(t, size=2):
    it = iter(t)
    return list(zip(*[it] * size))


def dir_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise NotADirectoryError(string)


def coords(s):
    seps = r"[;.]"
    try:
        situp = []
        for si in re.split(seps, s):
            situp.append(tuple(map(float, si.split(","))))
        return situp
    except:
        raise ArgumentTypeError(
            "Coordinates must be given divided by commas and space, dot, or semicolon e.g.: 'x,y k,l,'"
        )


def create_mask(args):

    args.scale_down_factor_screen = 1

    for idx, rect_coords in enumerate(args.rect_list):
        args.rect_list[idx] = np.array(
            np.array(rect_coords) // args.scale_down_factor_screen,
            dtype="int",
        )

    # Open image
    image = imread(args.current_image)

    # Open mask
    mask = imread(args.current_mask, as_gray=True)
    mask = mask > np.max(mask) / 2

    # Create connected components
    connected_components = bwlabel(mask)

    # check with E about this
    masked_image = image * mask[:, :, np.newaxis]

    binary_mask = np.zeros(args.img_fullres[0])
    for idx, rectangle in enumerate(args.rect_list, 1):
        # Find all unique indices of label image inside rectangle (> 0)
        x1, y1, x2, y2 = rectangle

        if x1 > x2:
            x1, x2 = x2, x1

        if y1 > y2:
            y1, y2 = y2, y1

        # create binary mask with all regions of label image wtih such indices
        unique = np.unique(connected_components[y1:y2, x1:x2])
        unique = unique[unique > 0]

        for val in unique:
            binary_mask[connected_components == val] = idx

    input_path, _ = os.path.splitext(args.current_image)
    _, input_name = os.path.split(input_path)
    args.output_mask = input_name + "_mask"

    np.save(os.path.join(args.output_folder, args.output_mask), binary_mask)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--rectangle_list",
        help="Coordinate",
        dest="pos_tuple",
        type=coords,
        nargs="?",
    )
    parser.add_argument(
        "--img_fullres", type=coords, dest="img_fullres", default=None
    )
    parser.add_argument(
        "--current_image", type=dir_path, dest="current_image", default=None
    )
    parser.add_argument(
        "--current_mask", type=dir_path, dest="current_mask", default=None
    )

    # If running the code in debug mode
    gettrace = getattr(sys, "gettrace", None)

    if gettrace():
        sys.argv = [
            "func_masking.py",
            "--rectangle_list",
            "1, 2; 3, 4; 5, 6; 7, 8",
            "--img_fullres",
            "100, 100",
            "--current_image",
            "/cluster/vive/MGH_photo_recon/2604_whole/deformed/2604.01_deformed.JPG",
            "--current_mask",
            "/cluster/vive/MGH_photo_recon/2604_whole/masked/2604.01_deformed_masked.png",
        ]

    args = parser.parse_args()

    create_mask(args)

    # example call:
    # fspython func_masking.py --rectangle_list 1, 2; 3, 4; 5, 6; 7, 8 --img_fullres 100, 100 --current_image /cluster/vive/MGH_photo_recon/2604_whole/deformed/2604.01_deformed.JPG --current_mask /cluster/vive/MGH_photo_recon/2604_whole/masked/2604.01_deformed_masked.png
