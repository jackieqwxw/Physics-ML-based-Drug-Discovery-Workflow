# TopologyNet Benchmark Workflow

This directory documents the workflow used to run **TopologyNet** for the machine learning benchmark described in the manuscript:

**“The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.”**

The purpose of this folder is to provide a reproducible procedure for generating binding affinity predictions using TopologyNet on the benchmark datasets used in this study.

---

## Method Overview

TopologyNet is a deep learning framework for predicting protein–ligand binding affinity using **topological descriptors derived from persistent homology**. Instead of relying only on traditional structural or physicochemical features, the method encodes the spatial structure of protein–ligand complexes using topological invariants that capture geometric and interaction patterns.

These topological representations are then processed using neural networks to predict binding affinity values.

In this benchmark study, TopologyNet was used as a representative topology-based deep learning approach to evaluate how topological descriptors perform in comparison with other machine learning scoring functions and physics-based binding free energy methods.

---

## Original Repository

Official implementation used in this study:

https://github.com/longyuxi/TopologyNet-2017


The original implementation provides scripts for computing topological descriptors from protein–ligand complexes and applying neural network models for binding affinity prediction.

This repository documents the workflow used to run TopologyNet predictions on the benchmark datasets.

---

## Requirements

The TopologyNet implementation requires a Python environment with several scientific computing libraries.

Typical dependencies include:

```text
Python 3
numpy
scipy
pandas
scikit-learn
tensorflow
```

Additional tools may be required for generating topological descriptors from protein–ligand structures depending on the specific configuration of the TopologyNet implementation

---
##  Input Preparation

TopologyNet operates on protein–ligand complexes and requires prepared structural data.

In this study, the following preparation steps were applied:

1- Protein structures were prepared in PDB format

2- Ligand structures were prepared in SDF format

3- Protein–ligand complexes were organized according to the benchmark datasets

4- Topological descriptors were generated using the TopologyNet feature extraction scripts

These descriptors were then used as input features for the TopologyNet prediction model.

---

##  Prediction Workflow

TopologyNet predictions were generated using the scripts provided in the original repository.

The workflow consists of the following steps:

1- Generate topological descriptors from protein–ligand complexes

2- Construct feature matrices for machine learning models

3- Apply the trained TopologyNet model to predict binding affinity values

These predictions were then collected and used for comparison with other machine learning and physics-based affinity predictors included in the benchmark study.

---

##  Automation


To simplify reproducibility and facilitate large-scale benchmarking, automation scripts were used to run TopologyNet predictions across multiple complexes.

These scripts allow batch execution of descriptor generation and prediction steps for all protein–ligand pairs in the dataset.

---

##  Directory Structure

Typical contents of this folder include:

```text
TopologyNet/
├── README.md
├── run_topologynet.sh
├── PDBBind/
│   └── index.csv
│   └── 1b8y_protein.pdb
│   └── 1b8y_ligand.sdf
│   └── 1b8y_ligand.mol2
│   └── 1bju_protein.pdb
│   └── 1bju_ligand.sdf
│   └── 1bju_ligand.mol2
├── DUD-E/
│   └── index.csv
│   └── 1A28.pdb
│   └── 1A28_0.sdf
│   └── 1A28_0.mol2
│   └── 1CVU.pdb
│   └── 1CVU_0.sdf
│   └── 1CVU_0.mol2
├── features/
└── outputs/
```

Where:

- run_topologynet.sh – shell script used to automate prediction runs

- dataset/ – prepared protein–ligand complexes

- features/ – generated topological descriptors

- outputs/ – predicted binding affinity values

---

##  Reproducibility Notes

The original TopologyNet implementation was used without modification.

Protein–ligand complexes were prepared using the same preprocessing pipeline used for other machine learning methods in this study.

Predictions were generated using the provided scripts and aggregated for benchmarking analysis.

Large intermediate files (feature matrices or descriptor outputs) may not be included in this repository due to GitHub storage limitations.


---

##  Citation

If you use TopologyNet in your research, please cite the original paper:

TopologyNet: Topology Based Deep Convolutional Neural Networks for Biomolecular Property Predictions

Additional details and implementation are available in the official repository.


```bibtex
@article{cang2017topologynet,
  title={TopologyNet: Topology based deep convolutional and multi-task neural networks for biomolecular property predictions},
  author={Cang, Zixuan and Wei, Guo-Wei},
  journal={PLOS Computational Biology},
  volume={13},
  number={7},
  pages={e1005690},
  year={2017},
  doi={10.1371/journal.pcbi.1005690},
  url={https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005690}
}
```
---

##  Disclaimer

This folder documents the workflow used to run TopologyNet predictions for the benchmark study.

The TopologyNet implementation and source code belong to the original authors and are distributed through their official repository.
