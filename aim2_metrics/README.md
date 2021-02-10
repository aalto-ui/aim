# AIM 2 Metrics

AIM 2 Metrics is a subproject of Aalto Interface Metrics (AIM). The subproject contains old and new metrics that are compatible with Python 3 and have been rigorously tested. The metrics will be incorporated into the next major release of AIM (version 2), to be published in 2021.


## Requirements

You need [Python 3.7](https://www.python.org/) (or later), [pip](https://pypi.org/project/pip/), and [git](https://git-scm.com/) to work on this subproject.

In addition, it is highly recommended to install [virtualenv](https://virtualenv.pypa.io/) or [Pipenv](https://pypi.org/project/pipenv/) to create a dedicated Python virtual environment. You can find more information on this below.


## Installation

Clone the AIM git repository and head over to the [aim2_metrics](./aim2_metrics/) directory (this subproject):
```
git clone https://github.com/aalto-ui/aim.git && cd aim/aim2_metrics
```

### Working with `virtualenv`

Create a new virtual environment:
```
virtualenv venv
```

Activate the virtual environment:
```
source venv/bin/activate
```

Install all dependencies, including development packages:
```
pip install -r requirements.txt
```

To deactivate the virtual environment, run:
```
deactivate
```

### Working with `Pipenv`

Install all dependencies, including development packages:
```
pipenv install --dev
```

Activate your Pipenv environment:
```
pipenv shell
```

To deactivate your Pipenv environment, run:
```
exit
```


## Tests

This subproject uses [pytest](https://pytest.org/), a Python testing framework to run tests on source code, including metrics.

### Configuration

Configure pytest, if needed:
```
nano pytest.ini
```

### Usage

Run all tests:
```
pytest .
```

Run a specific test file:
```
pytest [FILEPATH]
```


## Utility Tools

This subproject supports the following utility tools to ease development. Their installation and use is optional, but highly recommended.

- **isort.** Python utility to automatically sort imports. https://timothycrosley.github.io/isort/
- **Black.** Python code formatter. https://github.com/psf/black
- **Mypy.** Static type checker for Python. http://mypy-lang.org/
- **Flake8.** Python tool for style guide enforcement. https://flake8.pycqa.org/en/latest/
- **pre-commit.** Package manager for pre-commit hooks. https://pre-commit.com/ 

### Installation

Install pre-commit into your git hooks:
```
pre-commit install --install-hooks --overwrite
```

To uninstall pre-commit from your git hooks, run:
```
pre-commit uninstall
```

### Configuration

Configure isort, if needed:
```
nano .isort.cfg
```

Configure Black, if needed:
```
nano pyproject.toml
```

Configure mypy, if needed:
```
nano mypy.ini
```

Configure flake8, if needed:
```
nano .flake8
```

Configure pre-commit, if needed:
```
nano .pre-commit-config.yaml
```

### Usage

Sort imports:
```
isort .
```

Format code:
```
black .
```

Type check code:
```
mypy .
``` 

Lint code:
```
flake8 .
```

Run all pre-commit hooks against currently staged files:
```
pre-commit run
```

Run a single pre-commit hook against currently staged files:
```
pre-commit run [HOOK ID]
```

Run all pre-commit hooks against all files:
```
pre-commit run --all-files
```

Run all pre-commit hooks against specific files:
```
pre-commit run --files [FILES [FILES ...]]
```


## Evaluation

We provide a utility application to evaluate GUI designs (web page screenshots) against all metrics. The application generates a CSV file with evaluation results as well as plot figures for each metric.

### Configuration

Configure [Loguru](https://github.com/Delgan/loguru), if needed:
```
nano loguru.ini
```

### Usage

Evaluate GUI designs:
```
python gui_designs_evaluator.py -i data/inputs/alexa_top_50_global_sites/ -o data/outputs/ -p
```


## License

Copyright (c) 2018-present, [User Interfaces group](https://userinterfaces.aalto.fi/), [Aalto University](https://www.aalto.fi/), Finland

This software is distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT). See [LICENSE.txt](../LICENSE.txt) for details.
