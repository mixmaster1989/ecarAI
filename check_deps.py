"""Check and install dependencies for ИКАР-Ассистент."""

import sys
import subprocess
import pkg_resources
import os

def check_and_install_dependencies():
    """Check and install required dependencies."""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if not os.path.exists(requirements_file):
        print("Error: requirements.txt not found.")
        return False
    
    # Read requirements
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Check which packages need to be installed
    missing = []
    for requirement in requirements:
        # Remove version specifiers
        package = requirement.split('>=')[0].split('==')[0].split('>')[0].split('<')[0].strip()
        try:
            pkg_resources.get_distribution(package)
            print(f"+ {package} is already installed")
        except pkg_resources.DistributionNotFound:
            print(f"- {package} needs to be installed")
            missing.append(requirement)
    
    # Install missing packages
    if missing:
        print(f"\nInstalling {len(missing)} missing packages...")
        for package in missing:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"+ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"- Failed to install {package}")
                return False
    
    return True

if __name__ == "__main__":
    print("Checking dependencies for ИКАР-Ассистент...")
    if check_and_install_dependencies():
        print("\nAll dependencies are installed!")
        sys.exit(0)
    else:
        print("\nFailed to install all dependencies.")
        sys.exit(1)