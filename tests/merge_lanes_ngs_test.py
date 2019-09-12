"""
An example test file
"""

import pathlib
import re
from click.testing import CliRunner
from mdu_pytools import merge_ngs_lanes


def test_cat_fastq(tmpdata):
    """
    Checking the outcome of cat_fastq, making sure the order of lanes is respected
    """
    outfolder = pathlib.Path("outfolder")
    fastq_list = [
        "sample1_R1_" + lane_numb + ".fastq.gz"
        for lane_numb in ["L00" + lane_numb for lane_numb in ["1", "2", "3", "4"]]
    ]
    cmd = merge_ngs_lanes.cat_fastq(fastq_list, "sample1", "R1", outfolder)
    assert (
        cmd
        == "cat sample1_R1_L001.fastq.gz sample1_R1_L002.fastq.gz sample1_R1_L003.fastq.gz sample1_R1_L004.fastq.gz > outfolder/sample1/sample1_R1.fastq.gz"
    )


def test_gen_command_subfolder_none(tmpdata, capfd):
    """
    Testing the output from gen_command without a subfolder
    """
    r1_list = [
        "sample1_R1_" + lane_numb + ".fastq.gz"
        for lane_numb in ["L00" + lane_numb for lane_numb in ["1", "2", "3", "4"]]
    ]
    r2_list = [
        "sample1_R2_" + lane_numb + ".fastq.gz"
        for lane_numb in ["L00" + lane_numb for lane_numb in ["1", "2", "3", "4"]]
    ]
    data = {"R1": r1_list, "R2": r2_list}
    outfolder = pathlib.Path("outfolder")
    merge_ngs_lanes.gen_command("sample1", data, outfolder, subfolder=None)
    out, err = capfd.readouterr()
    assert (
        out.strip()
        == "mkdir -p outfolder/sample1 && cat sample1_R1_L001.fastq.gz sample1_R1_L002.fastq.gz sample1_R1_L003.fastq.gz sample1_R1_L004.fastq.gz > outfolder/sample1/sample1_R1.fastq.gz && cat sample1_R2_L001.fastq.gz sample1_R2_L002.fastq.gz sample1_R2_L003.fastq.gz sample1_R2_L004.fastq.gz > outfolder/sample1/sample1_R2.fastq.gz"
    )


def test_gen_command_with_subfolder_ntc(tmpdata, capfd):
    """
    Testing the output from gen_command without a subfolder
    """
    subfolder = (("data", "^(?!NTC).*"), ("ntc", "(?<=NTC).*"))
    subfolder = dict((path, re.compile(regex)) for path, regex in subfolder)
    r1_list = [
        "NTC_R1_" + lane_numb + ".fastq.gz"
        for lane_numb in ["L00" + lane_numb for lane_numb in ["1", "2", "3", "4"]]
    ]
    r2_list = [
        "NTC_R2_" + lane_numb + ".fastq.gz"
        for lane_numb in ["L00" + lane_numb for lane_numb in ["1", "2", "3", "4"]]
    ]
    data = {"R1": r1_list, "R2": r2_list}
    outfolder = pathlib.Path("outfolder")
    merge_ngs_lanes.gen_command("NTC", data, outfolder, subfolder=subfolder)
    out, err = capfd.readouterr()
    assert (
        out.strip()
        == "mkdir -p outfolder/ntc/NTC && cat NTC_R1_L001.fastq.gz NTC_R1_L002.fastq.gz NTC_R1_L003.fastq.gz NTC_R1_L004.fastq.gz > outfolder/ntc/NTC/NTC_R1.fastq.gz && cat NTC_R2_L001.fastq.gz NTC_R2_L002.fastq.gz NTC_R2_L003.fastq.gz NTC_R2_L004.fastq.gz > outfolder/ntc/NTC/NTC_R2.fastq.gz"
    )


def test_gen_command_with_subfolder_data(tmpdata, capfd):
    """
    Testing the output from gen_command without a subfolder
    """
    subfolder = (("data", "^(?!NTC).*"), ("ntc", "(?<=NTC).*"))
    subfolder = dict((path, re.compile(regex)) for path, regex in subfolder)
    r1_list = [
        "sample1_R1_" + lane_numb + ".fastq.gz"
        for lane_numb in ["L00" + lane_numb for lane_numb in ["1", "2", "3", "4"]]
    ]
    r2_list = [
        "sample1_R2_" + lane_numb + ".fastq.gz"
        for lane_numb in ["L00" + lane_numb for lane_numb in ["1", "2", "3", "4"]]
    ]
    data = {"R1": r1_list, "R2": r2_list}
    outfolder = pathlib.Path("outfolder")
    merge_ngs_lanes.gen_command("sample1", data, outfolder, subfolder=subfolder)
    out, err = capfd.readouterr()
    assert (
        out.strip()
        == "mkdir -p outfolder/data/sample1 && cat sample1_R1_L001.fastq.gz sample1_R1_L002.fastq.gz sample1_R1_L003.fastq.gz sample1_R1_L004.fastq.gz > outfolder/data/sample1/sample1_R1.fastq.gz && cat sample1_R2_L001.fastq.gz sample1_R2_L002.fastq.gz sample1_R2_L003.fastq.gz sample1_R2_L004.fastq.gz > outfolder/data/sample1/sample1_R2.fastq.gz"
    )


def test_end_to_end_no_subfolder(tmpdata):
    """
    Test the cli interface
    """
    runner = CliRunner()
    results = runner.invoke(
        merge_ngs_lanes.main, ["-i", str(tmpdata), "-o", "outfolder"]
    )
    out = results.output.split("\n")
    out_exp1 = re.sub(str(tmpdata) + "/", "", out[1])
    out_exp2 = re.sub(str(tmpdata) + "/", "", out[2])
    assert results.exit_code == 0
    assert (
        out_exp1
        == "mkdir -p outfolder/sample1 && cat sample1_R1_L001.fastq.gz sample1_R1_L002.fastq.gz sample1_R1_L003.fastq.gz sample1_R1_L004.fastq.gz > outfolder/sample1/sample1_R1.fastq.gz && cat sample1_R2_L001.fastq.gz sample1_R2_L002.fastq.gz sample1_R2_L003.fastq.gz sample1_R2_L004.fastq.gz > outfolder/sample1/sample1_R2.fastq.gz"
    )
    assert (
        out_exp2
        == "mkdir -p outfolder/NTC && cat NTC_R1_L001.fastq.gz NTC_R1_L002.fastq.gz NTC_R1_L003.fastq.gz NTC_R1_L004.fastq.gz > outfolder/NTC/NTC_R1.fastq.gz && cat NTC_R2_L001.fastq.gz NTC_R2_L002.fastq.gz NTC_R2_L003.fastq.gz NTC_R2_L004.fastq.gz > outfolder/NTC/NTC_R2.fastq.gz"
    )


def test_end_to_end_with_subfolder(tmpdata):
    """
    Test the cli interface with subfolder
    """
    runner = CliRunner()
    results = runner.invoke(
        merge_ngs_lanes.main,
        [
            "-i",
            str(tmpdata),
            "-o",
            "outfolder",
            "--subfolder",
            "data",
            "^(?!NTC).*",
            "--subfolder",
            "ntc",
            "(?<=NTC).*",
        ],
    )
    out = results.output.split("\n")
    out_exp1 = re.sub(str(tmpdata) + "/", "", out[1])
    out_exp2 = re.sub(str(tmpdata) + "/", "", out[2])
    assert results.exit_code == 0
    assert (
        out_exp1
        == "mkdir -p outfolder/data/sample1 && cat sample1_R1_L001.fastq.gz sample1_R1_L002.fastq.gz sample1_R1_L003.fastq.gz sample1_R1_L004.fastq.gz > outfolder/data/sample1/sample1_R1.fastq.gz && cat sample1_R2_L001.fastq.gz sample1_R2_L002.fastq.gz sample1_R2_L003.fastq.gz sample1_R2_L004.fastq.gz > outfolder/data/sample1/sample1_R2.fastq.gz"
    )
    assert (
        out_exp2
        == "mkdir -p outfolder/ntc/NTC && cat NTC_R1_L001.fastq.gz NTC_R1_L002.fastq.gz NTC_R1_L003.fastq.gz NTC_R1_L004.fastq.gz > outfolder/ntc/NTC/NTC_R1.fastq.gz && cat NTC_R2_L001.fastq.gz NTC_R2_L002.fastq.gz NTC_R2_L003.fastq.gz NTC_R2_L004.fastq.gz > outfolder/ntc/NTC/NTC_R2.fastq.gz"
    )
