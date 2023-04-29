"""
This script is called by the freesurfer GUI command- connected_components 
"""
import argparse
import os
import sys
from argparse import ArgumentParser

import numpy as np
from skimage.io import imread
from skimage.measure import label as bwlabel


class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.split(values))

    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    def split(self, s):
        try:
            s = list(map(float, s))
        except:
            s = list(map(float, s[0].split()))

        coords = list(self.chunks(s, 4))
        if len(coords[-1]) != 4:
            print("Invalid coordinates")
            sys.exit()
        return coords


def chunkwise(t, size=2):
    it = iter(t)
    return list(zip(*[it] * size))


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def dir_path(string):
    return string if os.path.isdir(string) else NotADirectoryError(string)


def create_mask(args):
    for idx, rect_coords in enumerate(args.rect_list):
        args.rect_list[idx] = np.array(
            np.array(rect_coords),
            dtype="int",
        )

    # Open image
    image = imread(args.current_image)

    # Open mask
    mask = imread(args.current_mask, as_gray=True)
    mask = mask > np.max(mask) / 2

    # Create connected components
    connected_components = bwlabel(mask)

    binary_mask = np.zeros(image.shape[0:2], dtype="uint8")

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
    out_name = input_name + "_mask"

    np.save(os.path.join(args.out_dir, out_name), binary_mask)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--rectangle_coordinates",
        nargs="+",
        dest="rect_list",
        action=SplitArgs,
    )
    parser.add_argument("--in_img", type=file_path, dest="current_image", default=None)
    parser.add_argument("--in_mask", type=file_path, dest="current_mask", default=None)
    parser.add_argument("--out_dir", type=dir_path, dest="out_dir", default=None)

    # If running the code in debug mode
    gettrace = getattr(sys, "gettrace", None)

    if gettrace():
        sys.argv = [
            "func_connected_components.py",
            "--rectangle_coordinates",
            "431 559 477 602 1131 565 1180 628 1788 572 1841 641",
            "--in_img",
            "/cluster/vive/MGH_photo_recon/2604_whole/deformed/2604.01_deformed.JPG",
            "--in_mask",
            "/cluster/vive/MGH_photo_recon/2604_whole/masked/2604.01_deformed_masked.png",
            "--out_dir",
            "/tmp",
        ]

    args = parser.parse_args()

    create_mask(args)
