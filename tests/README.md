# Brel Tests

This directory contains tests for Brel. The tests are written in Python and use the `pytest` framework.

## Running the tests

To run the tests, make sure you install all the requirements in `requirements-test.txt`. Then, run the following command:

```bash
make test
```

This command will run the linter, the tests and generate a coverage report.

## Coverage

The coverage report is generated in the `htmlcov` directory. Open the `index.html` file in your browser to see the coverage report.

## Test structure

The tests are organized in the following structure:

- `calculation`: Tests for the calculation network.
- `end_to_end`: End-to-end tests for a handmade XBRL filing.
- `tests_core`: Tests for the core functionality of Brel, namely, filings, facts, contexts and qnames.
- `utils_tests`: Tests for the utility functions of Brel.
