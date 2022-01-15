# My personal DCC scripts

This repo contains a Python package that can be loaded into multiple DCCs. It contains a collection of small utilities I commonly use.

## Add-ons

- Positive Y Camera
  - Add a camera at origin facing positive Y
- Camera Utils
  - Position cameras using "Mouse look" controls
- "Pre-flight" Checklist system
  - Runs automated unit tests on your scenes and attempts to fix any issues found
  - DCC-agnostic

## Using with Blender

Just clone this repo, and add it as your scripts directory in `Edit > Preferences > File Paths > Scripts`. All add-ons will show up in the add-ons menu.

You will also need PySide2 installed on your system.
