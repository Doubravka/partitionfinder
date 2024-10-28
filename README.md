# How to get started 🚀

This verison is intended to run with python3 and [uv](https://docs.astral.sh/uv/) as package manager.
The package manager uses [pyproject.toml](pyproject.toml) to know which packages to install.

1. Have python 3 installed.

2. Get `uv`. There are many options how to install uv. Here is an example with pip:

```
pip install uv
uv 
```

3. Run the program from the project folder. For example: 
```
uv run PartitionFinder.py examples/nucleotide
```
The packages listed in [pyproject.toml](pyproject.toml) will get installed to a python virtual environment (.venv folder in the root of the project). Python version specified in [.python-version](.python-version) will be used. The virtual environment will be used for the execution.


# PartitionFinder 2

PartitionFinder 2 is a Python program for simultaneously 
choosing partitioning schemes and models of molecular evolution for phylogenetic analyses of DNA, protein, and morphological data. 
You can PartitionFinder 2 before running a phylogenetic analysis, in order
to decide how to divide up your sequence data into separate blocks before
analysis, and to simultaneously perform model selection on each of those
blocks.


# Operating System

Mac/Windows/Linux

# Manual

The manual includes installation instructions, quickstart, and (very) detailed instructions.

* Enlgish: PDF is in the `/docs` folder. 
* Chinese: [can be viewed here](http://htmlpreview.github.io/?https://github.com/brettc/partitionfinder/blob/master/docs/PartitionFinder2%E7%9A%84%E4%B8%80%E8%88%AC%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95%EF%BC%88%E4%B8%AD%E6%96%87%E7%89%88-%E7%BD%91%E9%A1%B5%E7%89%88%EF%BC%89.html), or in the `/docs` folder if you want the raw HTML


# Tutorial / walk through

www.robertlanfear.com/partitionfinder/tutorial