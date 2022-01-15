bl_info = {
    "name": "Better Camera Rotation",
    "author": "Evan Pratten <ewpratten@gmail.com>",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "description": "Adds better rotation controls for cameras",
    "category": "Camera",
}


import bpy


def register():
    print("[BCR] Registering")

def unregister():
    print("[BCR] Unregistering")


if __name__ == "__main__":
    register()
