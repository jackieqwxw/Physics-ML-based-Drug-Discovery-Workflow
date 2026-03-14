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

## Original Tool

KDEEP predictions were generated using the PlayMolecule platform:

PlayMolecule              https://open.playmolecule.org/

KDEEP tool page:              https://open.playmolecule.org/tools/kdee

---

## Input Dataset Preparation

Each protein–ligand complex was prepared in the following format:

```text
system_name_protein.pdb
system_name_ligand.sdf
```

Example:

```text
1b8y_protein.pdb
1b8y_ligand.sdf
```

A dataset index file was also prepared:

```text
index.csv
```

Example structure:

systemname,proteinpath,ligandpath,label
1b8y,1b8y_protein.pdb,1b8y_ligand.sdf,0

All input files were compressed into a single archive:

```text
dataset.zip
```

---

## Running KDEEP Predictions

KDEEP predictions were generated using the PlayMolecule web interface.

###  Step 1 – Open PlayMolecule

Navigate to:

```text
https://open.playmolecule.org/tools
```

Select:

```text
KDEEP – Binding Affinity Prediction
```

###  Step 2 – Select Advanced Options

Enable:

```text
Advanced Options
```
Then choose:

```text
Protein-Ligand Dataset
```
Upload the prepared dataset archive:

```text
dataset.zip
```

###  Step 3 – Model Selection

Use the default KDEEP model:

```text
default.ckpt
```

Provide a job name and submit the job.

###  Step 4 – Run Prediction

After submission:

- the PlayMolecule server processes the dataset

- predictions are generated for all protein–ligand complexes

Typical runtime for the dataset used in this study was approximately:  
```text
~3 hours
```

---

## Output Files

After job completion, the results can be downloaded as a **CSV file**.

The output CSV contains several columns including:

```text
pdb_id
Ligand
SMILES
Kd/Ki(M)
Gexp
Gpbsa
abs_Error
norm_ΔGexp
norm_ΔGcalc
norm_Error
class
dG [kcal/mol] mean predict
```

---

## Benchmark Value Used in This Study

For the benchmarking analysis reported in the manuscript, the following column was used:

```text
dG [kcal/mol] mean predict
```

This value represents the predicted **binding free energy generated** by the KDEEP model and was used for comparison with other machine learning scoring functions.

---

## Reproducibility Notes

- KDEEP predictions were generated using the **PlayMolecule server implementation.**

- The **default pretrained model** (default.ckpt) was used.

- No retraining or modification of the KDEEP model was performed.

- Input datasets were prepared according to the required PlayMolecule format.

---


## Citation

If you use KDEEP in your research, please cite:

Jiménez J., Škalič M., Martínez-Rosell G., De Fabritiis G.
KDEEP: Protein–Ligand Absolute Binding Affinity Prediction via 3D-Convolutional Neural Networks
Journal of Chemical Information and Modeling, 58, 287-296 (2018).
https://doi.org/10.1021/acs.jcim.7b00650

### BibTeX

```bibtex
@article{jimenez2018kdeep,
  title={KDEEP: Protein–Ligand Absolute Binding Affinity Prediction via 3D-Convolutional Neural Networks},
  author={Jiménez, José and Škalič, Miha and Martínez-Rosell, Gerard and De Fabritiis, Gianni},
  journal={Journal of Chemical Information and Modeling},
  volume={58},
  number={2},
  pages={287--296},
  year={2018},
  doi={10.1021/acs.jcim.7b00650}
}


