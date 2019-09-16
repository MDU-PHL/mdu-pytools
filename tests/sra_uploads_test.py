"""
Test sra_uploads
"""

import os

from mdu_pytools.sra_uploads import copy_fastq


def test_copy_fastq(tmpfastq):
    """
    Test copy_fastq
    """
    src, dest, isolates = tmpfastq
    os.chdir(dest)
    isolates = isolates.name
    copy_fastq(isolates, src)
    output = sorted(list(fn.name for fn in dest.glob("*fastq.gz")))
    assert output == [
        "alt_sample01_R1.fastq.gz",
        "alt_sample01_R2.fastq.gz",
        "alt_sample02_R1.fastq.gz",
        "alt_sample02_R2.fastq.gz",
        "alt_sample03_R1.fastq.gz",
        "alt_sample03_R2.fastq.gz",
        "alt_sample04_R1.fastq.gz",
        "alt_sample04_R2.fastq.gz",
        "alt_sample05_R1.fastq.gz",
        "alt_sample05_R2.fastq.gz",
        "alt_sample06_R1.fastq.gz",
        "alt_sample06_R2.fastq.gz",
        "alt_sample07_R1.fastq.gz",
        "alt_sample07_R2.fastq.gz",
        "alt_sample08_R1.fastq.gz",
        "alt_sample08_R2.fastq.gz",
        "alt_sample09_R1.fastq.gz",
        "alt_sample09_R2.fastq.gz",
        "alt_sample10_R1.fastq.gz",
        "alt_sample10_R2.fastq.gz",
    ]
