from setuptools import setup, find_packages
from pathlib import Path


def read(rel_path):
    here = Path(".").absolute()
    with open(here / rel_path, "rt") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="baked-tools",
    version=get_version("baked_tools/__init__.py"),
    packages=find_packages(),
)
