################################################################################
# Doll Data Loading
#
# Loads the doll metadata from doll_data.json during initialization.
#
# The JSON file contains:
# - doll_width : Width of the complete doll sprite sheet.
# - doll_height : Height of the complete doll sprite sheet.
# - crop_list : Layer crop coordinates used when extracting assets.
# - count_list : Number of available variants for each layer/category.
#
# Data is loaded at init priority -100 so it is available before any
# image generation, layer setup, or wardrobe screens are initialized.
#
################################################################################

init -100 python:
    import json

    def load_doll_data(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return (
            data["doll_width"],
            data["doll_height"],
            data["crop_list"],
            data["count_list"],
        )

    # Load doll configuration from the image set and unpack it into
    # global variables for easy access throughout the project.
    doll_width, doll_height, CROP_LIST, COUNT_LIST = load_doll_data(
        renpy.loader.transfn("images/doll/doll_data.json")
    )