"""Python setup.py for brel package"""

import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("brel", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="brel-xbrl",
    version=read("brel", "VERSION"),
    python_requires=">=3.10",
    description="An XBRL parser for Python",
    url="https://github.com/BrelLibrary/brel/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="PapediPoo, ghislainfourny",
    packages=find_packages(exclude=["tests", ".github"]),
    package_data={"": ["*.json"]},
    intall_requires=[
        "appdirs==1.4.4",
        "black==23.12.1",
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "coverage==7.4.3",
        "databind.core==4.4.2",
        "databind.json==4.4.2",
        "Deprecated==1.2.14",
        "docspec==2.2.1",
        "docspec-python==2.2.1",
        "docstring_parser==0.11",
        "fs==2.4.16",
        "ghp-import==2.1.0",
        "graphviz==0.20.1",
        "html5lib==1.1",
        "idna==3.6",
        "importlib-metadata==7.0.1",
        "iniconfig==2.0.0",
        "Jinja2==3.1.3",
        "lxml==5.1.0",
        "lxml-stubs==0.5.1",
        "Markdown==3.5.2",
        "markdown-it-py==3.0.0",
        "MarkupSafe==2.1.5",
        "mdurl==0.1.2",
        "mergedeep==1.3.4",
        "mkdocs==1.5.3",
        "mypy==1.15.0",
        "mypy-extensions==1.0.0",
        "nr-date==2.1.0",
        "nr-stream==1.1.5",
        "nr.util==0.8.12",
        "numpy==1.26.4",
        "packaging==23.2",
        "pandas==2.2.1",
        "pandas-stubs==2.2.3.250308",
        "pathspec==0.12.1",
        "platformdirs==4.2.0",
        "pluggy==1.4.0",
        "prettytable==3.9.0",
        "py4j==0.10.9.7",
        "pydoc-markdown==4.8.2",
        "Pygments==2.17.2",
        "pyspark==3.5.1",
        "pytest==8.0.2",
        "pytest-cov==4.1.0",
        "python-dateutil==2.8.2",
        "pytz==2024.1",
        "PyYAML==6.0.1",
        "pyyaml_env_tag==0.1",
        "requests==2.31.0",
        "rich==13.7.1",
        "setuptools==75.8.2",
        "six==1.16.0",
        "tomli==2.0.1",
        "tomli_w==1.0.0",
        "typeapi==2.1.2",
        "types-openpyxl==3.1.5.20250306",
        "types-protobuf==5.29.1.20250403",
        "types-python-dateutil==2.8.19.20240106",
        "types-pytz==2025.2.0.20250326",
        "types-requests==2.31.0.20240218",
        "types-six==1.17.0.20250304",
        "types-tabulate==0.9.0.20241207",
        "typing_extensions==4.6.3",
        "tzdata==2024.1",
        "urllib3==2.1.0",
        "watchdog==4.0.0",
        "wcwidth==0.2.13",
        "webencodings==0.5.1",
        "wrapt==1.16.0",
        "yapf==0.40.2",
        "zipp==3.17.0",
    ],
    entry_points={"console_scripts": ["brel = brel.__main__:main"]},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    extras_require={
        "test": [
            "appdirs==1.4.4",
            "black==23.12.1",
            "certifi==2023.11.17",
            "charset-normalizer==3.3.2",
            "click==8.1.7",
            "coverage==7.4.3",
            "databind.core==4.4.2",
            "databind.json==4.4.2",
            "Deprecated==1.2.14",
            "docspec==2.2.1",
            "docspec-python==2.2.1",
            "docstring_parser==0.11",
            "fs==2.4.16",
            "ghp-import==2.1.0",
            "graphviz==0.20.1",
            "html5lib==1.1",
            "idna==3.6",
            "importlib-metadata==7.0.1",
            "iniconfig==2.0.0",
            "Jinja2==3.1.3",
            "lxml==5.1.0",
            "lxml-stubs==0.5.1",
            "Markdown==3.5.2",
            "markdown-it-py==3.0.0",
            "MarkupSafe==2.1.5",
            "mdurl==0.1.2",
            "mergedeep==1.3.4",
            "mkdocs==1.5.3",
            "mypy==1.15.0",
            "mypy-extensions==1.0.0",
            "nr-date==2.1.0",
            "nr-stream==1.1.5",
            "nr.util==0.8.12",
            "numpy==1.26.4",
            "packaging==23.2",
            "pandas==2.2.1",
            "pandas-stubs==2.2.3.250308",
            "pathspec==0.12.1",
            "platformdirs==4.2.0",
            "pluggy==1.4.0",
            "prettytable==3.9.0",
            "py4j==0.10.9.7",
            "pydoc-markdown==4.8.2",
            "Pygments==2.17.2",
            "pyspark==3.5.1",
            "pytest==8.0.2",
            "pytest-cov==4.1.0",
            "python-dateutil==2.8.2",
            "pytz==2024.1",
            "PyYAML==6.0.1",
            "pyyaml_env_tag==0.1",
            "requests==2.31.0",
            "rich==13.7.1",
            "setuptools==75.8.2",
            "six==1.16.0",
            "tomli==2.0.1",
            "tomli_w==1.0.0",
            "typeapi==2.1.2",
            "types-openpyxl==3.1.5.20250306",
            "types-protobuf==5.29.1.20250403",
            "types-python-dateutil==2.8.19.20240106",
            "types-pytz==2025.2.0.20250326",
            "types-requests==2.31.0.20240218",
            "types-six==1.17.0.20250304",
            "types-tabulate==0.9.0.20241207",
            "typing_extensions==4.6.3",
            "tzdata==2024.1",
            "urllib3==2.1.0",
            "watchdog==4.0.0",
            "wcwidth==0.2.13",
            "webencodings==0.5.1",
            "wrapt==1.16.0",
            "yapf==0.40.2",
            "zipp==3.17.0",
        ]
    },
)
