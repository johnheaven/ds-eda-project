# Exploratory Data Analysis (EDA) project – first Neue Fische assignment

This repository is based on a Neue Fische template. The assignment was to explore publicly available data on house prices in King County, USA. The data covers the period from May 2014 to 2015. We were given a choice of fictitious scenarios to choose from and had to advise a putative client on investment decisions.

Because the data is for past sales, not asking prices of available houses, I took the approach of attempting to draw some inferences from the data and assuming that they would still hold in the future.

The Jupyter notebook can be found here: [Jupyter notebook](./EDA.ipynb).

Part of the assignment was a presentation of results. You can view this [here](./EDA%20presentation.pdf), although I have updated the notebook since presenting it and may continue to do so.

* Details of the assignment: [assignment.md](./assignment.md)

* Description of an EDA workflow (by Neue Fische): [workflow.md](./workflow.md)

The Jupyter notebook should be viewable on GitHub, but if you wish to download this and kick the tyres, be my guest.

## Requirements

See requirements.txt and setup information below.

## Setup

```
pyenv local 3.11.1
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
