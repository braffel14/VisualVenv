#!/bin/bash
# Create a new venv at projectpath location

projectpath=$1

cd $projectpath
python3 -m venv venv
source venv/bin/activate
deactivate
