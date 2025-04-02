#!/bin/bash

# Define the URL and the destination file
URL="https://go.microsoft.com/fwlink/?linkid=853070"
PKG_FILE="CompanyPortal-Installer.pkg"
APP_NAME="Company Portal.app"

# Download the CompanyPortal.pkg
echo "Downloading $PKG_FILE..."
curl -L -o "$PKG_FILE" "$URL"

# Check if the download was successful
if [ $? -ne 0 ]; then
    echo "Failed to download $PKG_FILE. Please download it manually from: $URL"
    exit 1
fi

# Install the application
echo "Installing $APP_NAME..."
sudo installer -pkg "$PKG_FILE" -target /

# Check if the installation was successful
if [ $? -ne 0 ]; then
    echo "Failed to install $APP_NAME"
    exit 1
fi

# Open the application
echo "Opening $APP_NAME..."
open "/Applications/$APP_NAME"

# Bring the application to the front
osascript -e "tell application \"$APP_NAME\" to activate"

sudo rm CompanyPortal-Installer.pkg 
echo "Process completed successfully."
