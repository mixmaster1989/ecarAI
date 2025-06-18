"""Test script to verify imports."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    # Import core modules
    from ikar import config
    print("+ Config module imported")
    
    from ikar import database
    print("+ Database module imported")
    
    from ikar.ui import styles
    print("+ UI styles module imported")
    
    from ikar.ui import widgets
    print("+ UI widgets module imported")
    
    print("\nAll modules imported successfully!")
    print("The application should now be able to start.")
    
except ImportError as e:
    print(f"X Import error: {e}")
    print("\nPlease fix the error and try again.")