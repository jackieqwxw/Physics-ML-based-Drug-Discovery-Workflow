# Yuel Benchmark Workflow

This directory documents the workflow used to run **Yuel** for the machine learning benchmark described in the manuscript:

**“The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.”**

The purpose of this folder is to provide a reproducible procedure for generating compound–protein interaction predictions using Yuel on the benchmark datasets used in this study.

---

## Method Overview

Yuel is a **structure-free compound–protein interaction (CPI) prediction model** designed to predict binding affinity between small molecules and proteins with high generalizability.

Unlike many neural network models that rely on fully connected layers applied to combined protein–ligand features, Yuel applies fully connected layers only to **individual atom features and residue features**. The compound–protein interaction score is then calculated by summing the pairwise interactions between compound atoms and protein residues.

This design allows Yuel to learn interaction patterns while reducing overfitting and improving generalization across different datasets.

---

## Original Repository

Official repository:

https://bitbucket.org/dokhlab/yuel


This repository documents how the original Yuel implementation was used to generate predictions for the benchmark datasets used in our study.

---

## Requirements

The Yuel implementation requires the following software:

```text
Python 3
pandas
numpy
matplotlib
rdkit
tensorflow==2.3.0
tensorflow-probability
dm-sonnet
graph_nets
```

A Docker image containing the required environment is also available:
```text
docker pull juw1179/yuel:0.0.1
```
---

## Dataset Format

Yuel expects the input dataset as a CSV or TSV file containing compound and protein information.

Typical dataset columns include:

  - Compound (SMILES or InChI)

  - Compound type (smi or inchi)

  - Protein sequence

  - Binding affinity

Example columns:


```text
Compound,CompType,Protein,Affinity
```

Notes:

- If the compound column contains SMILES, the compound type must be smi

- If the compound column contains InChI, the compound type must be inchi

- The protein column must contain the amino acid sequence

- The affinity column must be present even during prediction (can be filled with placeholder values)

---

## Prediction
```text
Example prediction command:
python yuel.py predict \
--data=data/pdbbind-test.csv \
--compound_column=Ligand \
--compound_type_column=CompType \
--protein_column=Sequence \
--affinity_column=Affinity \
--comp_size=64 \
--nfeat=32 \
--prot_size=2048 \
--model=models/pdbbind.model
```
---

## Custom Dataset Prediction

To run predictions on a custom dataset:

  1-Prepare a dataset file containing compound SMILES and protein sequences.

  2-Ensure the required columns are defined.

  3-Provide a placeholder value for the affinity column.

Example dataset format:
```text
Compound,CompType,Protein,Affinity
CCO,smi,MKVLWAALLVTFLAGCQAKVE...,0
CCN,smi,MGDVEKGKKIFIMKCSQCHTV...,0
```
---

## Directory Structure

Typical contents of this folder include:

```text
Yuel/
├── README.md
├── run_yuel_prediction.sh
├── dataset/
├── outputs/
└── logs/
```
---

##  Reproducibility Notes

The original Yuel implementation was used without modification.

Predictions were generated using the pre-trained models provided by the authors.

Dataset formatting followed the structure required by the Yuel prediction interface.

Large datasets and output files may not be included in this repository due to GitHub storage limitations

---
##  Citation

If you use Yuel in your work, please cite the original publication:

Yuel: Compound–Protein Interaction Prediction with High Generalizability

---

##  Disclaimer

This folder documents the workflow used to run Yuel predictions for the benchmark study.

The Yuel model and source code belong to the original authors and are available through their official repository.
