"""
Upload data to SRA
"""
import os
import subprocess

from loguru import logger
import click


def run_cmd(cmd):
    """
    Simple command runner with logger of stdout
    """
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf8",
    )
    while proc.poll() is None:
        logger.info(proc.stdout.readline().strip())


def copy_fastq(isolates, reads_folder):
    """
    Run parallel to copy over FASTQ data
    """
    logger.info("Starting data copying...")
    cmd = f"parallel --bar --col-sep '\t' -j1 '[ ! -f {{2}}_R1.fastq.gz ] && cp {reads_folder}/{{1}}/*R1* {{2}}_R1.fastq.gz && cp {reads_folder}/{{1}}/*R2* {{2}}_R2.fastq.gz' :::: {isolates}"
    run_cmd(cmd)


def upload_using_ascp(folder, sra_subfolder, ascp_key):
    """
    Run ascp to upload data to SRA.
    """
    logger.info("Starting upload of data to SRA.")
    cmd = f"ascp -i {ascp_key} -QT -l500m -d *.fastq.gz subasp@upload.ncbi.nlm.nih.gov:uploads/{sra_subfolder}/{folder}"
    run_cmd(cmd)


@click.command()
@click.argument("isolates")
@click.option(
    "-f",
    "--folder",
    help="Folder on NCBI to upload. Used to find the reads when submitting via the SRA portal.",
    default="mdu",
    show_default=True,
)
@click.option(
    "-r",
    "--reads-folder",
    help="Where reads are located (uses MDU_READS env variable if available).",
    default=os.environ.get("MDU_READS", None),
    show_default=True,
)
@click.option(
    "-k",
    "--ascp-key",
    help="Path to ascp ssh upload key (uses ASCP_UPLOAD_KEY env variable if available). This can be obtained from the SRA Submission Portal.",
    default=os.environ.get("ASCP_UPLOAD_KEY", None),
    show_default=True,
)
@click.option(
    "-s",
    "--sra-subfolder",
    help="SRA subfolder owned by you where data will copied to (uses SRA_SUBFOLDER env variable is available).",
    default=os.environ.get("SRA_SUBFOLDER", None),
    show_default=True,
)
def main(isolates, folder, reads_folder, ascp_key, sra_subfolder):
    """
    """
    logger.info("Welcome to SRA Uploads...")
    copy_fastq(isolates, reads_folder)
    upload_using_ascp(folder, sra_subfolder, ascp_key)
    logger.info("All done")


if __name__ == "__main__":
    main()
