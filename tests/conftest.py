"""
Example conftest.py

Here, I add a fixture that copies some data to a temp folder that
can then be accessed by other tests
"""

import pathlib
import pytest


@pytest.fixture
def tmpdata(tmpdir_factory):
    """
    Creating a fixture that all tests can use with a temporary folder and
    with the package data
    """
    tmpdir = pathlib.Path(tmpdir_factory.mktemp("data"))
    for sample_id in ["sample1", "NTC"]:
        for lane in "-":
            for read in ["R" + read_numb for read_numb in ["1", "2"]]:
                filename = tmpdir / f"{sample_id}_{read}_{lane}.fastq.gz"
                filename.touch()
    return tmpdir
