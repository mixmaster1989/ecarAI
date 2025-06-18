"""Status checker for ИКАР-Ассистент."""

import os
import sys
import time
import importlib
import sqlite3
from pathlib import Path

def check_directories():
    """Check if all required directories exist."""
    print("Checking directories...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    required_dirs = [
        os.path.join(base_dir, "ikar"),
        os.path.join(base_dir, "ikar", "logs"),
        os.path.join(base_dir, "ikar", "data"),
        os.path.join(base_dir, "ikar", "models"),
        os.path.join(base_dir, "ikar", "cache"),
        os.path.join(base_dir, "ikar", "assets"),
        os.path.join(base_dir, "ikar", "ui")
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"+ {directory} exists")
        else:
            print(f"- {directory} missing")
            all_exist = False
    
    return all_exist

def check_database():
    """Check if the database is accessible."""
    print("\nChecking database...")
    
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ikar', 'data', 'ikar_history.db')
    
    if not os.path.exists(db_path):
        print(f"- Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        print(f"+ Database connected successfully")
        print(f"+ Found {len(tables)} tables")
        return True
    except Exception as e:
        print(f"- Database error: {e}")
        return False

def check_modules():
    """Check if all required modules can be imported."""
    print("\nChecking modules...")
    
    modules = [
        "ikar.config",
        "ikar.database",
        "ikar.ai_engine",
        "ikar.web_search",
        "ikar.audio",
        "ikar.ui.styles",
        "ikar.ui.widgets",
        "ikar.main"
    ]
    
    all_imported = True
    for module_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"+ {module_name} imported successfully")
        except ImportError as e:
            print(f"- {module_name} import error: {e}")
            all_imported = False
    
    return all_imported

def check_ai_model():
    """Check if AI model can be loaded."""
    print("\nChecking AI model...")
    
    try:
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from ikar.ai_engine import ai_engine
        
        print("+ AI engine imported successfully")
        
        # Wait for model to load (with timeout)
        print("Waiting for model to load (max 10 seconds)...")
        start_time = time.time()
        while not ai_engine.is_ready() and time.time() - start_time < 10:
            time.sleep(0.5)
        
        if ai_engine.is_ready():
            print("+ AI model loaded successfully")
            return True
        else:
            print("- AI model not loaded within timeout")
            return False
    except Exception as e:
        print(f"- AI engine error: {e}")
        return False

def main():
    """Run all checks."""
    print("=== ИКАР-Ассистент Status Check ===\n")
    
    dirs_ok = check_directories()
    db_ok = check_database()
    modules_ok = check_modules()
    ai_ok = check_ai_model()
    
    print("\n=== Summary ===")
    print(f"Directories: {'OK' if dirs_ok else 'FAILED'}")
    print(f"Database: {'OK' if db_ok else 'FAILED'}")
    print(f"Modules: {'OK' if modules_ok else 'FAILED'}")
    print(f"AI Model: {'OK' if ai_ok else 'FAILED'}")
    
    all_ok = dirs_ok and db_ok and modules_ok and ai_ok
    print(f"\nOverall status: {'OK' if all_ok else 'ISSUES DETECTED'}")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())