from setuptools import find_packages, setup

setup(
    name="src",
    packages=find_packages(where="src"),
    version="0.1.0",
    package_dir={"": "src"},
)
