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
                tmpdir.joinpath(f"{sample_id}_{read}_{lane}.fastq.gz").touch()
    return tmpdir


@pytest.fixture
def tmpfastq(tmpdir_factory):
    """
    Test sra-uploads
    """
    tmpsrc = pathlib.Path(tmpdir_factory.mktemp("reads"))
    tmpdest = pathlib.Path(tmpdir_factory.mktemp("dest"))
    isolates = tmpdest / "isolates.txt"
    isolates.touch()
    samples = ""
    for sample_numb in range(1, 11):
        sample = f"sample{sample_numb:02}"
        altsample = f"alt_sample{sample_numb:02}"
        samples += "\t".join([sample, altsample]) + "\n"
        tmpsrc.joinpath(sample).mkdir()
        for read in [f"R{read_numb}" for read_numb in range(1, 3)]:
            filename = f"{sample}_{read}.fastq.gz"
            tmpsrc.joinpath(sample, filename).touch()
    isolates.write_text(samples)
    return tmpsrc, tmpdest, isolates
