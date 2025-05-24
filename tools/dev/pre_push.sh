#!/bin/bash

# Run from command line with ./tools/dev/pre_push.sh  (requires chmod +x)

lt_yellow   () { printf "\e[33m"      ; "$@" ; printf "\e[0m"; }
dk_green    () { printf "\e[38;5;35m" ; "$@" ; printf "\e[0m"; }
purple      () { printf "\e[35m"      ; "$@" ; printf "\e[0m"; }

purple echo 'Running pre-push checks...' && \

lt_yellow echo 'Running prospector checks for information about errors, potential problems, convention violations and complexity...' && \
prospector  --max-line-length 120 --output-format pylint && \

lt_yellow echo 'Running mypy static type checks...' && \
mypy && \

lt_yellow echo 'Bandit is checking for security issues...' && \
bandit -r -q . -x ./.venv,./.aws-sam/ --format screen && \

lt_yellow echo 'Running unit tests:' && \
coverage run --branch --source=./ -m pytest tests && \

lt_yellow echo 'Coverage report (fails under 100%)...' && \
coverage report -m --fail-under=100 --omit=.venv && \

purple echo 'Pre-push checks complete.'

