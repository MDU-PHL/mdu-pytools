"""
A script to merge lanes from an Illumina run
"""
import os
import collections
import pathlib
import re

import click
from loguru import logger
import tqdm


def cat_fastq(fastq_list, sample_id, read_number, outfolder):
    """
    Generate a cat command line to join the lanes
    """
    outfile = sample_id + "_" + read_number + ".fastq.gz"
    return f"cat {' '.join(sorted(fastq_list))} > {outfolder / sample_id / outfile}"


def gen_command(sample_id, data, outfolder, subfolder):
    """
    For a given sample_id, generate the shell command to create a subfolder labelled with
    the sample_id, and then cat the fastq in to it.
    """
    # check to see if need to add subfolder to outfolder path
    if subfolder:
        for subpath in subfolder.keys():
            if subfolder[subpath].search(sample_id):
                if len(subpath) > 0:
                    outfolder = outfolder / subpath
                break
    cmd = f"mkdir -p {outfolder / sample_id}"
    for read_number in sorted(data.keys()):
        cmd += " && " + cat_fastq(data[read_number], sample_id, read_number, outfolder)
    print(cmd)


@click.command()
@click.option("-i", "--infolder", default=os.environ.get("PWD"), show_default=True)
@click.option("-o", "--output", default=os.environ.get("PWD"), show_default=True)
@click.option(
    "-s", "--subfolder", default=None, show_default=True, multiple=True, type=(str, str)
)
def main(infolder, output, subfolder):
    """
    Generate the shell commands to properly concatenate mutiple lanes of Illumina data into one FASTQ file.

    Assumes the sample_id is formed by the characters up to the first "_" in the filename.

    \b
    Usage:
    # simple usage
    merge-ngs-lanes -i /path/to/fastq -o /path/to/output > cmd.sh

    \b
    # split output to different subfolders with regex
    # in the case below, samples starting with NTC will but in an ntc subfolder
    # samples not starting with an NTC will be put in the data subfolder
    # these are subfolders of output folder
    merge-ngs-lanes -i /path/to/fastq -o /path/to/output --subfolder 'data' '(?!NTC).*' --subfolder 'ntc' '(?<=NTC).*' > cmd

    \b
    # once the cmd.sh file is created run
    # it is work running less cmd.sh to check the commands
    # one may need to play a bit with the regex expressions to get the subfolders
    # working correctly
    less cmd.sh # check the output to make sure it correct
    bash cmd.sh
    """
    if subfolder:
        subfolder = dict((path, re.compile(regex)) for path, regex in subfolder)
    output = pathlib.Path(output)
    fastqs = collections.defaultdict(lambda: collections.defaultdict(list))
    path = pathlib.Path(infolder)
    for fastq in tqdm.tqdm(path.glob("**/*fastq.gz"), unit=" files"):
        if "unindexed" in str(fastq).lower():
            continue
        filename = fastq.name
        sample_id = filename.split("_")[0]
        logger.info(f"Working on {sample_id}")
        r = "R1" if "_R1_" in filename else "R2"
        fastqs[sample_id][r].append(str(fastq.absolute()))
    for sample_id in fastqs.keys():
        gen_command(sample_id, fastqs[sample_id], output, subfolder)


if __name__ == "__main__":
    main()
