################################################################################
# Dress-Up UI
#
# Main screens used by the outfit creator.
#
# Layout:
#   outfits_ui
#   ├── top_menu
#   ├── category_bar
#   ├── item_grid
#   └── color_menu
#       ├── color_menu_buttons
#       ├── color_menu_list
#       └── color_menu_picker
#
# Global state:
#   picker : bool
#       False = use palette swatches
#       True  = use free color picker
#
################################################################################

################################################################################
# Globals
################################################################################

define picker = False
define catalogue = Catalogue()

### Item Grid

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

define COLOR_PICKER_MARGIN = 20
define COLOR_PICKER_SPACING = 5

### Top Menu

define TOP_MENU_HEIGHT = 40
define TOP_MENU_WIDTH = ITEM_GRID_VIEWPORT_WIDTH + 2

################################################################################
# Color Menu Screens
################################################################################


## Color Menu Buttons ##########################################################
##
## Displays the available color channels for the currently selected item.
##
## Each button corresponds to a color slot managed by the active category's
## color manager. Selecting a button changes the active color channel that
## will be edited by either the palette view or free-form picker.

screen color_menu_buttons(cm):
    style_prefix "color_menu_buttons"
    vbox:              
        for i in range(len(cm.get_active_color_swatches())):
            textbutton "Color [i+1]":
                if cm.cur_color == i:
                    at selected_effect
                else:
                    at hover_effect_main                  
                action Function(cm.set_cur_color, i)

style color_menu_buttons_button_text:
    align(0.5, 0.5)
    color gui.text_color
    size 30

style color_menu_buttons_vbox:
    spacing COLOR_MENU_BUTTON_SPACING

style color_menu_buttons_button:
    xsize COLOR_MENU_COLOR_BUTTON_WIDTH
    ysize COLOR_MENU_COLOR_BUTTON_HEIGHT
    background "gui_bg"


## Color Menu Picker ###########################################################
##
## Displays the free-form color picker used to select arbitrary colors.
##
## Retrieves the currently active picker widget from the current category's
## color manager and displays both the picker and hue adjustment bar.
##
## Used when:
## picker == True

screen color_menu_picker(cm):
    style_prefix 'cpicker'

    $ p = cm.cur_picker()

    frame:
        background None
        padding(0, 0, 0, 0)
        margin(
            COLOR_PICKER_MARGIN,
            COLOR_PICKER_MARGIN,
            COLOR_PICKER_MARGIN,
            COLOR_PICKER_MARGIN
        )
        vbox:   
            spacing COLOR_PICKER_SPACING                           
            add p
            bar value FieldValue(p, "hue_rotation", 1.0) xsize p.xsize
    

## Color Menu List #############################################################
##
## Displays the predefined color palette for the currently selected color
## channel.
##
## Each swatch applies a specific color value to the active channel when
## selected.
##
## Used when:
## picker == False

screen color_menu_list(cm):
    style_prefix "color_list"
    $ channel, colors = cm.cur_color_list()
    frame:
        grid COLOR_LIST_GRID_COLUMNS COLOR_LIST_GRID_ROWS:             
            for c in colors:
                button:    
                    background Solid(c)
                    #if c == cm.cur_color_value() #at outline(color="#ff0000", width=10)
                    action Function(cm.set_color, c, channel) 
                    at hover_effect_color

style color_list_grid:
    spacing COLOR_LIST_SPACING  

style color_list_button:
    xysize (COLOR_LIST_BUTTON_WIDTH, COLOR_LIST_BUTTON_WIDTH)

style color_list_frame:
    background None
    padding(0, 0, 0, 0)
    margin(
        COLOR_LIST_MARGIN,
        COLOR_LIST_MARGIN,
        COLOR_LIST_MARGIN,
        COLOR_LIST_MARGIN
    )

## Color Menu Toggle ###########################################################

screen color_menu_toggle():
    style_prefix "color_menu_toggle"
    button at hover_effect_main:       
        text "Mode" align(.5, .5) size 30
        action ToggleVariable("picker", True)

style color_menu_toggle_button:
    background "gui_bg"
    xysize (COLOR_MENU_TOGGLE_WIDTH, COLOR_MENU_TOGGLE_HEIGHT) 


## Color Menu Toggle ###########################################################

screen color_menu_swatch(cm):
    style_prefix "color_swatch"
    frame:
        add cm.cur_color_swatch():
            align(.5, .5)          
            xsize COLOR_SWATCH_WIDTH
            ysize COLOR_SWATCH_HEIGHT

style color_swatch_frame:
    align(.5, .5)
    margin(
        COLOR_SWATCH_MARGIN,
        COLOR_SWATCH_MARGIN,
        COLOR_SWATCH_MARGIN,
        COLOR_SWATCH_MARGIN
    )
    xsize COLOR_SWATCH_FRAME_WIDTH
    ysize COLOR_SWATCH_FRAME_HEIGHT           
            

## Color Menu ##################################################################
##
## Main color customization panel.
##
## Combines color channel selection, current color preview, and color editing
## controls. Depending on the current picker state, either the predefined
## color list or the free-form color picker is displayed.
##
## Displays a placeholder message when the current category does not support
## color customization.

screen color_menu():  
    style_prefix "color_menu_menu"
    $ cm = catalogue.current_category.color_manager

    frame:
        if not len(cm.get_active_color_lists()):
            text "No colors"
        else:
            hbox align(0, .5):
                use color_menu_toggle()
                use color_menu_buttons(cm)     
                use color_menu_swatch(cm)              
                if picker:
                    use color_menu_picker(cm)
                else:
                    use color_menu_list(cm)

style color_menu_menu_frame:
    xysize(
        COLOR_MENU_WIDTH,
        COLOR_MENU_HEIGHT
    )
    padding(0, 0, 0, 0)

style color_menu_menu_frame_text:
    color gui.text_color
    align(.5, .5)

################################################################################
# Item Selection Screens
################################################################################


## Item Grid ###################################################################
##
## Displays all available items belonging to the currently selected category.
##
## Items are arranged in a scrollable grid. Selecting an item toggles its
## equipped state and updates the doll preview.
##
## Grid dimensions are calculated dynamically based on the number of items
## available in the current category.

screen item_grid():
    style_prefix "item_grid"
    viewport:
        mousewheel "vertical"
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        frame:     
            grid ITEM_GRID_COLUMNS ITEM_GRID_ROWS:
                for i in range(0, catalogue.current_stock()):
                    button:
                        add catalogue.get_button(i) align(.5, .5)
                        action Function(catalogue.current_category.toggle, i)
                        at hover_effect_clothes
                        if catalogue.current_item == i:
                            at selected_effect

style item_grid_viewport:
    xsize ITEM_GRID_VIEWPORT_WIDTH
    ysize ITEM_GRID_VIEWPORT_HEIGHT

style item_grid_grid:
    xfill False
    yfill False
    align(.5, .5)
    spacing ITEM_GRID_SPACING

style item_grid_frame:
    background None
    xfill False
    yfill False
    padding(0, 0, 0, 0)
    margin(0, 0, 0, 0)

style item_grid_button:
    background "gui_bg"                       
    xysize(
        ITEM_GRID_ITEM_SIZE,
        ITEM_GRID_ITEM_SIZE
    )


################################################################################
# Navigation Screens
################################################################################


## Category Bar ################################################################
##
## Displays outfit navigation controls.
##
## The upper row contains clothing groups such as Hair, Clothes, Accessories,
## and other major outfit sections.
##
## The lower row contains individual categories belonging to the selected
## group.
##
## Selecting a group updates the available categories. Selecting a category
## updates the item grid and color controls.

screen category_bar():
    style_prefix "category_bar"
    vbox:              
        hbox:            
            for k in catalogue.group_keys:
                textbutton k.capitalize():              
                    action Function(catalogue.set_current_group, k)
                    at hover_effect_groups
                    if catalogue.current_group_key == k:
                        at selected_effect
        hbox:        
            for v in catalogue.current_categories():
                textbutton "[v]":            
                    action Function(catalogue.set_current_category, v.key)
                    at hover_effect_category
                    if catalogue._current_category_key == v.key:
                        at selected_effect

style category_bar_vbox:
    spacing CATEGORY_BUTTON_BAR_SPACING

style category_bar_hbox:
    spacing CATEGORY_BUTTON_BUTTON_SPACING

style category_bar_button:
    background "gui_bg"
    xsize CATEGORY_BUTTON_WIDTH
    ysize CATEGOTY_BUTTON_HEIGHT

style category_bar_button_text:
    size 30
    color gui.text_color
    align(.5, .5)
    text_align 0.5

## Top Menu ####################################################################
##
## Displays global outfit creator actions.
##
## Available actions:
## Random - Generates a random outfit.
## Reset - Clears all current selections.
## Options - Opens the preferences menu.
## Save - Saves the current doll configuration.
## Menu - Returns to the main menu.
##
## This menu remains visible regardless of the currently selected category.

screen top_menu:
    style_prefix "top_menu"
    frame:    
        hbox:      
            textbutton "Random" action Function(catalogue.random_outfit)
            textbutton "Reset" action Function(catalogue.reset_all_selections)
            textbutton "Options" action ShowMenu("preferences")
            textbutton "Save" action Function(catalogue.save_doll)
            textbutton "Menu" action MainMenu()

style top_menu_button is gui_button
style top_menu_button_text is gui_button_text

style top_menu_frame:
    xysize (TOP_MENU_WIDTH, TOP_MENU_HEIGHT)
    background "top_menu_bg"

style top_menu_hbox:
    spacing 30
    align(.5, .5)

style top_menu_button_text:
    size 25
    color "#000000"
    hover_color "#5a5a5a"
    selected_color "#000000"
    text_align 0.5

################################################################################
# Root Screens
################################################################################

## Doll Panel ##################################################################

screen doll_panel():
    add catalogue.get_doll(dynamic=picker)


## Control Panel ###############################################################

screen control_panel():
    vbox spacing 20 yalign .5:  
        use top_menu()                         
        use category_bar() 
                
        use item_grid()
        use color_menu()                    
        

## Outfits UI ##################################################################
##
## Main dress-up interface.
##
## This screen assembles all components required for outfit creation and
## customization. The doll preview updates automatically in response to item
## and color selection changes.

screen outfits_ui():
    add "bgim"
    hbox spacing (config.screen_width - doll_width - ITEM_GRID_VIEWPORT_WIDTH)//2 :   
        use doll_panel()
        use control_panel()
        

        
            

