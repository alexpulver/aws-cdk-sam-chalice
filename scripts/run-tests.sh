#!/bin/bash

set -o errexit
set -o verbose

targets=(api database monitoring app.py pipeline.py stacks.py stages.py)

bandit --recursive "${targets[@]}"
black --check --diff "${targets[@]}"
flake8 --config .flake8 "${targets[@]}"
isort --settings-path .isort.cfg --check --diff "${targets[@]}"
mypy --config-file .mypy.ini api database monitoring  # Splitting commands due to https://github.com/python/mypy/issues/4008
mypy --config-file .mypy.ini app.py pipeline.py stacks.py stages.py
pylint --rcfile .pylintrc "${targets[@]}"
safety check -r api/runtime/requirements.txt -r requirements.txt -r requirements-dev.txt

PYTHONPATH="${PWD}/api/runtime" \
  coverage run --source "${PWD}" --omit "tests/*" -m unittest discover -v -s tests
