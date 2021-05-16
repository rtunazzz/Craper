from pathlib import Path
from setuptools import setup, find_packages

from os import path

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE/"README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    reqs = f.read().split('\n')

setup(
    name="craper",
    version="1.0.1",
    description="A collection of product scrapers for various websites.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rtunazzz/Craper",
    author="Artur Hnat",
    author_email="rtunaboss@gmail.com",
    license="MIT",
    # keyword="TBD",
    python_requires='>=3.9',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    # packages=["craper"],
    packages=find_packages(exclude=("tests",)) + ['craper/config', 'craper/data'],
    include_package_data=True,
    install_requires=reqs,
    entry_points={
        "console_scripts": [
            "craper=craper.__main__:main",
        ]
    },
)
