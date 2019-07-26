#!/bin/bash
PYTHON=$(echo -ne "#!$(which python3)")
PATH_TO_INSTALL=$(dirname $(which python3))
echo 'Running sudo commands...'
sudo printf '%s\n' $PYTHON | cat - masksorter.py > $PATH_TO_INSTALL/masksorter
sudo chmod +x $PATH_TO_INSTALL/masksorter
echo "Installed to $PATH_TO_INSTALL/"
