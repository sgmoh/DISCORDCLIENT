#!/bin/bash

# Script to clone the multipurpos GitHub repository
# Author: AI Assistant
# Date: 2023

# Colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================================"
echo "    GitHub Repository Cloning Tool"
echo "========================================================"

# Repository URL
REPO_URL="https://github.com/sgmoh/multipurpos"

# Get current directory as default destination
DEFAULT_DEST="./multipurpos"

# Ask user for destination directory or use default
read -p "Enter destination directory (default: $DEFAULT_DEST): " DEST_DIR
DEST_DIR=${DEST_DIR:-$DEFAULT_DEST}

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is not installed.${NC}"
    echo "Please install Git first:"
    echo "  - Ubuntu/Debian: sudo apt-get install git"
    echo "  - Fedora: sudo dnf install git"
    echo "  - macOS: brew install git"
    echo "  - Windows: Download from https://git-scm.com/download/win"
    exit 1
fi

echo -e "${YELLOW}Cloning repository from: ${NC}$REPO_URL"
echo -e "${YELLOW}To: ${NC}$DEST_DIR"

# Check if destination directory exists and is not empty
if [ -d "$DEST_DIR" ] && [ "$(ls -A $DEST_DIR 2>/dev/null)" ]; then
    echo -e "${RED}Destination directory exists and is not empty!${NC}"
    read -p "Would you like to overwrite it? (y/n): " OVERWRITE
    if [[ $OVERWRITE == "y" || $OVERWRITE == "Y" ]]; then
        echo -e "${YELLOW}Removing existing directory...${NC}"
        rm -rf "$DEST_DIR"
    else
        echo "Cloning aborted."
        exit 1
    fi
fi

# Clone the repository
echo "Cloning repository, please wait..."
if git clone "$REPO_URL" "$DEST_DIR"; then
    echo -e "${GREEN}Repository successfully cloned!${NC}"
    
    # Count number of files and directories
    FILE_COUNT=$(find "$DEST_DIR" -type f | wc -l)
    DIR_COUNT=$(find "$DEST_DIR" -type d | wc -l)
    
    echo -e "${YELLOW}Repository Statistics:${NC}"
    echo "  - Files: $FILE_COUNT"
    echo "  - Directories: $DIR_COUNT"
    
    # Show repository structure (first two levels)
    echo -e "${YELLOW}Repository Structure:${NC}"
    ls -la "$DEST_DIR"
    
    echo -e "\n${GREEN}You can now navigate to the repository:${NC}"
    echo "  cd $DEST_DIR"
    
    # Check if there's a package.json or requirements.txt
    if [ -f "$DEST_DIR/package.json" ]; then
        echo -e "\n${YELLOW}This appears to be a Node.js project.${NC}"
        echo "You may want to install dependencies:"
        echo "  cd $DEST_DIR && npm install"
    fi
    
    if [ -f "$DEST_DIR/requirements.txt" ]; then
        echo -e "\n${YELLOW}This appears to be a Python project.${NC}"
        echo "You may want to install dependencies:"
        echo "  cd $DEST_DIR && pip install -r requirements.txt"
    fi
    
    echo -e "\n${GREEN}Happy coding!${NC}"
else
    echo -e "${RED}Failed to clone repository.${NC}"
    echo "Please check:"
    echo "  - Your internet connection"
    echo "  - That the repository URL is correct"
    echo "  - That you have necessary permissions"
    exit 1
fi

exit 0
