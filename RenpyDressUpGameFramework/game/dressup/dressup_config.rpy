## This file contains all the adjustable parameters of the framework

init -200 python:  
    ################################################################################
    # Defaults
    ################################################################################

    # The path to the base directory of the doll imageset. Do not put trailing /
    IMAGESET_PATH = "images/doll" # or "images/doll_2" to try out the other included example

################################################################################
# UI Constants
################################################################################

### Globals

define catalogue = Catalogue()
define DRESSUP_GAP = 40
define CONTROL_PANEL_WIDTH = config.screen_width - doll_width - DRESSUP_GAP

### Item Grid

define ITEM_GRID_COLUMNS = 6
define ITEM_GRID_ROWS = max((catalogue.current_stock() + 4) // ITEM_GRID_COLUMNS, 3)
define ITEM_GRID_SPACING = 15
define ITEM_GRID_ITEM_SIZE = int(round(
    (CONTROL_PANEL_WIDTH - ITEM_GRID_SPACING * (ITEM_GRID_COLUMNS - 1))
    / ITEM_GRID_COLUMNS
))
define ITEM_GRID_VIEWPORT_HEIGHT = 3 * ITEM_GRID_ITEM_SIZE + 2 * ITEM_GRID_SPACING 
define ITEM_GRID_VIEWPORT_WIDTH = CONTROL_PANEL_WIDTH

### Category Bar

define CATEGORY_BUTTON_BUTTON_SPACING = -5
define CATEGORY_BUTTON_BAR_SPACING = -4
define CATEGOTY_BUTTON_HEIGHT = 55
define CATEGORY_BAR_GROUP_BUTTON_WIDTH = CONTROL_PANEL_WIDTH // len(catalogue.group_keys) - CATEGORY_BUTTON_BUTTON_SPACING
define CATEGORY_BAR_CATEGORY_BUTTON_WIDTH = CONTROL_PANEL_WIDTH // len(catalogue.current_categories()) - CATEGORY_BUTTON_BUTTON_SPACING

### Color Menu

define COLOR_MENU_WIDTH = CONTROL_PANEL_WIDTH
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
define TOP_MENU_WIDTH = CONTROL_PANEL_WIDTH + 2
