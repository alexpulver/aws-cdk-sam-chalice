#!/bin/bash

set -o errexit
set -o verbose

targets=(api database monitoring app.py deployment.py pipeline.py)

bandit --recursive "${targets[@]}"
black --check --diff "${targets[@]}"
flake8 --config .flake8 "${targets[@]}"
isort --settings-path .isort.cfg --check --diff "${targets[@]}"
# mypy: split commands due to https://github.com/python/mypy/issues/4008
mypy --config-file .mypy.ini api database monitoring
mypy --config-file .mypy.ini app.py deployment.py pipeline.py
pylint --rcfile .pylintrc "${targets[@]}"
# safety: ignore coverage 5.5 (41002) report, no issues per Snyk: https://snyk.io/advisor/python/coverage
safety check \
  -i 41002 \
  -r api/runtime/requirements.txt \
  -r requirements.txt \
  -r requirements-dev.txt

PYTHONPATH="${PWD}/api/runtime" \
  coverage run --source "${PWD}" --omit ".venv/*,tests/*" -m unittest discover -v -s tests
