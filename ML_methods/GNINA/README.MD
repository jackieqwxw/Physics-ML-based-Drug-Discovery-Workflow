# GNINA Benchmark Workflow

This directory documents the procedure used to generate ** GNINA docking predictions ** for the benchmark described in the manuscript:

**“The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.”**

GNINA was used as a ** deep learning–enhanced docking and scoring method ** to evaluate protein–ligand binding affinity predictions in comparison with other machine learning and physics-based methods.
---

```text
GNINA
```
---



---

## Method Overview

GNINA is a molecular docking tool derived from AutoDock Vina that incorporates convolutional neural networks (CNNs) to improve scoring and pose ranking of protein–ligand complexes.

The CNN models evaluate the binding interaction between the protein and ligand using a 3D representation of the binding site, allowing improved scoring compared to classical docking scoring functions.

GNINA can perform:

- traditional docking

- CNN-based rescoring

- CNN-based pose ranking

In this benchmark study, GNINA was used to generate docking predictions and the predicted binding affinity values were extracted from the docking output

---

## Original Resources

GNINA GitHub repository:

https://github.com/gnina/gnina

GNINA workshop tutorial:

https://gnina.github.io/gnina/rsc_workshop2021/#/

Google Colab tutorial used in this study:

https://colab.research.google.com/drive/1GXmk1v8C-c4UtyKFqIm9HnsrVYH0pI-c

---

## Execution Environment

GNINA predictions were generated using Google Colab following the official GNINA tutorial workflow.

The provided tutorial code was used without modification except for adapting file paths to run batch predictions across the benchmark dataset.

---

##  GNINA Installation and Usage

This section explains how to install GNINA and run docking and scoring workflows similar to those used in this benchmark.

The commands below follow the setup used in the Google Colab environment.

---

###  1. Install Required Tools

GNINA depends on molecular processing tools such as OpenBabel and Python libraries for visualization.

#### Install OpenBabel

```bash
!apt install openbabel
```

Purpose:

converts molecular formats

prepares ligand structures

commonly used in docking pipelines

---

#### Install Miniconda

```bash
!wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
!chmod +x Miniconda3-latest-Linux-x86_64.sh
!bash ./Miniconda3-latest-Linux-x86_64.sh -b -f -p /usr/local
```

Purpose:

provides package management

installs scientific dependencies easily

---

#### Install OpenBabel via Conda

```bash
!conda install -q -y -c conda-forge openbabel
```
Purpose:

ensures compatibility with GNINA molecular processing tools

---

#### Configure Python Path

```bash
import sys
sys.path.append('/usr/local/lib/python3.8/site-packages/')
```
Purpose:

ensures installed packages are available to Python
---

#### Install Visualization Library

```bash
!pip install py3Dmol
```
Purpose:

enables 3D visualization of docking results in notebooks

---
### 2. Download GNINA

Download the GNINA executable.

```bash
!wget https://github.com/gnina/gnina/releases/download/v1.0.1/gnina
```
Make the binary executable.

```bash
!chmod +x gnina
```
Verify installation.

```bash
!./gnina
```
This prints the GNINA help message.

---

### 3. Basic Docking Example

GNINA docking requires:

receptor structure (PDB)

ligand structure (SDF or PDB)

Example command:

```bash
!./gnina -r rec.pdb -l lig.pdb --autobox_ligand lig.pdb
```

Explanation of options:

Option	Meaning
-r	receptor structure
-l	ligand structure
--autobox_ligand	automatically define docking box around ligand

This performs docking and prints predicted poses and affinity scores.

---

### 4. Save Docking Output

To save docking results:

```bash
!./gnina -r rec.pdb -l lig.pdb --autobox_ligand lig.pdb --seed 0 -o docked.sdf.gz
```

Explanation of additional options:

Option	Meaning

```bash
--seed 0	ensures reproducibility
```
-o	output file containing docking poses

Output file:

```bash
docked.sdf.gz
```

Each pose contains predicted affinity values.
---

### 5. Scoring Only (No Docking)

GNINA can also score an existing pose.

```bash
!./gnina --score_only -r rec.pdb -l lig.pdb --verbosity=2
```

Purpose:

evaluate affinity without running docking

useful for rescoring docked poses

---

### 6. Inspect Scoring Functions

```bash
To list scoring options:
!./gnina --help | grep scoring | head -3
```

To print scoring terms used by GNINA


```bash
!./gnina --print_terms
```

These commands show how GNINA computes its predicted binding affinity.

---
Input Dataset

The dataset used in this study contains:


```bash
index.csv
1b8y_protein.pdb
1b8y_ligand.sdf
```
---


## Batch Docking Script

The GNINA docking workflow was automated by looping over all entries in index.csv.

Example code used in the Colab environment:


```bash
-r                 receptor structure (PDB)
-l                 ligand structure (SDF)
--autobox_ligand   automatically define docking box using ligand
--cnn_rotation 1   enable CNN rotation evaluation
--num_modes 30     generate up to 30 docking poses
--seed 0           fixed seed for reproducibility
-o                 output docking poses
```

---

## Output Files

GNINA produces an SDF output file for each docking run.


```bash
Example output:
result_docking3/
0_1b8y.sdf
1_2xyz.sdf
2_3abc.sdf
```

Each SDF file contains docking poses and associated scoring information.

---

## Benchmark Value Used in This Study

For the benchmarking analysis reported in the manuscript, the following value was extracted from the GNINA output:
Affinity (kcal/mol)

This value corresponds to the predicted binding affinity reported by GNINA for each docking pose.

The best-scoring pose affinity value was used as the GNINA prediction for benchmarking comparisons.
---


## Reproducibility Notes

- GNINA docking was executed using the official tutorial workflow.

- The execution environment was Google Colab.

- The only modification made to the tutorial code was the addition of a loop to process all protein–ligand complexes listed in index.csv.

- Output affinity values were extracted directly from the generated SDF files.
---


## Citation

If you use GNINA in your research, please cite:

GNINA project:

```bash
https://github.com/gnina/gnina
```


If you use GNINA in your research, please cite:

McNutt, A. T.; Francoeur, P.; Aggarwal, R.; Masuda, T.; Meli, R.; Ragoza, M.; Sunseri, J.; Koes, D. R.  
**GNINA 1.0: Molecular Docking with Deep Learning.**  
Journal of Cheminformatics, 13, 43 (2021).  
https://doi.org/10.1186/s13321-021-00522-2

### BibTeX

```bibtex
@article{mcnutt2021gnina,
  title={GNINA 1.0: Molecular Docking with Deep Learning},
  author={McNutt, Andrew T and Francoeur, Paul and Aggarwal, Rishabh and Masuda, Tomohiro and Meli, Ryan and Ragoza, Matthew and Sunseri, Jocelyn and Koes, David R},
  journal={Journal of Cheminformatics},
  volume={13},
  number={1},
  pages={43},
  year={2021},
  doi={10.1186/s13321-021-00522-2}
}
```




