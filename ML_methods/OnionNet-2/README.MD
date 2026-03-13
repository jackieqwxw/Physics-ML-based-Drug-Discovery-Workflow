# OnionNet-2 Benchmark Workflow

This directory documents the workflow used to run the **OnionNet-2** model for the machine learning benchmark described in the manuscript:

**“The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.”**

The purpose of this folder is to provide a reproducible procedure for generating binding free energy predictions using OnionNet-2 on the benchmark datasets used in this study.

---

## Overview

OnionNet-2 is a convolutional neural network model designed to predict protein-ligand binding affinity using residue-atom contact features.

In this study, OnionNet-2 was used as one of several machine learning models benchmarked against physics-based binding free energy methods and other AI approaches.

The model was applied to protein-ligand complexes from two benchmark datasets:

- **PDBbind dataset**
- **DUD-E dataset**

---

## Original OnionNet-2 Repository

The original implementation of OnionNet-2 is available at:     https://github.com/zchwang/OnionNet-2


This repository does not re-implement the OnionNet-2 model. Instead, it documents how the original code was used to generate predictions for our benchmark datasets.

---

## Environment Setup

The OnionNet-2 environment was created following the installation instructions from the original repository.

## Required Packages

The following software versions were used:

```text
python >= 3.8
tensorflow==2.3
pandas==1.3.4
scikit-learn==0.22.1
joblib==1.0.1
numpy==1.18.5
scipy==1.4.1

```
If GPU acceleration is available, `tensorflow-gpu==2.3` may be used instead of `tensorflow==2.3`.

---

## Installation Example

Create and activate a conda environment:

```bash
conda create -n onionnet2 python=3.8
conda activate onionnet2
```
```bash
Install required packages:
pip install tensorflow==2.3
pip install pandas==1.3.4
pip install scikit-learn==0.22.1
pip install joblib==1.0.1
pip install numpy==1.18.5
pip install scipy==1.4.1
```
Clone the original OnionNet-2 repository:
```bash
git clone https://github.com/zchwang/OnionNet-2

```
---

##  Input Preparation

Protein and ligand structures were prepared prior to running OnionNet-2.

- **Protein Preparation**  Proteins were prepared by:

    Removing bound ligands

    Adding hydrogen atoms

    Saving the resulting structures in PDB format

    OpenBabel was used for these steps.

- **Ligand Preparation**  Ligands were prepared by:

    Generating 3D coordinates

    Adding hydrogen atoms

    Saving the structures in SDF format

These prepared protein and ligand structures were then used as inputs for OnionNet-2 predictions.

- **Dataset Structure**

    The dataset used for prediction is indexed using a CSV file:   dataset/PDB/index.csv

    This file contains paths to protein and ligand structures.

Example structure:

proteinpath,ligandpath
./ACE/protein.pdb,./ACE/ligand1.sdf

./ACE/protein.pdb,./ACE/ligand2.sdf

---
## Pre-trained Model Files

OnionNet-2 requires the pre-trained model and scaler files.

These files are not included in this repository due to GitHub size limits.

They can be obtained from the original OnionNet-2 repository:

https://zenodo.org/records/10728089/62shell_saved-model.h5

https://github.com/zchwang/OnionNet-2/tree/master/models/train_scaler.scaler

---

##  Prediction Workflow

Predictions were generated using the predict.py script provided in the original OnionNet-2 repository.

To automate prediction across the entire dataset, a batch script was used to iterate through the entries in index.csv.

Each iteration performs the following steps:

-  Read protein and ligand paths from the dataset index

-  Construct absolute paths to input files

-  Run OnionNet-2 prediction

Store the predicted binding affinity
---
##  Example Prediction Command

The OnionNet-2 prediction script is executed as follows:
```bash
python predict.py \
-rec_fpath protein.pdb \
-lig_fpath ligand.sdf \
-shape 84,124,1 \
-scaler scaler.save \
-model model.h5 \
-shells 62 \
-out_fpath prediction.txt
```

Where:

- rec_fpath = protein structure file

- lig_fpath = ligand structure file

- shape = input tensor shape used by the model

- scaler = saved feature scaler

- model = trained OnionNet-2 model

- shells = number of residue-atom shells

- out_fpath = output prediction file
---
##  Batch Prediction Script

To process all complexes in the dataset automatically, we used a loop script:

```bash
run_onionnet2_loop.sh
```

This script:

Reads index.csv

Iterates over each protein-ligand pair

Runs OnionNet-2 predictions

Collects predicted values

---
##  Output Format

All predicted values were collected into a single CSV file:

onionnet2_predictions.csv

Example output:

proteinpath,ligandpath,prediction
./ACE/protein.pdb,./ACE/lig1.sdf,-9.21

./ACE/protein.pdb,./ACE/lig2.sdf,-7.55

./ACE/protein.pdb,./ACE/lig3.sdf,-8.04

This output file preserves the original dataset index and adds a column containing the predicted binding affinity.

---
##  Files in this Directory

Typical contents of this folder include:

OnionNet-2/
├── README.md

├── run_onionnet2_loop.sh

├── run_onionnet2_predictions.py

├── PDB database/

├── DUD-E/

└── model/

---
##  Reproducibility Notes

OnionNet-2 was used exactly as implemented in the original repository.

The only modification introduced in this workflow was the automation of predictions across the benchmark datasets.

All input preparation steps and execution parameters are documented here to enable reproducibility.

---
##  Citation

If you use OnionNet-2 in your work, please cite the original publication:

Wang Z, Zheng L, Liu Y, Qu Y, Li YQ, Zhao M, Mu Y, Li W.

OnionNet-2: A Convolutional Neural Network Model for Predicting
Protein-Ligand Binding Affinity Based on Residue-Atom Contacting Shells.
Frontiers in Chemistry. 2021.


---
##  Disclaimer

This folder documents the workflow used in our benchmark study.

The OnionNet-2 model and source code belong to the original authors.
Please refer to the original repository for the official implementation and license information.


