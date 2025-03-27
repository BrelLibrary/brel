# Brel Tests

This directory contains tests for Brel. The tests are written in Python and use the `pytest` framework.

## Running the tests

To run the tests, make sure you install all the requirements in `requirements-test.txt`. You can run the following command to install the requirements in a virtual environment:

#### UNIX SYSTEMS:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
```

#### WINDOWS SYSTEMS:
```
python -m venv .venv
.venv\Scripts\activate.bat   
pip install -e .
pip install -r requirements-test.txt
```

Then, run the following command:

#### UNIX SYSTEMS:
```bash
make test
```

#### WINDOWS SYSTEMS:
Firstly, you need to install chocolatey, which can be found [here](chocolatey.org/install), and then follow the instructions in [this](https://stackoverflow.com/questions/2532234/how-to-run-a-makefile-in-windows) StackOverflow post. We are working on a solutions so that additional installations are not required in the future.
```bash
make test
```
This command will run the linter, the tests and generate a coverage report.

\
\
To deactivate the virtual environment, run the following command:

```bash
deactivate
```

## Coverage

The coverage report is generated in the `htmlcov` directory. Open the `index.html` file in your browser to see the coverage report.

## Test structure

The tests are organized in the following structure:

- `calculation_tests`: Tests for the calculation network.
- `characteristics_tests`: Tests for the characteristics of the filing.
- `core_tests`: Tests for the core functionality of Brel, namely, filings, facts, contexts and QNames.
- `end_to_end_tests`: End-to-end tests for a handmade XBRL filing.
- `utils_tests`: Tests for the utility functions of Brel.
