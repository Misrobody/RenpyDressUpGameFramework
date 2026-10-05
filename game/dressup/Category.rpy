################################################################################
# Category
#
# Represents a single customizable doll layer (hair, eyes, mouth, clothing,
# etc.).
#
# Each category:
#   - Belongs to a CategoryGroup.
#   - Tracks its currently selected item.
#   - Manages layer-specific color customization.
#   - Provides both full-size and preview images.
#
# Asset folders are expected to follow the format:
#
#   <priority> - <group> - <category>
#
################################################################################

init python:
    ################################################################################
    # Defaults
    ################################################################################

    # Indicates that no item is currently equipped for a category.
    NO_SELECTION = -1

    # Placeholder layer returned whenever a category has no active selection.
    EMPTY_IMAGE = Transform(
        Solid("#00000000"),
        xysize=(doll_width, doll_height)
    )


    ################################################################################
    # Category
    ################################################################################

    class Category:
        def __init__(self, category_group, name, priority, base_index=NO_SELECTION, color_manager=None):
            """
            Create a category from an asset folder definition.
            Args:
                category_group: Parent CategoryGroup object.
                name:           Internal category identifier.
                priority:       Layer render priority. Higher values render above lower ones.
                base_index:     Default equipped item on initialization.
                color_manager:  Optional ColorManager used for layer recoloring.
            """
            self._category_group = category_group
            self._name = name.title().replace("_", " ")
            self.key = name
            self._priority = priority
            self._selected_index = base_index       
            self._base_index = base_index         
            self._color_manager = color_manager if color_manager else ColorManager()
            self._asset_path = f"{self._priority} - {self.category_group.key} - {self.key}"
            self._item_count = COUNT_LIST[self._asset_path]

        def random_item(self):
            """
            Randomly select an available item and assign random colors
            for active color channels.
            """
            self._selected_index = renpy.random.randint(self._base_index, self._item_count - 1)
            self._color_manager.random_colors()

        def __repr__(self):
            return self._name

        def deselect(self):
            self._selected_index = self._base_index

        def reset_colors(self):
            self._color_manager.reset_colors()

        def select(self, index):
            self._selected_index = index

        def toggle(self, item_id):
            if self.selected_index == item_id:
                self.deselect()
            else:
                self.select(item_id)

        # Getters

        @property
        def color_manager(self):
            return self._color_manager

        @property
        def priority(self):
            return self._priority

        @property
        def selected_index(self):
            return self._selected_index

        @property
        def category_group(self):
            return self._category_group

        @property
        def item_count(self):
            return self._item_count

        @property
        def current_image(self):
            return self.get_image(self._selected_index)

        @property
        def name(self):
            return self._name

        def get_image(self, index):
            """
            Returns the displayable for an item index.
            If NO_SELECTION is supplied, a transparent placeholder image
            is returned instead.
            """
            if index == NO_SELECTION:
                return EMPTY_IMAGE
            return At(
                f"images/doll/{self._asset_path}/{self.key}_{index}.PNG",
                self._color_manager.get_rgb_transform()
            )

        def get_button_image(self, index):
            """
            Generates a cropped preview image used by wardrobe buttons.
            Crop data is retrieved from CROP_LIST and automatically scaled
            to fit the preview area.
            """
            item_key = f"{self.key}_{index}.PNG"
            keys_test = CROP_LIST.keys()
            assert item_key in keys_test, f"{item_key} is not in crop_list.keys():\n{keys_test}"
                
            # Expand the detected crop region to provide a more usable
            # thumbnail area around the item.
            mean_x, mean_y, dev_x, dev_y = CROP_LIST[item_key]

            MAGIC_NUMBER = 1.2
            dev_x = round(min(MAGIC_NUMBER*max(dev_x, 1), doll_width))
            dev_y = round(min(MAGIC_NUMBER*max(dev_y, 1), doll_height))

            x0 = max(int(mean_x - dev_x/2), 0)
            y0 = max(int(mean_y - dev_y/2), 0)
            
            scalef = min(CROP_SIZE / dev_x, CROP_SIZE / dev_y)
            return  Transform(Crop((x0, y0, dev_x, dev_y), self.get_image(index)), zoom=scalef)

        # Setters

        def set_base_index(self, i):
            self._base_index = i
            self._selected_index = i

        def set_color_manager(self, mgr):
            self._color_manager = mgr



