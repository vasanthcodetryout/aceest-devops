import sys
import os

# Add the project root directory to Python's path
# This allows pytest to find app.py when running from any directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
