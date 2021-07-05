#!/bin/bash

set -o errexit
set -o verbose

_targets=(api database monitoring app.py deployment.py pipeline.py)

bandit --recursive "${_targets[@]}"
black --check --diff "${_targets[@]}"
flake8 --config .flake8 "${_targets[@]}"
isort --settings-path .isort.cfg --check --diff "${_targets[@]}"
mypy --config-file .mypy.ini api database monitoring  # Splitting commands due to https://github.com/python/mypy/issues/4008
mypy --config-file .mypy.ini app.py deployment.py pipeline.py
pylint --rcfile .pylintrc "${_targets[@]}"
safety check -r api/runtime/requirements.txt -r requirements.txt -r requirements-dev.txt

coverage run --rcfile .coveragerc -m unittest discover --start-directory tests
