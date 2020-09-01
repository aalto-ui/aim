# AIM 2 Metrics

A subproject for AIM 2 metrics. The metrics are Python 3 compatible, revised, and rigorously tested.


## Technologies

Main technologies and Python packages used in this subproject.

### Backend

- **Python 3.7.** Programming language. https://www.python.org/
- **Pipenv.** Packaging tool for Python. https://github.com/pypa/pipenv
- **isort.** Python utility to automatically sort imports. https://timothycrosley.github.io/isort/
- **Black.** Python code formatter. https://github.com/psf/black
- **Mypy.** Static type checker for Python. http://mypy-lang.org/
- **Flake8.** Python tool for style guide enforcement. https://flake8.pycqa.org/en/latest/
- **pytest.** Python testing framework. https://pytest.org/
- **pre-commit.** Package manager for pre-commit hooks. https://pre-commit.com/ 


## Installation

Clone the git repository:
```
git clone git@github.com:aalto-ui/aim.git && cd aim/aim2_metrics
```

Install the dependencies with development packages:
```
pipenv install --dev
```

Activate the virtual environment:
```
pipenv shell
```

Deactivate the virtual environment (if needed):
```
exit
```

Install pre-commit into your git hooks:
```
pre-commit install --install-hooks --overwrite
```

Uninstall pre-commit from your git hooks (if needed):
```
pre-commit uninstall
```


## Configuration

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

Configure pytest, if needed:
```
nano pytest.ini
```

Configure pre-commit, if needed:
```
nano .pre-commit-config.yaml
```


## Utilities

Sort imports:
```
isort .
```

Format the code:
```
black .
```

Type check the code:
```
mypy .
``` 

Lint the code:
```
flake8 .
```

Run pre-commit hooks against currently staged files:
```
pre-commit run
```

Run an individual pre-commit hook against currently staged files:
```
pre-commit run <hook_id>
```

Run pre-commit hooks against all files:
```
pre-commit run --all-files
```


## Tests

Run the tests:
```
pytest .
```


## License

Copyright (c) 2018-present, [User Interfaces group](https://userinterfaces.aalto.fi/), [Aalto University](https://www.aalto.fi/), Finland

This software is distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT). See [LICENSE.txt](../LICENSE.txt) for details.
