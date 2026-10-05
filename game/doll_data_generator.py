#!/usr/bin/env python3

import os, sys, json

from array import array
from collections import defaultdict
from PIL import Image

######################################################################################
### Functions
######################################################################################


def count_png_files(directory):
    png_count = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".png"):
                png_count += 1

    return png_count


def get_png_count_list(root_dir):
    res = {}

    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            full_dir = os.path.join(root, d)
            res[d] = count_png_files(full_dir)

    return res


def resize_pngs_by_height(root_dir, target_height):
    for subdir, _, files in os.walk(root_dir):
        for file in files:

            if not file.lower().endswith(".png"):
                continue

            path = os.path.join(subdir, file)

            try:
                with Image.open(path) as image:

                    width, height = image.size

                    aspect_ratio = width / height
                    new_width = int(target_height * aspect_ratio)

                    resized = image.resize(
                        (new_width, target_height),
                        Image.Resampling.LANCZOS
                    )

                    resized.save(path)

                    print(
                        f"Resized: {path} -> "
                        f"{new_width}x{target_height}"
                    )

            except Exception as e:
                print(f"Error processing {path}: {e}")


def get_doll_size(rootdir):
    for subdir, _, files in os.walk(rootdir):
        for file in files:

            if file.lower().endswith(".png"):

                path = os.path.join(subdir, file)

                with Image.open(path) as image:
                    return image.size

    raise RuntimeError("No PNG files found")


def get_all_crops(doll_width, doll_height, rootdir):

    comp_x = array('I', [0] * doll_width)
    comp_y = array('I', [0] * doll_height)
    '''
    def get_img_crop(imgpath, step=4):

        image = Image.open(imgpath).convert("RGBA")
        pixels = image.load()

        comp_x[:] = array('I', [0] * doll_width)
        comp_y[:] = array('I', [0] * doll_height)

        for y in range(0, doll_height, step):

            row_sum = 0

            for x in range(0, doll_width, step):

                r, g, b, a = pixels[x, y]

                s = r + g + b + a

                comp_x[x] += s
                row_sum += s

            comp_y[y] += row_sum

        weighted_sum_x = 0
        weighted_sum_y = 0

        total_x = 0
        total_y = 0

        max_len = max(doll_width, doll_height)

        for idx in range(max_len):

            if idx < doll_width:
                val_x = comp_x[idx]
                total_x += val_x
                weighted_sum_x += idx * val_x

            if idx < doll_height:
                val_y = comp_y[idx]
                total_y += val_y
                weighted_sum_y += idx * val_y

        mean_x = weighted_sum_x / total_x if total_x else 0
        mean_y = weighted_sum_y / total_y if total_y else 0

        weighted_dev_x = 0
        weighted_dev_y = 0

        for idx in range(max_len):

            if idx < doll_width:
                val_x = comp_x[idx]
                weighted_dev_x += abs(idx - mean_x) * val_x

            if idx < doll_height:
                val_y = comp_y[idx]
                weighted_dev_y += abs(idx - mean_y) * val_y

        dev_x = weighted_dev_x / total_x if total_x else 0
        dev_y = weighted_dev_y / total_y if total_y else 0

        return (
            int(mean_x),
            int(mean_y),
            int(dev_x),
            int(dev_y)
        )
    '''
    
    def get_img_crop(imgpath):

        image = Image.open(imgpath).convert("RGBA")

        bbox = image.getbbox()

        if bbox is None:
            return (0, 0, 0, 0)

        left, top, right, bottom = bbox

        width = right - left
        height = bottom - top

        mean_x = left + width // 2
        mean_y = top + height // 2

        return (
            mean_x,
            mean_y,
            width,
            height
        )    
         
    results = {}

    for dirpath, dirnames, filenames in os.walk(rootdir):

        for f in filenames:

            if f.lower().endswith(".png"):

                path = os.path.join(dirpath, f)

                results[f] = get_img_crop(path)

    return results

def save_doll_data(filepath, doll_width, doll_height, crop_list, count_list):
    data = {
        "doll_width": doll_width,
        "doll_height": doll_height,
        "crop_list": crop_list,
        "count_list": count_list,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Saved data to {filepath}")

######################################################################################
### The actual processing
######################################################################################


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <image_set_directory>")
    sys.exit(1)

IMGSET_DIR = sys.argv[1]

desired_height = 1080

doll_width, doll_height = get_doll_size(IMGSET_DIR)

if doll_height != desired_height:

    resize_pngs_by_height(
        IMGSET_DIR,
        desired_height
    )

    doll_width, doll_height = get_doll_size(
        IMGSET_DIR
    )

CROP_LIST = get_all_crops(
    doll_width,
    doll_height,
    IMGSET_DIR
)

COUNT_LIST = get_png_count_list(
    IMGSET_DIR
)

save_doll_data(
    IMGSET_DIR + "/doll_data.json",
    doll_width,
    doll_height,
    CROP_LIST,
    COUNT_LIST
)