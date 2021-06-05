#!/bin/bash

set -o errexit
set -o verbose

# Install local CDK CLI version
npm install

# Install project dependencies
pip install pip-tools==6.1.0
pip-sync api/runtime/requirements.txt requirements.txt requirements-dev.txt
