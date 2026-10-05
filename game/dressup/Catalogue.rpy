################################################################################
# Catalogue System
#
# Scans the doll asset directory and automatically builds:
# - Category Groups (body, face, clothing, etc.)
# - Categories (hair, eyes, mouth, skin, etc.)
# - Group -> Category mappings
#
# The catalogue acts as the central controller for:
# - Item selection
# - Category navigation
# - Color management
# - Character composition
# - Saving rendered dolls
################################################################################

init python:
    import datetime, os
    from collections import defaultdict

    ################################################################################
    # Defaults
    ################################################################################

    # Base skin layer. Also used as the default selected category.
    SKIN_LAYER = "skin"

    # Category selected when the catalogue is first opened.
    DEFAULT_CATEGORY_KEY = SKIN_LAYER

    # Group selected when the catalogue is first opened.
    DEFAULT_GROUPS_KEY = "body"


    ################################################################################
    # Category Configuration
    ################################################################################
    #
    # Per-category initialization settings.
    #
    # base_index:
    # Default item selected when the category is initialized.
    #
    # manager:
    # ColorManager controlling recolorable layers in this category.
    #
    # Categories omitted from this table use their default Category settings.

    CATEGORY_CONFIG = {
        "skin": {
            "base_index": 0,
            "manager": SKIN_MANAGER,
        },
        "eyebrows": {
            "base_index": 0,
            "manager": NO_COLOR_MANAGER,
        },
        "mouth": {
            "base_index": 0,
            "manager": MOUTH_MANAGER,
        },
        "eyes": {
            "base_index": 0,
        },
        "background": {
            "base_index": 0,
        }
    }

    ################################################################################
    # Asset Discovery
    ################################################################################
    
    def read_cats():
        '''
        Reads the doll folder structure and generates runtime category objects.
        Expected folder format: <priority> - <group> - <category>
        Returns:
            subs -> group lookup table
            cats -> category lookup table
            maps -> group -> category mapping
        '''
        cats = {}
        subs = {}
        maps = defaultdict(list)
        for root, dirs, files in os.walk(renpy.loader.transfn("images/doll/")):
            for dirname in dirs:
                infos = dirname.split(" - ")
                if infos[1] not in subs:
                    subs[infos[1]] = CategoryGroup(infos[1], priority=len(subs))
                curcat = Category(subs[infos[1]], infos[2], int(infos[0]))
                cats[infos[2]] = curcat
                maps[curcat.category_group.key].append(curcat)
        return subs, cats, maps


    ################################################################################
    # Catalogue
    ################################################################################

    class Catalogue:
        def __init__(self):
            self._current_category_key = DEFAULT_CATEGORY_KEY
            self._current_group_key = DEFAULT_GROUPS_KEY
            self._initialize_categories()

        def _initialize_categories(self): 
            """
            Initializes all catalogue data.
             
            Steps:
            1. Load category definitions from disk.
            2. Build layer render order.
            3. Sort categories by priority.
            4. Apply category-specific defaults.
            5. Attach configured ColorManagers.
            """   
            self._groups, self._categories, self._mappings = read_cats()

            self._layer_order = sorted(
                self._categories.keys(),
                key=lambda k: self._categories[k]._priority,
                reverse=True
            )

            for i in self._mappings.keys():
                self._mappings[i] = sorted(
                    self._mappings[i],
                    key=lambda c: self._categories[c.key]._priority,
                    reverse=True
                )

            for key, config in CATEGORY_CONFIG.items():
                category = self._categories[key]
                if "base_index" in config:
                    category.set_base_index(config["base_index"])
                if "manager" in config:
                    category.set_color_manager(config["manager"])
                
        def toggle_item(self, item_id):
            category = self.current_category.toggle(item_id)

        def reset_all_selections(self):
            for category in self._categories.values():
                category.deselect()
                category.reset_colors()

        def _show_message(self, message):
            renpy.show_screen(
                "confirm",
                message=message,
                yes_action=Hide("confirm"),
                no_action=Hide("confirm"),
                no_show=False,
                yes_message="Got it!"
            )

        def save_doll(self):
            """
            Saves the currently assembled character.
            Routes to either desktop or web implementation depending
            on the active Ren'Py platform.
            """
            if renpy.emscripten:
                self.save_doll_web()
            else:
                self.save_doll_desktop()

        def save_doll_web(self):
            """
            Web builds cannot save rendered files directly.
            Displays an informational message instructing the player
            to use screenshots instead.
            """
            self._show_message(
                "The save function is only available on desktop for technical reasons. However, fell free to take a screenshot of your character!"
            )

        def save_doll_desktop(self): 
            """
            Renders the current doll composite to a JPG file and saves
            it to the game directory.          
            Output filename format: <game_name><timestamp>.jpg
            """            
            filename = (
                f"{config.name}"
                f"{datetime.datetime.now():%Y%m%d%H%M%S}.jpg"
            )
            renpy.render_to_file(self.get_doll(), filename, doll_width, doll_height)
            full_path = os.path.join(config.basedir, filename)         
            self._show_message(
                f"Your Character has been saved at:\n"
                f"{{color={gui.muted_color}}}{full_path}"
            )

        def random_outfit(self):
            for k in self._categories:
                self._categories[k].random_item()

        # Setters
           
        def set_current_category(self, key):
            self._current_category_key = key
            self._categories[key].color_manager.update_pickers()

        def set_current_group(self, key):
            self._current_group_key = key
            self._current_category_key = self._mappings[key][0].key

        def set_current_color(self, color, index = 0):
            self.current_category.set_color(color, index)

        def is_selected_subcategory(self, cur):
            return self._current_category_key == cur

        # Getters

        @property
        def current_category_key(self):
            return self._current_category_key

        @property
        def current_group_key(self):
            return self._current_group_key

        @property
        def current_category(self):
            return self._categories[self._current_category_key]

        @property
        def group_keys(self):
            return self._mappings.keys()

        @property
        def current_item(self):
            return self.current_category.selected_index

        def current_categories(self):
            return sorted(
                    self._mappings[self._current_group_key],
                    key=lambda k: self._categories[k.key]._priority,
                    reverse=True
                )

        def current_stock(self):
            return self.current_category.item_count

        def get_button(self, item_id):
            category = self.current_category
            return category.get_button_image(item_id)


        def get_doll(self, dynamic = False):
            """
            Builds the final layered character image. If `dynamic` is True,
            return a DynamicDisplayable that updates over time;
            otherwise return a static Transform.
            Layers are composited according to _layer_order.
            """
            def build_composite():
                return Transform(Composite(
                    (doll_width, doll_height),
                    *[
                        coord
                        for key in self._layer_order
                        for coord in ((0, 0), self._categories[key].current_image)
                    ]
                ))

            if dynamic:
                def doll_callback(st, at):
                    return build_composite(), 0.05
                return DynamicDisplayable(doll_callback)
            else:
                return build_composite()

            
        