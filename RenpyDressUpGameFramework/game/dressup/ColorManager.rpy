init -50 python:
    ################################################################################
    # Constants
    ################################################################################

    DEFAULT_COLORS = [
        "#ffffff", "#ffff66", "#ff6600", "#ff0000", "#990000",
        "#ffb1d2", "#e4458d", "#9967cb", "#53297c", "#6bc7fe",
        "#213c7a", "#3ddcb8", "#80d557", "#006a48", "#965446",
        "#331919", "#787897", "#474a5c", "#1a1a1a"
    ]

    SKIN_COLORS = [
        "#fce2c4", "#f7e1c6", "#f5d7b2", "#f3e0d7", "#f0d5be",
        "#eac086", "#f1c27d", "#e2bda0", "#e0ac69", "#d4a484",
        "#d2996b", "#c68642", "#b3744a", "#a67c52", "#8d5524",
        "#7f4f24", "#6b4423", "#5c3b1e", "#4b2e1a"
    ]

    PICKER_WIDTH = 655
    PICKER_HEIGHT = 100
    
    # You can switch around the channels to switch around the order of colors 1, 2 and 3
    CHANNELS = ("gray", "green", "blue", "red")


    ################################################################################
    # Color Manager
    ################################################################################

    class ColorManager:
        def __init__(self,
            base_gray="#ffffff", list_gray=DEFAULT_COLORS, active_gray=False,
            base_red=DEFAULT_COLORS[10], list_red=DEFAULT_COLORS, active_red=True,
            base_green=DEFAULT_COLORS[9], list_green=DEFAULT_COLORS, active_green=True,
            base_blue=DEFAULT_COLORS[1], list_blue=DEFAULT_COLORS, active_blue=True
        ):
            bases  = {
                CHANNELS[0]:locals()["base_" + CHANNELS[0]],
                CHANNELS[1]:locals()["base_" + CHANNELS[1]],
                CHANNELS[2]:locals()["base_" + CHANNELS[2]],
                CHANNELS[3]:locals()["base_" + CHANNELS[3]]
            }
            lists  = {
                CHANNELS[0]:locals()["list_" + CHANNELS[0]],
                CHANNELS[1]:locals()["list_" + CHANNELS[1]],
                CHANNELS[2]:locals()["list_" + CHANNELS[2]],
                CHANNELS[3]:locals()["list_" + CHANNELS[3]]
            }
            active  = {
                CHANNELS[0]:locals()["active_" + CHANNELS[0]],
                CHANNELS[1]:locals()["active_" + CHANNELS[1]],
                CHANNELS[2]:locals()["active_" + CHANNELS[2]],
                CHANNELS[3]:locals()["active_" + CHANNELS[3]]
            }

            self._base_colors     = bases
            self._color_lists     = lists
            self._active_channels = active

            self._pickers = {
                ch: ColorPicker(PICKER_WIDTH, PICKER_HEIGHT, bases[ch])
                for ch in CHANNELS
            }

            self._color_swatches = {
                ch: DynamicDisplayable(picker_color, picker=self._pickers[ch])
                for ch in CHANNELS
            }

            self.cur_color = 0

        def set_cur_color(self, i):
            self.cur_color = i

        def cur_color_value(self):
            return self.get_color(CHANNELS[self.cur_color + 1]).hexcode

        def cur_color_list(self):
            return self.get_active_color_lists()[self.cur_color]

        def cur_color_swatch(self):
            return self.get_active_color_swatches()[self.cur_color]

        def cur_picker(self):
            return self.get_active_pickers()[self.cur_color]

        def _active(self):
            return (ch for ch in CHANNELS if self._active_channels[ch])

        def random_colors(self):
            for ch in self._active():
                self._pickers[ch].set_color(
                    renpy.random.choice(self._color_lists[ch])
                )

        def get_color(self, channel):
            return self._pickers[channel].color

        def get_color_swatch(self, channel):
            return self._color_swatches[channel]

        def get_active_color_swatches(self):
            return [self._color_swatches[ch] for ch in self._active()]

        def get_active_pickers(self):
            return [self._pickers[ch] for ch in self._active()]

        def get_active_color_lists(self):
            return [(ch, self._color_lists[ch]) for ch in self._active()]

        def update_pickers(self):
            for ch in CHANNELS:
                self._pickers[ch].set_color(self._pickers[ch].color)

        def set_color(self, color, channel):
            self._pickers[channel].set_color(color)

        def reset_colors(self):
            for ch in CHANNELS:
                self._pickers[ch].set_color(self._base_colors[ch])

        def get_rgb_transform(self):
            shadow = "#130b00"
            kwargs = {}
            for ch in CHANNELS:
                kwargs[ch] = [self._pickers[ch].color, shadow]
                kwargs[ch + "_thresh"] = [255, 0]
            return RGBColorize(**kwargs).transform


    ################################################################################
    # Default Color Manager Definitions
    ################################################################################

    SKIN_MANAGER = ColorManager(
        base_green="#e0ac69",
        list_green=SKIN_COLORS,
        active_blue=False,
        active_red=False
    )
    NO_COLOR_MANAGER = ColorManager(
        active_blue=False,
        active_red=False,
        active_green=False
    )
    MOUTH_MANAGER = ColorManager(
        active_blue=False,
        active_red=False,
        base_green=DEFAULT_COLORS[4],
        active_green=True)

    BG_MANAGER = ColorManager(
        base_gray=DEFAULT_COLORS[9],
        active_gray=True,
        base_red=DEFAULT_COLORS[1],
        active_red=True,
        active_green=False,
        active_blue=False
    )
