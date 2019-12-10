import pathlib
from setuptools import setup, find_packages


setup(
    name="scrapy-mongoengine",
    version="0.1.0",
    url="https://github.com/edison7500/scrapy-mongoengine",
    description="Scrapy extenstion to item export to mongodb",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Scrapy developers",
    license="BSD",
    classifiers=[
        "Framework :: Scrapy",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=["Twisted", "Scrapy", "mongoengine"],
)
