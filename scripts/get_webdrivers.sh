#!/usr/bin/env bash

#############
#
# This script downloads the Chrome webdrivers for Selenium needed for the functioning of the backend.
# It currently runs on Linux or OSX.
#
# You can pass a specific Chrome version number (only the major, like "89", not the complete release number) if
# you don't use the latest release.
#
# bash ./scripts/get_webdrivers.sh [CHROME_VERSION]
#
#############

OS="linux"
RELEASE="LATEST_RELEASE"

# 1. Check for dependencies of this script depending on the OS
if [ "$(uname)" == "Darwin" ]; then
  # Mac OS X platform
  OS="mac"

  if [ ! $(which wget) ] || [ ! $(which unzip) ]; then
    echo "Make sure you have both wget and unzip installed."
    echo "If you use 'brew', try the following commands:"
    echo "brew install wget"
    echo "brew install unzip"
    exit 2
  fi
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  # GNU/Linux platform
  if [ ! $(which wget) ] || [ ! $(which unzip) ]; then
    echo "Make sure you have both wget and unzip installed."
    echo "If you use 'apt', try the following command:"
    echo "apt install wget unzip"
    exit 2
  fi
else
  echo "This script does not support your operating system. Run on OSX or Linux."
  exit 1
fi

# 2. Find the release number for the Chrome driver
if [ $1 ]; then
  RELEASE="LATEST_RELEASE_$1"
fi

# Find the local chrome version
VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/${RELEASE})
echo "Downloading chrome driver ${RELEASE}"

# 3. Download chromedriver
wget -q "https://chromedriver.storage.googleapis.com/${VERSION}/chromedriver_${OS}64.zip" -O driver.zip

# 4. Unzip and make it executable
unzip driver.zip
chmod +x chromedriver

# 5. Move to the desired location
if [ ! -d "./backend/webdrivers" ]; then
  mkdir ./backend/webdrivers
fi
mv chromedriver ./backend/webdrivers/chromedriver_${OS}

# 6. Cleanup
rm driver.zip