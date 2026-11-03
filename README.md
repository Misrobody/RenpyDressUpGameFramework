# Dress-Up Framework

A modular plug-and-play character creator and dress-up framework for Ren'Py, compatible with both web and desktop builds.

Assets are loaded directly from the image set. After creating or modifying assets, run the metadata generator to automatically build the data required by the framework.

## Asset Credits

- [Better Colorize for Ren'Py](https://feniksdev.itch.io/better-colorize-for-renpy) by Feniksdev
- [Color Picker for Ren'Py](https://feniksdev.itch.io/color-picker-for-renpy) by Feniksdev

## How It Works

The framework automatically discovers clothes, hairstyles, facial features, accessories, and other doll layers from a structured image set.

After updating your assets, run:

```bash
python generate_metadata.py images/doll
```

The generator will:

- Resize assets to the framework resolution.
- Detect doll dimensions.
- Generate thumbnail crop data.
- Count available items.
- Create `doll_data.json`.

No manual metadata editing is required.

## Asset Structure

### Folder Naming

Category folders must follow this format:

```text
<priority> - <group> - <category>
```

Example:

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
- `group` determines the top-level navigation tab.
- `category` determines the selectable category within that group.

### File Naming

Items inside a category folder must be named:

```text
<category>_<index>.PNG
```

Example:

```text
50 - clothes - shirt/

shirt_0.PNG
shirt_1.PNG
shirt_2.PNG
```

The category name in the filename must match the category defined in the folder name.

## Navigation Structure

Groups become the first navigation row.

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

Produces:

```text
Hair
Face
Clothes
```

Categories become the second navigation row.

Example:

```text
Hair
├── Front Hair
├── Back Hair
└── Eyebrows
```

## Image Requirements

- PNG only.
- Thumbnail generation uses visible pixels only.
- Assets are automatically resized by the generator.
- Optimizing source images is recommended for web builds.

## Metadata File

The generator creates a single metadata file:

```text
doll_data.json
```

inside the root of the image set directory.
