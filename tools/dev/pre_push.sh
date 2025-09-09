#!/bin/bash

# Run from command line with ./tools/dev/pre_push.sh  (requires chmod +x)

purple      () { printf "\e[35m"      ; "$@" ; printf "\e[0m"; }

purple echo 'Running pre-push checks...' && echo && \

purple echo 'Running ruff code quality checks for information about errors, potential problems, convention violations and complexity...' && \
ruff check . && echo && \

purple echo 'Running mypy static type checks...' && \
mypy && echo && \

purple echo 'Bandit is checking for security issues...' && \
bandit -r -q . -x ./.venv,./.aws-sam/ --format screen && echo && \

purple echo 'Running unit tests:' && \
coverage run --branch --source=./ -m pytest tests && echo && \

purple echo 'Coverage report (fails under 100%)...' && \
coverage report -m --fail-under=100 --omit=.venv && echo && \

purple echo 'Pre-push checks complete.'

