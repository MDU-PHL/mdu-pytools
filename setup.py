"""
Setup mdu-pytools
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

# Load version string from package
from mdu_pytools import __version__ as version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mdu-pytools",  # Required
    version=version,  # Required
    description="Small tools/scripts written in Python for MDU",
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional 
    url="https://github.com/MDU-PHL/mdu-pytools",  # Optional
    author="MDU Bioinformatics",  # Optional
    author_email="andersgs near gmail dot com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="bioinformatics microbial-genomics",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    python_requires=">=3.6, <4",
    
    install_requires=[
        "pandas",
        "loguru",
        "click"
    ],  # Optional
    extras_require={  # Optional
        "dev": ["pre-commit", "pipenv"],
        "test": ["pytest", "pytest-cov"],
    },
#    package_data={"package_name": ["data/example_data.csv"]},  # Optional
    entry_points={"console_scripts": ["sample=sample:main"]},  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/MDU-PHL/mdu-pytools/issues",
        #"Funding": "https://donate.pypi.org",
        #"Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/MDU-PHL/mdu-pytools/",
    },
)
