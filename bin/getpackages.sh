#!/bin/bash
# Get Loaded Packages Script

pathfilepath=$1
savepath=$2
cd $pathfilepath
source venv/bin/activate
pip3 list > $savepath
deactivate

