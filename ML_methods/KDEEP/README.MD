## KDEEP Benchmark Workflow

This directory documents the procedure used to generate **KDEEP binding affinity predictions** for the benchmark described in the manuscript:

** “The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.”**

KDEEP predictions were generated using the **PlayMolecule web platform**, which provides an implementation of the KDEEP deep learning model.

---

## Method Overview

KDEEP is a deep learning scoring function designed to predict ** absolute protein–ligand binding affinity** using **3D convolutional neural networks (3D-CNNs)** applied to voxelized representations of protein–ligand complexes.

The model encodes the binding site environment into a three-dimensional grid describing physicochemical properties of both the protein and ligand. A convolutional neural network then learns the relationship between these spatial descriptors and experimental binding affinities.

The method was trained using the **PDBbind database** and achieves strong correlation between predicted and experimental binding affinities in benchmark datasets.

In this study, KDEEP was used as a **deep learning baseline scoring function** to compare with other machine learning and physics-based affinity prediction methods.

---



---




---




---




---





---





---







---






---






---
