#!/usr/bin/env python
"""Launcher script for ИКАР-Ассистент 3.0."""

import os
import sys
import logging
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create necessary directories
base_dir = os.path.dirname(os.path.abspath(__file__))
ikar_dir = os.path.join(base_dir, 'ikar3')
dirs = [
    os.path.join(ikar_dir, 'data'),
    os.path.join(ikar_dir, 'data', 'logs'),
    os.path.join(ikar_dir, 'data', 'cache'),
    os.path.join(ikar_dir, 'assets', 'sounds'),
    os.path.join(ikar_dir, 'assets', 'icons'),
    os.path.join(ikar_dir, 'assets', 'animations')
]

for directory in dirs:
    os.makedirs(directory, exist_ok=True)

# Configure logging
log_dir = os.path.join(ikar_dir, 'data', 'logs')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(log_dir, 'ikar.log'), mode='a', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import PyQt5
        import pygame
        import pyttsx3
        import transformers
        import torch
        import duckduckgo_search
        import requests
        import bs4
        import numpy
        
        logger.info("All dependencies are installed.")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print(f"Error: Missing dependency: {e}")
        print("Please install all required dependencies with: pip install -r requirements.txt")
        return False

def show_console_splash():
    """Show a simple console splash screen."""
    splash = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║                  ИКАР-АССИСТЕНТ 3.0                      ║
    ║                                                          ║
    ║          Интеллектуальный помощник сервисного            ║
    ║              инженера ККТ и 1С                           ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(splash)
    print("Загрузка компонентов...")

def main():
    """Main entry point."""
    show_console_splash()
    
    logger.info("Starting ИКАР-Ассистент 3.0...")
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Import and run the application
    try:
        from ikar3.main import main as run_app
        return run_app()
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        print(f"Error starting application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())