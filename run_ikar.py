#!/usr/bin/env python
"""Launcher script for ИКАР-Ассистент."""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ikar', 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(logs_dir, 'ikar.log'), 
                           mode='a', 
                           encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import PyQt5
        import pyttsx3
        import pygame
        import transformers
        import torch
        import duckduckgo_search
        import requests
        import bs4
        import sentence_transformers
        
        logger.info("All dependencies are installed.")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print(f"Error: Missing dependency: {e}")
        print("Please install all required dependencies with: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories if they don't exist."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ikar_dir = os.path.join(base_dir, 'ikar')
    
    dirs = [
        os.path.join(ikar_dir, 'data'),
        os.path.join(ikar_dir, 'logs'),
        os.path.join(ikar_dir, 'models'),
        os.path.join(ikar_dir, 'cache'),
        os.path.join(ikar_dir, 'assets')
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    
    logger.info("Directory structure verified.")

def main():
    """Main entry point."""
    logger.info("Starting ИКАР-Ассистент...")
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Create directories
    create_directories()
    
    # Import and run the application
    try:
        from ikar.main import main as run_app
        return run_app()
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        print(f"Error starting application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())