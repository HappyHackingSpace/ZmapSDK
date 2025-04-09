#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Python package build process...${NC}"

# Check if Python and required tools are installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install it first.${NC}"
    exit 1
fi

# Create and activate a virtual environment
echo -e "${GREEN}Creating a virtual environment...${NC}"
VENV_DIR=".venv"

# Check if python3-venv or python-venv is installed
if ! python3 -m venv $VENV_DIR 2>/dev/null; then
    echo -e "${RED}Failed to create virtual environment. Installing python3-venv...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt install -y python3-venv
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-venv
    else
        echo -e "${RED}Please install python3-venv package for your distribution.${NC}"
        exit 1
    fi
    python3 -m venv $VENV_DIR
fi

# Source the virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
else
    source "$VENV_DIR/Scripts/activate"  # For Windows
fi

# Install required packaging tools in the virtual environment
echo -e "${GREEN}Installing required packaging tools in virtual environment...${NC}"
pip install --upgrade pip build twine

# Clean previous builds
echo -e "${GREEN}Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info/

# Run tests if they exist
if [ -d "tests" ]; then
    echo -e "${GREEN}Running tests...${NC}"
    python -m unittest discover
fi

# Build the package using modern build tool
echo -e "${GREEN}Building package...${NC}"
python -m build

# Check the package
echo -e "${GREEN}Checking package with twine...${NC}"
twine check dist/*

# Upload to PyPI
echo -e "${GREEN}Ready to upload to PyPI.${NC}"
read -p "Do you want to upload to PyPI? (y/n): " upload_answer

if [[ $upload_answer == "y" || $upload_answer == "Y" ]]; then
    echo -e "${GREEN}Uploading to PyPI...${NC}"
    twine upload dist/*
    echo -e "${GREEN}Upload complete!${NC}"
else
    echo -e "${GREEN}Upload skipped. Package files are available in the 'dist' directory.${NC}"
fi

# Deactivate the virtual environment
deactivate

echo -e "${GREEN}All done!${NC}"
