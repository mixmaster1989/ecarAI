"""Create directory structure for ИКАР-Ассистент 3.0."""

import os

# Define the directory structure
dirs = [
    'ikar3',
    'ikar3/core',
    'ikar3/ui',
    'ikar3/ui/components',
    'ikar3/ui/themes',
    'ikar3/ai',
    'ikar3/ai/models',
    'ikar3/ai/engines',
    'ikar3/web',
    'ikar3/audio',
    'ikar3/data',
    'ikar3/assets',
    'ikar3/assets/icons',
    'ikar3/assets/sounds',
    'ikar3/assets/animations',
    'ikar3/plugins'
]

# Create directories
base_dir = os.path.dirname(os.path.abspath(__file__))
for directory in dirs:
    path = os.path.join(base_dir, directory.replace('/', os.sep))
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")

print("\nDirectory structure for ИКАР-Ассистент 3.0 created successfully!")