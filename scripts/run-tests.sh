#!/bin/bash

set -o errexit
set -o verbose

targets=(api database monitoring app.py constants.py deployment.py pipeline.py)

bandit --recursive "${targets[@]}"
black --check --diff "${targets[@]}"
flake8 --config .flake8 "${targets[@]}"
isort --settings-path .isort.cfg --check --diff "${targets[@]}"
# mypy: split commands due to https://github.com/python/mypy/issues/4008
mypy --config-file .mypy.ini "${targets[@]:0:3}"
mypy --config-file .mypy.ini "${targets[@]:3:4}"
pylint --rcfile .pylintrc "${targets[@]}"
# safety: ignore coverage 5.5 (41002) report, no issues per Snyk: https://snyk.io/advisor/python/coverage
safety check \
  -i 41002 \
  -r api/runtime/requirements.txt \
  -r requirements.txt \
  -r requirements-dev.txt
# Report code complexity
radon mi "${targets[@]}"
# Exit with non-zero status if code complexity exceeds thresholds
xenon --max-absolute A --max-modules A --max-average A "${targets[@]}"

PYTHONPATH="${PWD}/api/runtime" \
  coverage run --source "${PWD}" --omit ".venv/*,tests/*" -m unittest discover -v -s tests
