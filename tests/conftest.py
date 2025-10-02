import os
import sys

# Ensure the project's src directory is on sys.path for test discovery when running
# under tools that don't install the package in editable mode.
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
