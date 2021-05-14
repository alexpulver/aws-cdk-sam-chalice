#!/bin/bash

set -o errexit
set -o verbose

python -m unittest discover --start-directory tests
