#!/usr/bin/env python
"""Build script for ИКАР-Ассистент."""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Build ИКАР-Ассистент")
    parser.add_argument("--onefile", action="store_true", help="Build as a single file")
    parser.add_argument("--name", default="ИКАР-Ассистент", help="Name of the output file")
    parser.add_argument("--icon", default="ikar/assets/icon.ico", help="Path to icon file")
    parser.add_argument("--no-console", action="store_true", help="Hide console window")
    return parser.parse_args()

def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller."""
    print("Installing PyInstaller...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_assets():
    """Create necessary asset files if they don't exist."""
    assets_dir = os.path.join("ikar", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Create placeholder files if they don't exist
    placeholder_files = {
        "ambient.mp3": "Placeholder for ambient music",
        "notification.mp3": "Placeholder for notification sound",
        "startup.mp3": "Placeholder for startup sound",
        "icon.ico": None  # Will be created as a binary file
    }
    
    for filename, content in placeholder_files.items():
        filepath = os.path.join(assets_dir, filename)
        if not os.path.exists(filepath):
            if content is None:
                # Create a simple icon file
                try:
                    from PIL import Image
                    img = Image.new('RGB', (256, 256), color=(53, 132, 228))
                    img.save(filepath)
                    print(f"Created placeholder icon: {filepath}")
                except ImportError:
                    print("PIL not installed, skipping icon creation")
            else:
                with open(filepath, "w") as f:
                    f.write(content)
                print(f"Created placeholder file: {filepath}")

def build_executable(args):
    """Build the executable."""
    print(f"Building {args.name}...")
    
    # Create assets
    create_assets()
    
    # Base command
    cmd = [
        "pyinstaller",
        "--name", args.name,
        "--clean",
        "--noconfirm",
    ]
    
    # Add onefile option if specified
    if args.onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    
    # Add windowed option if specified
    if args.no_console:
        cmd.append("--windowed")
    
    # Add icon if it exists
    if os.path.exists(args.icon):
        cmd.extend(["--icon", args.icon])
    
    # Add data files
    cmd.extend([
        "--add-data", f"ikar/assets;ikar/assets",
    ])
    
    # Add the main script
    cmd.append("run_ikar.py")
    
    # Execute build
    print("Running PyInstaller with command:")
    print(" ".join(cmd))
    subprocess.call(cmd)
    
    print("\nBuild completed!")
    if args.onefile:
        print(f"Executable is located at: dist/{args.name}.exe")
    else:
        print(f"Application folder is located at: dist/{args.name}/")

def main():
    """Main entry point."""
    args = parse_args()
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller is not installed.")
        install_pyinstaller()
    
    # Build the executable
    build_executable(args)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())