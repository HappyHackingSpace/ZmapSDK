#!/bin/bash
# Script to build and install the package using modern tooling

echo "Building and installing zmap-sdk package using pyproject.toml"

# Make sure build is installed
python -m pip install --upgrade pip build twine

# Build the package
echo "Building package..."
python -m build

# Install the package
echo "Installing package..."
python -m pip install -e .

echo "Build and installation complete!" 