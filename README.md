# MDU Python Tools

[![CircleCI](https://circleci.com/gh/MDU-PHL/mdu-pytools.svg?style=svg)](https://circleci.com/gh/MDU-PHL/mdu-pytools) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mdu-pytools) ![PyPI](https://img.shields.io/pypi/v/mdu-pytools) ![PyPI - License](https://img.shields.io/pypi/l/mdu-pytools)

- [MDU Python Tools](#mdu-python-tools)
  - [Background](#background)
  - [Tools](#tools)
    - [merge-ngs-lanes](#merge-ngs-lanes)
  - [Development](#development)
    - [Development environment](#development-environment)

## Background

Some simple tools in python for MDU

## Tools

### merge-ngs-lanes

Use it to correctly merge lanes from an Illumina run into the a single FASTQ.

Get help:

```bash
merge-ngs-lanes --help
```

Basic usage:

```bash
merge-ngs-lanes -i /path/to/fastq_folder -o /path/to/output > cmd.sh
```

Advanced usage:

You can split the output to muliple subfolders of the output folder by adding `--subfolder`
to the command line. The option can be used multiple times, and takes two space separated values as input:
`path` `regex`. The `path` gives a name of the subfolder in the output folder, and the `regex` expression
determines which samples go in that subfolder.

For instance, the command below will split samples starting the NTC in to a subfolder called `ntc`,
while all other samples will be added to a subfolder called `data`.

```bash
merge-ngs-lanes -i /path/to/fastq -o /path/to/output --subfolder 'data' '(?!NTC).*' --subfolder 'ntc' '(?<=NTC).*' > cmd.sh
```

## Development

### Development environment

To develop with the same environment use `vagrant` and `virtualbox`:

```bash
vagrant up
vagrant ssh
```

Once logged in to the VM, the shared folder is in `/vagrant`.
