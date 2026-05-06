# 5GDHC Framework - Thermal Synergy Module

This repository contains the reproducible Python component of the 5GDHC Framework developed within NEST PNRR Task 8.4.7.

The module implements a Thermal Synergy analysis for early-stage screening of building groups in fifth-generation district heating and cooling applications. It processes hourly thermal demand profiles and computes TS/TSI indicators to identify promising combinations of users with complementary thermal needs.

## Contents
- `analysis.ipynb`: Jupyter notebook implementing the Thermal Synergy workflow
- `configNY.xlsx`: example configuration file
- `dataNY.xlsx`: example input dataset
- `simRes.xlsx`: example output/result file

## How to run
Open `analysis.ipynb` in Jupyter Notebook, JupyterLab or VS Code, ensure that the Excel files are in the same working directory, and run all cells sequentially.

## Requirements
Python 3.x, pandas, numpy, matplotlib, openpyxl.
