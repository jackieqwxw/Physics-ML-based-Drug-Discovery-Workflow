# Physics- and ML-Integrated CADD Workflow

This repository provides a hybrid workflow combining physics-based molecular simulations and machine learning methods for small-molecule drug discovery. 

## Part I: Physics-Based Free Energy Methods
### Overview
The physics module predicts protein–ligand binding free energies using alchemical simulations (e.g., FEP) and two-point methods (e.g., MM/GBSA, MM/PBSA).
   ### Software Environment
   Tested on:
   - AMBER 22
   - Schrödinger 2024-2
   - GROMACS 2022
   - gmx_MMPBSA v1.6.x
   - Gaussian 16
   - Open Babel
   - SLURM-based HPC environment
   
   ### Required User Inputs
   - Ligand structures (SDF)
   - Protein structure (PDB)
   
   ### Provided by This Repository
   - Parameterization scripts
   - MD input templates
   - MM/PB(GB)SA workflows
   - FEP setup and analysis scripts
   
   ### Quick Start (Minimal Example)
   1. Prepare ligand SDF and protein PDB
   2. Run ligand parameterization:
      cd LigPara && sbatch LigPara.sh ligands.sdf 0
   3. Compute free energies using MM/PB(GB)SA:
      cd MMPBSA && sbatch gmxmmpbsa.sh
   4. Compute free energies using FEP:
      cd FEP && sbatch FEP.sh
   
   ### Common Pitfalls
   - Ensure ligands with different net charges are separated into different SDF files
   - Separate complexes with and without ions
   - Check periodic boundary conditions before MM/PB(GB)SA
   - Ensure consistent atom naming between topology and trajectory

## Part II: Machine Learning–Based Free Energy Prediction
# Machine Learning Methods

This directory contains the workflows and documentation for the machine learning scoring functions evaluated in this study:

**“The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.”**

The purpose of this folder is to provide reproducible procedures for running the machine learning models used to benchmark binding affinity prediction and virtual screening performance.

Each subdirectory corresponds to a specific machine learning scoring function and contains instructions describing how the model was installed, executed, and applied to the benchmark datasets used in this study.

---

## Overview

Machine learning scoring functions have become widely used tools in computational drug discovery. These models aim to predict protein–ligand binding affinity or improve the ranking of docking poses by learning interaction patterns from structural or physicochemical descriptors.

In this study, several representative machine learning approaches were evaluated and compared with physics-based binding free energy methods.

The selected models represent different methodological categories, including deep learning, topology-based learning, and classical machine learning scoring functions.

---

## Implemented Methods

The following machine learning methods were evaluated:

| Method | Type | Description |
|------|------|------|
| **OnionNet-2** | Deep learning | CNN model based on residue–atom interaction shells |
| **KDEEP** | Deep learning | 3D convolutional neural network for binding affinity prediction |
| **TopologyNet** | Deep learning | Topology-based model using persistent homology features |
| **Yuel** | Deep learning | Graph neural network model for protein–ligand interaction prediction |
| **GNINA** | Deep learning / docking | Docking software with CNN-based scoring functions |
| **Boltz-2** | Machine learning | Statistical scoring function using interaction descriptors |
| **RF-Score-VS** | Machine learning | Random forest model based on atom-type contact counts |

---

## Directory Structure

Each method has its own folder containing the workflow used in this benchmark.

```text
ML_methods/
├── README.md
├── OnionNet-2/
├── KDEEP/
├── TopologyNet/
├── Yuel/
├── GNINA/
├── Boltz-2/
└── RF-Score-VS/
```

### Overview
