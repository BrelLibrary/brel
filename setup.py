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
    package_data={"brel-xbrl": ["config/*.json"]},
    install_requires=read_requirements("requirements.txt"),
    entry_points={"console_scripts": ["brel = brel.__main__:main"]},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    extras_require={"test": read_requirements("requirements-test.txt")},
)
