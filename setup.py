from setuptools import setup, find_packages

setup(
    name="banana",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ipykernel>=7.1.0",
        "matplotlib>=3.10.7",
        "pandas>=2.3.3",
    ],
)
