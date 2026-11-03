################################################################################
# Image definitions
################################################################################

image gui_bg = Frame("gui/frame.png", 10, 10) 

transform top_menu_color:
    matrixcolor TintMatrix("#ffffff")

image top_menu_bg:
    Frame("gui/frame.png", 10, 10)
    top_menu_color

image dressup_background = Solid("#dadada")


################################################################################
# Transform definitions
################################################################################

transform hover_effect_clothes:
    on hover:
        matrixcolor TintMatrix("#e0e0e0ff")
    on idle:
        matrixcolor TintMatrix("#00000000")

transform hover_effect_groups:
    on hover:
        matrixcolor TintMatrix("#e6e6e6")
    on idle:
        matrixcolor TintMatrix("#ffffff")

transform hover_effect_category:
    on hover:
        matrixcolor TintMatrix("#bbbbbb")
    on idle:
        matrixcolor TintMatrix("#d4d4d4")

transform hover_effect_color:
    on hover:
        matrixcolor TintMatrix("#7f89a7")
    on idle:
        matrixcolor TintMatrix("#00000000")

transform hover_effect_main:
    on hover:
        matrixcolor TintMatrix("#e0e0e0ff")
    on idle:
        matrixcolor TintMatrix("#00000000")

transform selected_effect:
    on hover:
        matrixcolor TintMatrix("#fffaba")  
    on idle:
        matrixcolor TintMatrix("#fff34d")