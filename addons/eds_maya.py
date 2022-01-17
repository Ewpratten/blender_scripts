"""Entrypoint for Maya to load EDS

Maya's plugin system looks for .py files in the root of a plugin directory.
This script will add `./eds` to the python path, then load it as a sub-module.
"""
import os

# We need to pull in mel so we can query the plugin path
import maya.mel as mel
maya_plugin_path = mel.eval("getenv MAYA_PLUG_IN_PATH").split(":")
print(f"[EDS Maya Bootstrap] Plugin path has {len(maya_plugin_path)} entries")

# With our list of plugin roots, we need to search through them until we find one that contains the eds module
for plugin_root in maya_plugin_path:
    print(f"[EDS Maya Bootstrap] Checking {plugin_root} for main EDS module")
    eds_path = os.path.join(plugin_root, "eds")
    if os.path.exists(eds_path):
        print(f"[EDS Maya Bootstrap] Found eds at {eds_path}")
        break
else:
    raise RuntimeError("[EDS Maya Bootstrap] Could not find EDS in Maya's plugin path")


# Add the parent of the eds module to the python path
import sys
sys.path.append(os.path.join(eds_path, ".."))

# We also require pymel. If it is not accessible, we can load it from git
try:
    print("[EDS Maya Bootstrap] Attempting to import pymel from the DCC python path")
    import pymel
except ImportError as e:
    print("[EDS Maya Bootstrap] Could not import pymel. Loading vendored version instead")

    # We need to import pymel from the vendored version
    pymel_path = os.path.join(eds_path, "../../third_party/pymel")
    print(f"[EDS Maya Bootstrap] Using the following path for pymel: {pymel_path}")
    sys.path.append(pymel_path)

    # Now we can import pymel
    import pymel

# Now we can import the eds module
from eds.dcc.maya import initializePlugin, uninitializePlugin