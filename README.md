# covidweb
Web uploader for COVID19 sequences

# Web Interface

# Commandline tool

To get started, first [install the uploader](#installation), and use the `bh20-seq-uploader` command to [upload your data](#usage).

## Installation

There are several ways to install the uploader. The most portable is with a [virtualenv](#installation-with-virtualenv).

### Installation with `virtualenv`

1. **Prepare your system.** You need to make sure you have Python, and the ability to install modules such as `pycurl` and `pyopenssl`. On Ubuntu 18.04, you can run:

```sh
sudo apt update
sudo apt install -y virtualenv git libcurl4-openssl-dev build-essential python3-dev libssl-dev
```

2. **Create and enter your virtualenv.** Go to some memorable directory and make and enter a virtualenv:

```sh
virtualenv --python python3 venv
. venv/bin/activate
```

Note that you will need to repeat the `. venv/bin/activate` step from this directory to enter your virtualenv whenever you want to use the installed tool.

3. **Install the tool.** Once in your virtualenv, install this project:
Install from git:

```sh
pip3 install  git+https://github.com/bio-ontology-research-group/bh20-seq-resource.git@master
```

4. **Test the tool.** Try running:

```sh
bh20-seq-uploader --help
```

It should print some instructions about how to use the uploader.

**Make sure you are in your virtualenv whenever you run the tool!** If you ever can't run the tool, and your prompt doesn't say `(venv)`, try going to the directory where you put the virtualenv and running `. venv/bin/activate`. It only works for the current terminal window; you will need to run it again if you open a new terminal.

### Installation with `pip3 --user`

If you don't want to have to enter a virtualenv every time you use the uploader, you can use the `--user` feature of `pip3` to install the tool for your user.

1. **Prepare your system.** Just as for the `virtualenv` method, you need to install some dependencies. On Ubuntu 18.04, you can run:

```sh
sudo apt update
sudo apt install -y virtualenv git libcurl4-openssl-dev build-essential python3-dev libssl-dev
```

2. **Install the tool.** You can run:

```sh
pip3 install --user git+https://github.com/arvados/bh20-seq-resource.git@master
```

3. **Make sure the tool is on your `PATH`.** The `pip3` command will install the uploader in `.local/bin` inside your home directory. Your shell may not know to look for commands there by default. To fix this for the terminal you currently have open, run:

```sh
export PATH=$PATH:$HOME/.local/bin
```

To make this change permanent, assuming your shell is Bash, run:

```sh
echo 'export PATH=$PATH:$HOME/.local/bin' >>~/.bashrc
```

4. **Test the tool.** Try running:

```sh
bh20-seq-uploader --help
```

It should print some instructions about how to use the uploader.

## Usage

Run the uploader with a FASTA or FASTQ file and accompanying metadata file in JSON or YAML:

```sh
bh20-seq-uploader example/sequence.fasta example/metadata.yaml
```

### Workflow for Generating a Pangenome

All these uploaded sequences are being fed into a workflow to generate a [pangenome](https://academic.oup.com/bib/article/19/1/118/2566735) for the virus. You can replicate this workflow yourself.

An example is to get your SARS-CoV-2 sequences from GenBank in `seqs.fa`, and then run a series of commands

```sh
minimap2 -cx asm20 -X seqs.fa seqs.fa >seqs.paf
seqwish -s seqs.fa -p seqs.paf -g seqs.gfa
odgi build -g seqs.gfa -s -o seqs.odgi
odgi viz -i seqs.odgi -o seqs.png -x 4000 -y 500 -R -P 5
```

Here we convert such a pipeline into the Common Workflow Language (CWL) and
sources can be found [here](https://github.com/hpobio-lab/viral-analysis/tree/master/cwl/pangenome-generate).

For more information on building pangenome models, [see this wiki page](https://github.com/virtual-biohackathons/covid-19-bh20/wiki/Pangenome#pangenome-model-from-available-genomes).
