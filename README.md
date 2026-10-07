# Dress-Up Framework

A modular plug and play character creator and dress-up framework for Ren'Py. Works both for web and desktop.

The image assets are loaded directly from the image folder. After creating or modifying an image set, run the metadata generation script to automatically build the data required by the framework.

---

# Asset Credit

[Better Colorize for Ren'py](https://feniksdev.itch.io/better-colorize-for-renpy) (Feniksdev)

[Color Picker for Ren'py](https://feniksdev.itch.io/color-picker-for-renpy) (Feniksdev)

[Shugo Chara Eggs](https://ko-fi.com/s/73209cb5d1) (Meowsclemilk)

---

# How It Works

The framework automatically discovers clothing, hairstyles, accessories, facial features, and other doll layers from a structured image set. Each category corresponds to a directory and contains one or more PNG images representing selectable items.

The metadata generation script automatically:
- Resizes assets to the framework's required resolution.
- Determines the doll canvas size.
- Generates thumbnail crop data.
- Counts available items.
- Creates `doll_data.json`.

No manual metadata editing is required.

## Image Set Structure

Category folders must follow the format:

```text
<priority> - <group> - <category>
```

Examples:

```text
0 - body - skin
10 - hair - back_hair
20 - hair - front_hair
30 - face - eyes
40 - face - mouth
50 - clothes - shirts
60 - clothes - jackets
70 - accessories - glasses
```

Where:
- `priority` determines render order.
- `group` determines the top-level navigation group.
- `category` determines the selectable category inside that group.

## Item Naming

Items inside a category folder must follow:

```text
<category>_<index>.PNG
```

The category name must match the category portion of the folder name because the framework generates paths using:

```python
"{category}_{index}.PNG"
```

Example:

```text
50 - clothes - shirt/

shirt_0.PNG
shirt_1.PNG
shirt_2.PNG
```

## Render Priority

The numeric priority at the beginning of the folder name determines draw order. Lower priorities render first. Higher priorities render on top.

Example:

## Groups

Groups are used for the first navigation row.

Example:

```text
10 - hair - front_hair
20 - hair - back_hair
30 - hair - eyebrows

40 - face - eyes
50 - face - mouth

60 - clothes - shirts
70 - clothes - pants
```

Creates:

```text
Hair
Face
Clothes
```

in the group selector.

## Categories

Categories are used for the second navigation row.

Example:

```text
Hair
├── Front Hair
├── Back Hair
└── Eyebrows
```

Each category manages:

- Current selected item
- Default selection
- Color customization
- Thumbnail generation
- Image loading

# Image Requirements

## Format

Supported:

```text
PNG
```

Unsupported:

```text
JPG
JPEG
WEBP
GIF
```

## Transparency

Images should use transparency. Only visible pixels are used when generating thumbnail crop information.

## Resolution

Images do **not** need to be manually resized. The metadata generation script automatically scales every PNG to the framework's target height. Simply supply your source assets and run the generator. However, it is highly encouraged to optimize your exported images, if you plan on using the web build.

# Metadata Generation

After creating or modifying assets:

```bash
python generate_metadata.py <imgset_directory>
```

Example:

```bash
python generate_metadata.py images/doll
```

---

# What The Generator Does

## 1. Resize Assets

If the image set height is not the expected framework height, every PNG is automatically resized while maintaining aspect ratio.

No manual resizing is required.

## 2. Detect Doll Size

The generator determines:

```json
{
    "doll_width": 720,
    "doll_height": 1080
}
```

from the image set.

## 3. Generate Thumbnail Crop Data

For every PNG the generator:

- Finds the visible bounding box.
- Extracts the occupied image region.
- Stores crop information.

This is used to generate centered wardrobe thumbnails.

## 4. Count Available Items

The generator counts the number of PNGs present in every category folder.

Example:

```json
{
    "10 - hair - front_hair": 12,
    "20 - face - eyes": 8,
    "30 - clothes - shirts": 15
}
```

## 5. Generate Metadata File

The generator creates:

```text
doll_data.json
```

inside the image set root directory.
