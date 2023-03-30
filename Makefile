.EXPORT_ALL_VARIABLES:
PROJECT=todo
BUCKET=todo
PROFILE=default
DATA_FOLDER=data

## Create virtual environment
venv:
	python3 -m venv venv
	source venv/bin/activate ; pip install --upgrade pip ; python3 -m pip install -r requirements-dev.txt
	source venv/bin/activate ; pip freeze > requirements_freeze.txt

## Clean virtual environment
clean:
	rm -rf venv

## Run the app
run:
	source venv/bin/activate ; PYTHONPATH='./src' python -m app req1 --optional-arg opt1

## App help message
run_help:
	source venv/bin/activate ; PYTHONPATH='./src' python -m app --help

## Run jupyter lab
jupyter:
	source venv/bin/activate; PYTHONPATH='./src' jupyter lab

## Run unit tests
test:
	source venv/bin/activate ; PYTHONPATH='./src' pytest -vvv -s

## Run black code formatter
black:
	source venv/bin/activate ; black  --line-length 120 .

## Run flake8 linter
flake8:
	source venv/bin/activate ; flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	source venv/bin/activate ; flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

## Upload Data to S3
sync_data_to_s3:
	aws s3 sync $(DATA_FOLDER)/ s3://$(BUCKET)/$(PROJECT)/ --profile $(PROFILE) --exclude ".*"

## Download Data from S3
sync_data_from_s3:
	aws s3 sync s3://$(BUCKET)/$(PROJECT)/ $(DATA_FOLDER)/ --profile $(PROFILE) --exclude ".*"

## Self documenting commands
.DEFAULT_GOAL := help
.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
