## This file contains all the adjustable parameters of the framework

init -200 python:  
    ################################################################################
    # Defaults
    ################################################################################

    # The path to the base directory of the doll imageset. Do not put trailing /
    IMAGESET_PATH = "images/doll_2"

################################################################################
# UI Constants
################################################################################

### Globals

define catalogue = Catalogue()

### Item Grid

init -200 python:
    # Height and width of a single grid item.
    CROP_SIZE = 200

define ITEM_GRID_COLUMNS = 6
define ITEM_GRID_ROWS = max((catalogue.current_stock() + 4) // ITEM_GRID_COLUMNS, 3)
define ITEM_GRID_ITEM_PADDING = 8
define ITEM_GRID_ITEM_SIZE = CROP_SIZE + ITEM_GRID_ITEM_PADDING
define ITEM_GRID_SPACING = 10
define ITEM_GRID_VIEWPORT_HEIGHT = 3 * ITEM_GRID_ITEM_SIZE + 2 * ITEM_GRID_SPACING
define ITEM_GRID_VIEWPORT_WIDTH = ITEM_GRID_COLUMNS * ITEM_GRID_ITEM_SIZE + (ITEM_GRID_COLUMNS - 1) * ITEM_GRID_SPACING

### Category Bar

define CATEGORY_BUTTON_BUTTON_SPACING = -5
define CATEGORY_BUTTON_BAR_SPACING = -4
define CATEGORY_BUTTON_GROUP_NUMBER = len(catalogue.group_keys)
define CATEGORY_BUTTON_WIDTH = ITEM_GRID_VIEWPORT_WIDTH // CATEGORY_BUTTON_GROUP_NUMBER - CATEGORY_BUTTON_BUTTON_SPACING
define CATEGOTY_BUTTON_HEIGHT = 55

### Color Menu

define COLOR_MENU_WIDTH = ITEM_GRID_VIEWPORT_WIDTH
define COLOR_MENU_HEIGHT = 200

### Color Menu Toggle

define COLOR_MENU_TOGGLE_WIDTH = 166
define COLOR_MENU_TOGGLE_HEIGHT = COLOR_MENU_HEIGHT

### Color Buttons

define COLOR_MENU_COLOR_BUTTON_WIDTH = 166
define COLOR_MENU_COLOR_BUTTON_HEIGHT = 70
define COLOR_MENU_BUTTON_SPACING = -5

### Color Swatch

define COLOR_SWATCH_MARGIN = 20
define COLOR_SWATCH_PADDING = 4
define COLOR_SWATCH_WIDTH = 100
define COLOR_SWATCH_FRAME_WIDTH = COLOR_SWATCH_PADDING*2 + COLOR_SWATCH_WIDTH + COLOR_SWATCH_MARGIN*2
define COLOR_SWATCH_HEIGHT = 150
define COLOR_SWATCH_FRAME_HEIGHT = COLOR_SWATCH_PADDING*2 + COLOR_SWATCH_HEIGHT + COLOR_SWATCH_MARGIN*2

### Color List

define COLOR_LIST_BUTTON_WIDTH = 50
define COLOR_LIST_GRID_ROWS = 3
define COLOR_LIST_GRID_COLUMNS = 12
define COLOR_LIST_SPACING = 5
define COLOR_LIST_MARGIN = 20

### Color Picker

init -200 python:
    # Color picker width
    PICKER_WIDTH = 655
    # Color picker height
    PICKER_HEIGHT = 100

define COLOR_PICKER_MARGIN = 20
define COLOR_PICKER_SPACING = 5

### Top Menu

define TOP_MENU_HEIGHT = 40
define TOP_MENU_WIDTH = ITEM_GRID_VIEWPORT_WIDTH + 2
