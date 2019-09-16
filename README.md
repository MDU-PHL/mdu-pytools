# MDU Python Tools

[![CircleCI](https://circleci.com/gh/MDU-PHL/mdu-pytools.svg?style=svg)](https://circleci.com/gh/MDU-PHL/mdu-pytools) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mdu-pytools) ![PyPI](https://img.shields.io/pypi/v/mdu-pytools) ![PyPI - License](https://img.shields.io/pypi/l/mdu-pytools)

- [MDU Python Tools](#mdu-python-tools)
  - [Background](#background)
  - [Tools](#tools)
    - [mdu-merge-ngs-lanes](#mdu-merge-ngs-lanes)
    - [mdu-sra-uploads](#mdu-sra-uploads)
      - [Environmental variables that can be used to set options](#environmental-variables-that-can-be-used-to-set-options)
  - [Development](#development)
    - [Development environment](#development-environment)

## Background

Some simple tools in python for MDU

## Tools

### mdu-merge-ngs-lanes

Use it to correctly merge lanes from an Illumina run into the a single FASTQ.

Get help:

```bash
mdu-merge-ngs-lanes --help
```

Basic usage:

```bash
mdu-merge-ngs-lanes -i /path/to/fastq_folder -o /path/to/output > cmd.sh
```

Advanced usage:

You can split the output to muliple subfolders of the output folder by adding `--subfolder`
to the command line. The option can be used multiple times, and takes two space separated values as input:
`path` `regex`. The `path` gives a name of the subfolder in the output folder, and the `regex` expression
determines which samples go in that subfolder.

For instance, the command below will split samples starting the NTC in to a subfolder called `ntc`,
while all other samples will be added to a subfolder called `data`.

```bash
mdu-merge-ngs-lanes -i /path/to/fastq -o /path/to/output --subfolder 'data' '(?!NTC).*' --subfolder 'ntc' '(?<=NTC).*' > cmd.sh
```

### mdu-sra-uploads

Use to it to upload FASTQ data to NCBI SRA.

Requires a file with tab-separated values of `MDU ID` and `AUSMDUID`. For example:

mdu1\tausmdu1

mdu2\tausmdu2

Getting help:

```bash
mdu-sra-uploads --help
```

```bash
Usage: mdu-sra-upload [OPTIONS] ISOLATES

Options:
  -f, --folder TEXT         Folder on NCBI to upload. Used to find the reads
                            when submitting via the SRA portal.  [default:
                            mdu]
  -r, --reads-folder TEXT   Where reads are located (uses MDU_READS env
                            variable if available).
  -k, --ascp-key TEXT       Path to ascp ssh upload key (uses ASCP_UPLOAD_KEY
                            env variable if available). This can be obtained
                            from the SRA Submission Portal.
  -s, --sra-subfolder TEXT  SRA subfolder owned by you where data will copied
                            to (uses SRA_SUBFOLDER env variable is available).
  --help                    Show this message and exit.
```

Basic usage:

```bash
cd /path/for/upload
# copy paste isolates.txt
mdu-sra-uploads isolates.txt
# when completing the submission, search for pre-uploaded files in the folder called mdu
```



#### Environmental variables that can be used to set options

* `MDU_READS`: full path to where FASTQ data is stored
* `ASCP_UPLOAD_KEY`: full path to where your Aspera NCBI upload key is located (obtain one from the SRA submission portal under the Aspera command line instructions)
* `SRA_FOLDER`: path to your folder at SRA. Usually composed by your `email` plus an "_" and some random alphanumeric characters. This can be obtained from SRA submission portal under the Aspera command line instructions (e.g., `john.doe@doe.industries.com_qEWo9`).

## Development

### Development environment

To develop with the same environment use `vagrant` and `virtualbox`:

```bash
vagrant up
vagrant ssh
```

Once logged in to the VM, the shared folder is in `/vagrant`.
