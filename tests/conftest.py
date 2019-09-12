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
        for lane in [f"L00{lane_numb}" for lane_numb in range(1, 5)]:
            for read in [f"R{read_numb}" for read_numb in range(1, 3)]:
                filename = tmpdir / f"{sample_id}_{read}_{lane}.fastq.gz"
                filename.touch()
    return tmpdir
