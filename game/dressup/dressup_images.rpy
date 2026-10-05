################################################################################
# Image definitions
################################################################################

image gui_bg = Frame("gui/frame.png", 10, 10) 

transform top_menu_color:
    matrixcolor TintMatrix("#ffafd2")

image top_menu_bg:
    Frame("gui/frame.png", 10, 10)

    top_menu_color

image bgim:
    "bg.jpg"
    xzoom 1.5
    yzoom 0.6*1.5
    xtile 3
    ytile 3

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
        matrixcolor TintMatrix("#ff7eab")
    on idle:
        matrixcolor TintMatrix("#fc4d8e")

transform hover_effect_category:
    on hover:
        matrixcolor TintMatrix("#fde4ed")
    on idle:
        matrixcolor TintMatrix("#ffafd2")

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

transform selected_effect_color:
    on hover:
        matrixcolor TintMatrix("#f30000d3")  
    on idle:
        matrixcolor TintMatrix("#800000e5")