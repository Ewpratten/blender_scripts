# My personal DCC scripts

This repo contains a Python package that can be loaded into multiple DCCs. It contains a collection of small utilities I commonly use.

## Features

- One plugin that works in all DCCs
- Positive Y Camera
  - Add a camera at origin facing positive Y
- Camera Utils
  - Position cameras using "Mouse look" controls
- "Pre-flight" Checklist system
  - Runs automated unit tests on your scenes and attempts to fix any issues found
  - DCC-agnostic
- Camera Picker
  - For working in scenes with multiple cameras
- Material presets
  - Quickly load various color palettes into your material set

### Multi-DCC Usage

The following steps are the only differences between running this plugin in each DCC.

## Using with Blender

Just clone this repo, and add it as your scripts directory in `Edit > Preferences > File Paths > Scripts`. All add-ons will show up in the add-ons menu.

You will also need PySide2 installed on your system.

## Using with Maya

Simply launch Maya using the following. The plugin will enter "bootstrap mode" and handle the rest of the loading work for you.

```sh
MAYA_PLUG_IN_PATH=/path/to/dcc_scripts/addons maya
```
