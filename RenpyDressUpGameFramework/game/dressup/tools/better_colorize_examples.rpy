################################################################################
##
## Better Colorize by Feniks (feniksdev.itch.io / feniksdev.com)
##
################################################################################
## This file contains code to create more dynamic colour sliders in Ren'Py and
## to recolour a base image with up to 7*4 colours in Ren'Py.
## There are three main parts:
## 1) A shader which recolours an image based on a set of colours and
##    thresholds.
## 2) A DynamicDisplayable function to recolour an image based on a variable's
##    value (from 0-100) when provided sets of colours and thresholds.
## 3) A shader and associated transform to create a gradient from multiple
##    colour codes
##
## TO GET STARTED: Look at the EXAMPLES section below to see how to set up
## images to work with this code. There is an example screen you can look at by
## creating a button to access it, for example, with:
##
# textbutton "Colorize" action ShowMenu("colorize_example")
##
## Also consider checking out my itch.io for the associated image tool, which
## will allow you to preview the colours and thresholds when recolouring your
## images so you can achieve the best possible results.
## I will also be releasing tutorials detailing how to set up images for this
## tool and how to recolour them, on https://feniksdev.com
## Leave a comment on the tool page on itch.io if you run into any issues!

################################################################################
## EXAMPLES
################################################################################
## VARIABLES ###################################################################
## This is used for the slider to change the colour of the image. It goes from
## 0-100. In this case, it's set to randomly select a starting colour, but this
## could also be a simple `default hair_color = 30` or whatever value you like.
default skin_value = renpy.random.randint(0, 100)

## CONSTANTS ###################################################################
## These make it simpler to provide these same colour codes to both the bar
## shader and the DynamicDisplayable.
## This first list only provides RGBColorize a list of colours. That means it'll
## get the default thresholds (in this case, 255, 170, 85, 0), and it expects
## the whole image to be grayscale (any red/green/blue will be treated as if
## they were shades of gray).
define THREE_COLOR_SKIN = [
    RGBColorize(["#ffffffff", "#ffefe6ff", "#e7a28dff", "#000"]),
    RGBColorize(["#F6D7C5FF", "#EBB998FF", "#7C2A2CFF", "#000"]),
    RGBColorize(["#ffeedaff", "#E19677FF", "#914633ff", "#000"]),
    RGBColorize(["#fae7c3ff", "#F1B67AFF", "#994d3aff", "#000"]),
    RGBColorize(["#FFEED6FF", "#F5A278FF", "#96402fff", "#000"]),
    RGBColorize(["#F09D73FF", "#AA5E3EFF", "#6e2f14ff", "#000"]),
    RGBColorize(["#DF8C6CFF", "#9C4C2BFF", "#57160cff", "#000"]),
    RGBColorize(["#B66854FF", "#6D3129FF", "#3a0f0fff", "#000"]),
    RGBColorize(["#B06C57FF", "#642B20FF", "#250707ff", "#000"]),
    RGBColorize(["#AC5D36FF", "#501E13FF", "#200207ff", "#000"]),
    RGBColorize(["#892E1CFF", "#3C0F0CFF", "#110005ff", "#000"]),
    RGBColorize(["#792934FF", "#2A0912FF", "#0e0006ff", "#000"]),
    RGBColorize(["#7E4D49FF", "#371C23FF", "#0c010fff", "#000"]),
]
## This second list provides RGBColorize with both colours and thresholds.
## Note that the fourth colour, "#000", is so that threshold can be used to
## isolate the line art and colour it black.
## The hand image this is used on is fairly pale, so the darkest thresholds are
## quite high (i.e. closer to 255 aka 100% / white) to get more depth out of the
## existing colours.
## Like with the last example, only one list of colours and thresholds are
## provided, so this will be treated as if the image is grayscale and ignore
## the red/green/blue channels.
define THREE_COLOR_SKIN2 = [
    RGBColorize(["#ffffffff", "#f4ddd3", "#ae6a55", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#F6D7C5FF", "#EBB998FF", "#7C2A2CFF", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#ffeedaff", "#E19677FF", "#914633ff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#fae7c3ff", "#F1B67AFF", "#994d3aff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#FFEED6FF", "#F5A278FF", "#96402fff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#F09D73FF", "#AA5E3EFF", "#6e2f14ff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#DF8C6CFF", "#9C4C2BFF", "#57160cff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#B66854FF", "#6D3129FF", "#3a0f0fff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#B06C57FF", "#642B20FF", "#250707ff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#AC5D36FF", "#501E13FF", "#200207ff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#892E1CFF", "#3C0F0CFF", "#110005ff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#792934FF", "#2A0912FF", "#0e0006ff", "#000"], [250, 181, 65, 47]),
    RGBColorize(["#7E4D49FF", "#371C23FF", "#0c010fff", "#000"], [250, 181, 65, 47]),
]

## This last list takes advantage of RGB channels. The base image has coloured
## the nails green and parts of the palm and fingers red so they can be coloured
## separately from the gray parts. This is useful for things like nail polish,
## separating lips from teeth or eyes from eye whites, adding extra depth to
## shadows with different colours, etc.
## In particular, it specifies which channel each colour list belongs to -
## gray is the "default", because it covers white & black, as well as all the
## shades of grey in between. Red, green and blue are used when there is more
## of that channel in the image than the others. For example, the nails are
## green, so the green channel controls the colour of the nails.
## These first few images don't need the red channel, because it should be the
## same colour as the gray channel, so it can be omitted.
## Similarly, the thresholds for the red/green channels are the same as the
## gray channel, but if you wanted to change it you could do so by specifying
## red_thresh / green_thresh / blue_thresh also.
## The blue channel matches the gray channel since it is not provided (nor
## present in the image).
define RGB_SKIN = [
    RGBColorize(gray=["#ffffff", "#f4ddd3", "#ae6a55", "#000000"],
        gray_thresh=[250, 181, 65, 47],
        green=["#c48beb", "#7645b7", "#1f0a57", "#000000"],
        green_thresh=[250, 181, 125, 56]),
    RGBColorize(gray=["#F6D7C5FF", "#EBB998FF", "#7C2A2CFF", "#000"],
        gray_thresh=[250, 181, 65, 47],
        green=["#d97ccb", "#8d0a61", "#550957", "#000"]),
    RGBColorize(gray=["#ffeedaff", "#E19677FF", "#914633ff", "#000"],
        gray_thresh=[250, 181, 65, 47],
        green=["#7e7cd9", "#201c63", "#090e48", "#000"]),
    RGBColorize(gray=["#fae7c3ff", "#F1B67AFF", "#994d3aff", "#000"],
        gray_thresh=[250, 181, 65, 47],
        green=["#7bb7d9", "#1b6360", "#083348", "#000"]),
    RGBColorize(gray=["#FFEED6FF", "#F5A278FF", "#96402fff", "#000"],
        gray_thresh=[250, 181, 65, 47],
        green=["#4fd6c5", "#2c4c47", "#084843", "#000"]),

    ## These images begin to provide the red channel to recolour the palm.
    RGBColorize(gray=["#F09D73FF", "#AA5E3EFF", "#6e2f14ff", "#000"],
        gray_thresh=[250, 181, 65, 47],
        red=["#c77f71", "#b35f4a", "#912211", "#000"],
        green=["#19993a", "#1c3322", "#06350e", "#000"]),
    RGBColorize(gray=["#DF8C6CFF", "#9C4C2BFF", "#57160cff", "#000"],
        gray_thresh=[250, 181, 65, 47],
        red=["#c77f71", "#b35f4a", "#912211", "#000"],
        green=["#e5d336", "#5e430a", "#513312", "#000"]),
    RGBColorize(gray=["#B66854FF", "#6D3129FF", "#3a0f0fff", "#000"],
        gray_thresh=[250, 181, 65, 47],
        red=["#c77f71", "#b35f4a", "#912211", "#000"],
        green=["#e59536", "#5e3209", "#513312", "#000"]),
    RGBColorize(gray=["#B06C57FF", "#642B20FF", "#250707ff", "#000"],
        gray_thresh=[250, 181, 65, 47],
        red=["#c77f71", "#b35f4a", "#912211", "#000"],
        green=["#cc341c", "#42201c", "#381d14", "#000"]),
    RGBColorize(gray=["#ac5d36", "#501e13", "#200207", "#000000"],
        gray_thresh=[250, 181, 65, 47],
        red=["#97655c", "#915749", "#912211", "#000000"],
        green=["#d32262", "#583144", "#270f18", "#000000"]),
    RGBColorize(gray=["#892e1c", "#3c0f0c", "#110005", "#000000"],
        gray_thresh=[250, 181, 65, 47],
        red=["#9e6255", "#834839", "#50201e", "#000000"],
        green=["#c48beb", "#7645b7", "#1f0a57", "#000000"]),
    RGBColorize(gray=["#792934", "#2a0912", "#0e0006", "#000000"],
        gray_thresh=[250, 181, 65, 47],
        red=["#a95963", "#743740", "#0e0006", "#000000"],
        green=["#d97ccb", "#8d0a61", "#550957", "#000000"]),
    RGBColorize(gray=["#7e4d49", "#371c23", "#0c010f", "#000000"],
        gray_thresh=[250, 181, 65, 47],
        red=["#bc7177", "#754949", "#2e0839", "#000000"],
        green=["#7e7cd9", "#201c63", "#090e48", "#000000"]),
]
## IMAGES ######################################################################
## These are the images which will be recoloured. It is a DynamicDisplayable
## that uses the function declared further down.
## We pass in the name of the image - in this case, the image is hand_rgb.png,
## so assuming auto-import rules, the image name is "hand_rgb".
## The var_name is the variable from earlier, which is called skin_value.
## It's in quotes so it can be fetched in real-time.
## Then the recolour colours are passed in. The thresholds are not provided.
image colorized_hand1 = DynamicDisplayable(multi_colorize_img,
    img="hand_rgb", var_name='skin_value', color_splits=THREE_COLOR_SKIN)
## This is the same as before, but it uses a list with the thresholds provided.
image colorized_hand2 = DynamicDisplayable(multi_colorize_img,
    img="hand_rgb", var_name='skin_value', color_splits=THREE_COLOR_SKIN2)
## This uses the RGB hand version, which allows for recolouring based on the
## red/green/blue channels also.
image colorized_hand3 = DynamicDisplayable(multi_colorize_img,
    img="hand_rgb", var_name='skin_value', color_splits=RGB_SKIN)

################################################################################
## SCREEN
################################################################################
screen colorize_example():
    tag menu

    # The background; can be whatever
    add "#21212db2"

    textbutton _("Return") action Return()

    vbox:
        spacing 15 yalign 0.5 xalign 0.1
        hbox:
            ## Here's the base image. It's made up of a (mostly) grayscale image
            ## layer that gets recoloured (the colorized_base image declared
            ## above as a DynamicDisplayable) and a heart image, which is not
            ## recoloured.
            fixed:
                fit_first True
                at transform:
                    zoom 0.65
                add "colorized_hand1"
                add "hand_heart"
                text "Default Thresholds" yalign 1.0 xalign 0.5:
                    outlines [(2, "#000")] color "#fff" size 60

            ## And the second version, with custom thresholds.
            fixed:
                fit_first True
                at transform:
                    zoom 0.65
                add "colorized_hand2"
                add "hand_heart"
                text "Custom Thresholds" yalign 1.0 xalign 0.5:
                    outlines [(2, "#000")] color "#fff" size 60

            ## And the final version, which uses the red and green channels as
            ## well as the gray channel.
            fixed:
                fit_first True
                at transform:
                    zoom 0.65
                add "colorized_hand3"
                add "hand_heart"
                text "RGB Version" yalign 1.0 xalign 0.5:
                    outlines [(2, "#000")] color "#fff" size 60

            vbar value VariableValue('skin_value', 100):
                ysize 0.7 yalign 0.5
                ## This At() construction lets us use the shader from earlier to
                ## make a bar image.
                ## We pass the skin colours from earlier to make up the bar
                ## colours. In `*THREE_COLOR_SKIN`, the * is a trick to
                ## pass in all the colours from the list.
                ## It also needs vertical=True to be a vertical bar.
                base_bar At("#fff", multicolor_image(*THREE_COLOR_SKIN, vertical=True))
                thumb Transform("#5b918e", ysize=20)
                bar_invert True # To have 0 at the top instead of the bottom


        ## This is the horizontal bar under the hand.
        ## It uses VariableValue with the variable from earlier. It goes
        ## from 0-100.
        bar value VariableValue('skin_value', 100):
            xsize 0.7 xalign 0.5 ## Sizing/positioning info
            ## This At() construction lets us use the shader from earlier to
            ## make a bar image.
            ## We pass the skin colours from earlier to make up the bar
            ## colours. In `*THREE_COLOR_SKIN`, the * is a trick to
            ## pass in all the colours from the list.
            base_bar At("#fff", multicolor_image(*THREE_COLOR_SKIN))
            thumb Transform("#5b918e", xsize=20)

    fixed:
        xalign 1.0 yalign 0.5 fit_first True
        ## This is an example of how to colorize an image directly, without
        ## all the sliders. This would be suitable to provide as an option
        ## in a character creator, for example.
        add "hand_rgb" at RGBColorize(
            gray=["#AC5D36FF", "#501E13FF", "#200207ff", "#000"],
            gray_thresh=[250, 181, 65, 47],
            red=["#c77f71", "#b35f4a", "#912211", "#000"],
            green=["#d32262", "#583144", "#270f18", "#000"]).transform:
                zoom 0.4
        add "hand_heart" zoom 0.4
        text "Set colour/\nnot dynamic" yalign 1.0 xalign 0.5 text_align 0.5:
            outlines [(2, "#000")] color "#fff"