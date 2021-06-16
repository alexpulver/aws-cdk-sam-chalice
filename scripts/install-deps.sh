#!/bin/bash

set -o errexit
set -o verbose

# Install local CDK CLI version
npm install

# Install project dependencies
pip install -r api/runtime/requirements.txt -r requirements.txt -r requirements-dev.txt
