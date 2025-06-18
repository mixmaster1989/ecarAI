import os

# Create directory structure
dirs = [
    'ikar/logs',
    'ikar/data',
    'ikar/models',
    'ikar/cache',
    'ikar/assets'
]

for directory in dirs:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory.replace('/', os.sep))
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")

# Create empty __init__.py in logs directory
logs_init = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ikar', 'logs', '__init__.py')
with open(logs_init, 'w') as f:
    f.write('"""Logs directory for ИКАР-Ассистент."""\n')

print(f"Created file: {logs_init}")