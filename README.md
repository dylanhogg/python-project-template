# Python project template

[![Latest Tag](https://img.shields.io/github/v/tag/dylanhogg/python-project-template)](https://github.com/dylanhogg/python-project-template/tags)
[![Build](https://github.com/dylanhogg/python-project-template/workflows/build/badge.svg)](https://github.com/dylanhogg/python-project-template/actions)

A quick start Python project template with some useful functionality, some standard packages and a GitHub build action.


## Makefile support for common tasks

1) `make venv` to create an isolated virtual environment (using [venv](https://docs.python.org/3/library/venv.html)) and install common packages
2) `make run` to run the main app in venv with appropriate paths set
3) `make jupyter` to launch [jubyter lab](https://jupyterlab.readthedocs.io/) with `/notebooks` root folder but still retaining notebook access to the parent `/src` and `/log` folders 
4) `make test` to run unit tests
5) `make black` to format code and `make flake8` for linting  
6) `make sync_data_to_s3` and `make sync_data_from_s3` to sync data with an s3 bucket

Type `make` for all commands.


## Application libraries included in template

1) https://github.com/theskumar/python-dotenv for environment variable management   
2) https://github.com/sphinx-doc/sphinx to create documentation  
3) https://github.com/tiangolo/typer for building CLI applications  
4) https://github.com/tqdm/tqdm for smart progress bar support  
5) https://github.com/Delgan/loguru for pleasant and powerful logging  


## Development libraries included in template

1) https://github.com/pytest-dev/pytest for writing your tests   
2) https://github.com/psf/black for code formatting  
3) https://github.com/pycqa/flake8 for code style linting  
4) https://github.com/jupyterlab/jupyterlab for notebooks  


## Other Python templates for inspiration/alternatives

1) https://github.com/TezRomacH/python-package-template
2) https://github.com/drivendata/cookiecutter-data-science
3) https://github.com/crmne/cookiecutter-modern-datascience


## Improvements

1) More GitHub actions
2) Replace requirements with [Poetry](https://python-poetry.org/)
3) Investigate adding static Typing checking, e.g. [mypy](https://github.com/python/mypy)
4) Turn into a [cookiecutter](https://cookiecutter.readthedocs.io/) template
5) Add more examples in `/src/examples`
