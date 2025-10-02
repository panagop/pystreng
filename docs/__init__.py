import os
import sys

# When MkDocs imports modules from docs/ during build, ensure the project's src
# directory is on sys.path so mkdocstrings can import the package.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)
