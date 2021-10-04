# AIM Contributing Guide

We are really excited that you are interested in contributing to AIM! Before submitting your contribution though, please make sure to take a moment and read through the following instructions and guidelines.


## Extending AIM with New Metrics

AIM has been designed from the ground-up with extensibility in mind. As a result, new metrics can be added with relatively small effort, but there are a few steps that need to be followed.

1. For your metric, create a unique Python package within the AIM backend [metrics](./backend/aim/metrics/) directory. The package name must start with the letter `m`, followed by the subsequent metric number. This is your metric ID. For example, `m7`.
2. Create two empty Python files within your Python package: `__init__.py` and `<YOUR_METRIC_ID>_<YOUR_METRIC_NAME>.py`. For example, `m7_my_metric_name.py`.
3. The latter file is the entry point for your metric and it must implement the `AIMMetricInterface`, specified in the [interfaces.py](./backend/aim/metrics/interfaces.py) file. The easiest way to get started is to copy paste the code from an existing metric file (e.g., `m1/m1_png_file_size.py`) and modify it according to your needs. **Note:** Remember to include extensive documentation to your metric.
4. For testing your metric, create a new Python file within the AIM backend [tests](./backend/tests/metrics/) directory. For example, `test_m7.py`.
5. Implement unit tests within the file. Remember to cover not only basic scenarios, but also various edge cases in your tests. Again, the easiest way to get started is to copy paste the code from an existing unit test file (e.g., `test_m1.py`) and modify it according to your needs. **Note:** You might need to include metric-specific test files within the AIM backend [data](./backend/data/tests/) directory.
6. Run the utility tools to unify and improve code quality (see [Utility Tools](./README.md/#tools))
7. Run the test file (see [Tests](./README.md/#tests)).

In addition to the metric implementation and unit testing, the metric must be registered into the system. This is done by editing the [metrics.json](./metrics.json) file.

First, the metric must be listed in a suitable category under the `categories` key.

**Table 1.** Description of the `categories` entry in `metrics.json`

| Key     | Description |
|:--------|:------------|
| id      | Category ID |
| name    | Category name |
| icon    | Category icon |
| metrics | List of metric IDs belonging to this category |

Second, a new metric entry must be added under the `metrics` key. Each entry’s key is its metric ID.

**Table 2.** Description of the `metrics` entry in `metrics.json`

| Key               | Description |
|:------------------|:------------|
| id                | Metric ID |
| name              | Metric name |
| description       | Metric description |
| evidence          | 1-5 `int`; rating of evidence for this metric |
| relevance         | 1-5 `int`; rating of relevance for this metric |
| speed             | 0-2 `int`; 0=Slow, 1=Medium, 2=Fast |
| visualizationType | `table` or `b64`, table=numerical results, b64=image results |
| references        | List of `references` entries specifying references, see description below |
| results           | List of `results` entries specifying results, see description below |

**Table 3.** Description of the `references` entry in `metrics.json`

| Key      | Description |
|:---------|:------------|
| title    | Reference title |
| url      | Reference URL (e.g., doi) |

**Table 4.** Description of the `results` entry in `metrics.json`

| Key         | Description |
|:------------|:------------|
| id          | Result ID, format is metric ID + underscore + index in the array returned by the metric |
| index       | Index in the metric result array |
| type        | `int`, `float`, or `b64` |
| name        | Result name |
| description | Optional result description. `false` if there is no description |
| scores      | List of `scores` entries specifying scores, see description below |

**Table 5.** Description of the `scores` entry in `metrics.json`

| Key         | Description |
|:------------|:------------|
| id          | Score ID |
| range       | Score range; lower and upper bound |
| description | Score description |
| icon        | Score icon |
| judgmeent   | Score judgment; CSS class name |

Appropriate score ranges can be obtained by running the Evaluator utility app `python evaluator.py -o data/evaluations/ALEXA500/ -p` in the [backend](./backend/) directory). This generates histogram figures for each metric as well as files for evaluation results and statistics. Open the `quantiles.csv` file to see the score ranges of your new metric and set them accordingly in `metrics.json`. In addition, you must format the generated `results.json` file, and use it to replace the [results.json](./frontend/src/assets/results.json) file.

After adding a new metric, the frontend must be restarted with `npm run dev` for development or recompiled with `npm run build` for production (executed in the [frontend](./frontend/) directory). The backend server must be restarted as well with `python server.py` (executed in the [backend](./backend/) directory). **Note:** Remember to test the AIM web application (incl. your new metric and its dynamically generated histogram) in both docker and dockerless mode.

Finally, append your name to the list of contributors below :)


## Credits

Big thank you to all the people who have already contributed to AIM!

Antti Oulasvirta, Samuli De Pascale, Janin Koch, Thomas Langerak, Jussi Jokinen, Kashyap Todi, Markku Laine, Manoj Kristhombuge, Yuxi Zhu, Aliaksei Miniukovich, Gregorio Palmas, Tino Weinkauf, Ai Nakajima, Valentin Ionita, Morteza Shiripour, and Amir Hossein Kargaran.