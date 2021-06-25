![interfacemetrics.aalto.fi](./frontend/src/assets/workflow.png)

# Aalto Interface Metrics (AIM)

**Aalto Interface Metrics (AIM)** is a new service that lets you automatically test the usability and aesthetics of your website using several verified user interface metrics. Simply enter a web page URL or upload a screenshot, and select desired metrics to get started. AIM segments the page, and displays a preview. As results are computed, they are presented along with detailed explanations, and histograms for comparison. AIM is fully open-sourced, and we invite you to extend the service with your own contributions. Head over to [interfacemetrics.aalto.fi](https://interfacemetrics.aalto.fi/) to give it a try, and for more information.


## Architecture

AIM codebase is divided into three distinct parts:

* [Backend - web application](./backend/)
* [Frontend - web application](./frontend/)
* [Legacy - miscellaneous files](./legacy/)

The backend is written in Python using the [Tornado](http://www.tornadoweb.org/) web application framework having [MongoDB](https://www.mongodb.com/) as a database, whereas the frontend is built with [Vue.js](https://vuejs.org/). The backend and the frontend communicate with each other in real-time via [WebSocket](https://tools.ietf.org/html/rfc6455). The legacy folder contains miscellaneous files of AIM version 1 that have not been integrated into the new AIM version yet.

The most important files and folders in the AIM codebase are:
```
.
├── backend               : AIM backend files
│   ├── aim               : Source code (incl. metrics)
│   ├── data              : Data files (incl. datasets)
│   ├── tests             : Unit tests
│   ├── webdrivers        : Web drivers
│   ├── evaluator.py      : Evaluator utility app
│   ├── screenshoter.py   : Screenshoter utility app
│   ├── server.conf       : Server configuration file
│   └── server.py         : Server app
├── frontend              : AIM frontend files
│   ├── build             : Build scripts
│   ├── src               : Sources code (incl. assets)
│   ├── static            : Static files (incl. histograms)
│   ├── test              : Unit tests, etc.
│   └── config.js         : Configuration module
├── legacy                : AIM legacy files (version 1)
├── metrics.json          : AIM metrics configuration file
├── ...
.
```


## Installation

Clone the [AIM git repository](https://github.com/aalto-ui/aim) and checkout the `aim2` branch:
```
git clone https://github.com/aalto-ui/aim.git
cd aim
git checkout aim2
```

### Dependencies

Make sure you have the following software already installed on your computer before proceeding!

The backend dependencies include [Python 3.7+](https://www.python.org/), [pip](https://pypi.org/project/pip/), and [MongoDB](https://www.mongodb.com/). In addition, it is highly recommended to install [virtualenv](https://pypi.org/project/virtualenv/) or [Pipenv](https://pypi.org/project/pipenv/) to create a dedicated Python virtual environment (see [instructions](#installation_backend)). Other dependencies include [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) for the frontend and [git](https://git-scm.com/) to track changes made to the codebase.

### Database

Create a new database called `aim` in [MongoDB](https://www.mongodb.com/) with the following two collections in it: `inputs` and `results`.

### Backend <a name="installation_backend"></a>

Go to the [backend](./backend/) directory and configure the server by editing the [server.conf](./backend/server.conf) file, especially the `database_uri` property.

#### Working with `virtualenv`

Create a new virtual environment:
```
virtualenv ../venv
```

Activate the virtual environment:
```
source ../venv/bin/activate
```

Install all dependencies, including development packages:
```
pip install -r requirements.txt
```

Re-activate the virtual environment to update paths (see [Stack Overflow](https://stackoverflow.com/questions/35045038/how-do-i-use-pytest-with-virtualenv) for details):
```
deactivate && source ../venv/bin/activate
```

To deactivate the virtual environment, run:
```
deactivate
```

#### Working with `Pipenv`

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

### Frontend

Go to the [frontend](./frontend/) directory and install the dependencies by running:
```
npm install
```


## Usage

### Backend

To start the backend server, go to the [backend](./backend/) directory and run:
```
python server.py
```

### Frontend

To start the frontend HTTP server in development mode, go to the [frontend](./frontend/) directory and run:
```
npm run dev
```


You can find the accepted environment variables in `frontend/config.js`. If you
want to change on of the default values, you can pass them directly an runtime
or by setting them in the shell environment. For example:
```sh
WS_URL='ws://localhost:8889/' npm run dev
```

To build the frontend for production, run the following command in the same directory:
```
npm run build
```

After the build is complete, the files (for production) can be found under the newly created `dist` directory. These files are meant to be served over an HTTP server, such as [Apache HTTP Server](https://httpd.apache.org/).

It is highly recommended to use a *load balancer* (e.g., Apache HTTP Server) in a production environment, as certain metrics are extremely CPU intensive. This means that the backend needs to be launched with multiple instances, each listening to a different port. A process manager (e.g., [pm2](http://pm2.keymetrics.io/)) will come in handy at that point.


## Tests <a name="tests"></a>

AIM backend uses [pytest](https://pypi.org/project/pytest/), a Python testing framework, to run tests on the backend source code, including metrics. To configure and run the tests, go to the [backend](./backend/) directory and follow the instructions below.

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


## Screenshoter App <a name="screenshoter"></a>

AIM backend provides a utility app for taking web page screenshots in specified dimensions (i.e., width, height, and/or full page). To configure and run the app, go to the [backend](./backend/) directory and follow the instructions below.

### Configuration

Configure [Loguru](https://pypi.org/project/loguru/), if needed:
```
nano loguru.ini
```

### Usage

Show the help message:
```
python screenshoter.py -h
```

Example of taking web page screenshots:
```
python screenshoter.py -i data/screenshots/ALEXA_500/urls.csv -sw 1280 -sh 800 -f -o data/screenshots/results/
```


## Evaluator App <a name="evaluator"></a>

AIM backend also provides a utility app for evaluating GUI designs (i.e., web page screenshots) against selected metrics. The app generates two CSV files, `results.csv` and `quantiles.csv`, with evaluation results and statistics, respectively. Optionally, it also generates histogram figures for each metric. To configure and run the app, go to the [backend](./backend/) directory and follow the instructions below.

### Configuration

Configure [Loguru](https://pypi.org/project/loguru/), if needed:
```
nano loguru.ini
```

### Datasets

[Alexa Top Global Sites](https://www.alexa.com/topsites) (ALEXA_500) currently serves as our test dataset. Additional datasets can be downloaded, for instance, from https://doi.org/10.7910/DVN/XEYNYW.

### Usage

Show the help message:
```
python evaluator.py -h
```

Example of evaluating GUI designs:
```
python evaluator.py -i data/screenshots/ALEXA_500/ -m m1,m2,m3 -p -o data/evaluations/results/
```

**Note:** A set of screenshots in the input directory can be excluded from the evaluation by listing their file names in the `exclude.txt` file.


## Utility Tools <a name="tools"></a>

In addition, AIM backend supports the following utility tools to (i) ease development and (ii) unify and improve code quality. Their installation and use is optional, but highly recommended.

- **isort.** Python utility to automatically sort imports. https://pypi.org/project/isort/
- **Black.** Python code formatter. https://pypi.org/project/black/
- **Mypy.** Static type checker for Python. https://pypi.org/project/mypy/
- **Flake8.** Python tool for style guide enforcement. https://pypi.org/project/flake8/
- **pre-commit.** Package manager for pre-commit hooks. https://pypi.org/project/pre-commit/

### Installation

Go to the [backend](./backend/) directory and install pre-commit into your git hooks:
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


## Troubleshooting

1. **PROBLEM:** Running `mypy` fails and the following error message is shown *./venv/lib/python3.7/site-packages is in the PYTHONPATH. Please change directory so it is not.* **SOLUTION:** Create your virtual environment outside of the AIM backend directory. For example, `virtualenv ../venv`. Alternatively, configure mypy to exclude your virtual environment directory.
2. **PROBLEM:** Running `mypy` finds errors in files that are not part of the AIM backend. For example, *venv/bin/activate_this.py:28: error: "str" has no attribute "decode"; maybe "encode"?* **SOLUTION:** Create your virtual environment outside of the AIM backend directory. For example, `virtualenv ../venv`. Alternatively, configure mypy to exclude your virtual environment directory.
3. **PROBLEM:** Running `python screenshoter.py` or submitting an URL in the web application fails and an error message similar to the following is shown *selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 89. Current browser version is 91.0.4472.77 with binary path /Applications/Google Chrome.app/Contents/MacOS/Google Chrome* **SOLUTION:** Download a matching version of [ChromeDriver](https://chromedriver.chromium.org/downloads) and replace the appropriate `chromedriver_xxx` file in the [webdrivers](./backend/webdrivers/) directory.


## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on contributing to AIM.


## Changelog

Detailed changes for each release are documented in the [release notes](https://github.com/aalto-ui/aim/releases).


## Funding Information and Contact

AIM and related research have been funded by the Technology Industries of Finland Future Makers project SOWP (2017-2019) and the European Research Council starting grant (COMPUTED 2015-2020).

For questions and further information, please contact us via email at <interfacemetrics@aalto.fi>.


## License

Copyright (c) 2018-present, [User Interfaces group](https://userinterfaces.aalto.fi/), [Aalto University](https://www.aalto.fi/), Finland

This software is distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT). See [LICENSE.txt](./LICENSE.txt) for details.
