#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from datetime import datetime

def print_colored(text, color_code):
    """Print colored text to terminal."""
    print(f"\033[{color_code}m{text}\033[0m")

def print_green(text):
    print_colored(text, "0;32")

def print_red(text):
    print_colored(text, "0;31")

def print_yellow(text):
    print_colored(text, "1;33")

def check_git_installed():
    """Check if git is installed on the system."""
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_repo_stats(repo_path):
    """Get statistics about the cloned repository."""
    file_count = 0
    dir_count = 0
    
    for root, dirs, files in os.walk(repo_path):
        file_count += len(files)
        dir_count += len(dirs)
    
    return file_count, dir_count

def main():
    """Main function to clone a GitHub repository."""
    print("=" * 56)
    print("    GitHub Repository Cloning Tool (Python Version)")
    print("=" * 56)
    
    # Repository URL
    repo_url = "https://github.com/sgmoh/multipurpos"
    
    # Default destination directory
    default_dest = os.path.join(os.getcwd(), "multipurpos")
    
    # Use default destination without asking
    dest_dir = default_dest
    print(f"Using destination directory: {dest_dir}")
    
    # Check if git is installed
    if not check_git_installed():
        print_red("Error: Git is not installed.")
        print("Please install Git first:")
        print("  - Ubuntu/Debian: sudo apt-get install git")
        print("  - Fedora: sudo dnf install git")
        print("  - macOS: brew install git")
        print("  - Windows: Download from https://git-scm.com/download/win")
        return 1
    
    print_yellow(f"Cloning repository from: {repo_url}")
    print_yellow(f"To: {dest_dir}")
    
    # Check if destination directory exists and is not empty
    if os.path.exists(dest_dir) and os.listdir(dest_dir):
        print_red("Destination directory exists and is not empty!")
        print_yellow("Removing existing directory...")
        shutil.rmtree(dest_dir)
    
    # Clone the repository
    print("Cloning repository, please wait...")
    
    try:
        result = subprocess.run(
            ["git", "clone", repo_url, dest_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        print_green("Repository successfully cloned!")
        
        # Get repository statistics
        file_count, dir_count = get_repo_stats(dest_dir)
        
        print_yellow("Repository Statistics:")
        print(f"  - Files: {file_count}")
        print(f"  - Directories: {dir_count}")
        
        # Show repository structure
        print_yellow("Repository Structure:")
        files = os.listdir(dest_dir)
        for file in files:
            file_path = os.path.join(dest_dir, file)
            if os.path.isdir(file_path):
                print(f"  📁 {file}/")
            else:
                print(f"  📄 {file}")
        
        print_green("\nYou can now navigate to the repository:")
        print(f"  cd {dest_dir}")
        
        # Check for common project files
        if os.path.exists(os.path.join(dest_dir, "package.json")):
            print_yellow("\nThis appears to be a Node.js project.")
            print("You may want to install dependencies:")
            print(f"  cd {dest_dir} && npm install")
        
        if os.path.exists(os.path.join(dest_dir, "requirements.txt")):
            print_yellow("\nThis appears to be a Python project.")
            print("You may want to install dependencies:")
            print(f"  cd {dest_dir} && pip install -r requirements.txt")
        
        print_green("\nHappy coding!")
        return 0
        
    except subprocess.CalledProcessError as e:
        print_red("Failed to clone repository.")
        print("Error details:")
        print(e.stderr)
        print("\nPlease check:")
        print("  - Your internet connection")
        print("  - That the repository URL is correct")
        print("  - That you have necessary permissions")
        return 1

if __name__ == "__main__":
    sys.exit(main())
