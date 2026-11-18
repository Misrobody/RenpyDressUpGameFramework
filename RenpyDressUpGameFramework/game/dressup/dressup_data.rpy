################################################################################
# Doll Data Loading
#
# Loads all the doll metadata from doll_data.json and doll_category_data.
#
# The doll_data.json file contains:
# - doll_width : Width of the complete doll sprite sheet.
# - doll_height : Height of the complete doll sprite sheet.
# - crop_list : Layer crop coordinates used when extracting assets.
# - count_list : Number of available variants for each layer/category.
# This file is not meant to be edited by the user.

# The doll_category_data file contains:
# - channels : defines the order in which the red, green, blue and gray
#   channels are interpreted. The fixed framework mapping is:
#       * unmutable color.
#       * mutable color 1.
#       * mutable color 2.
#       * mutable color 3.
# - skin_layer : the category key containing the skin.
# - default_category : the default selected category key.
# - default_group : the default selected category group.
# - category_config : the config details for each category.
#   A category key has two suppliable parameters:
#       * base_index : if provided, the index of the preselected item.
#       * manager : the color manager used by the category.
#         Please see the ColorManager.rpy file for more details.
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

    def load_doll_category_data(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return (
            data["globals"]["channels"],
            data["globals"]["skin_layer"],
            data["globals"]["default_category"],
            data["globals"]["default_group"],
            data["category_config"]
        )
   
    # Load doll configuration from the image set and unpack it into
    # global variables for easy access throughout the project.
    doll_width, doll_height, CROP_LIST, COUNT_LIST = load_doll_data(
        renpy.loader.transfn(f"{IMAGESET_PATH}/doll_data.json")
    )

    print(COUNT_LIST)

    CHANNELS, SKIN_LAYER, DEFAULT_CATEGORY_KEY, DEFAULT_GROUPS_KEY, CATEGORY_CONFIG = load_doll_category_data(
        renpy.loader.transfn(f"{IMAGESET_PATH}/doll_category_data.json")
    )  