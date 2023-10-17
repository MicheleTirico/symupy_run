# Symupy run

## Installation

Using [conda](https://docs.conda.io/en/latest/miniconda.html), create a new environment:

````bash
conda env create -f env.yaml
````

Activate it:
````bash
conda activate symupy
````

Update the environment:
````bash
conda env update --name symupy --file  env.yaml --prune
````

Install or update toolbox package:
````bash
pip install git+https://github.com/MicheleTirico/toolbox.git
````
