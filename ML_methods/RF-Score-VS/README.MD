# RF-Score-VS Benchmark Workflow

This directory documents the workflow used to run **RF-Score-VS** for the machine learning benchmark described in the manuscript:

**“The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.”**

The purpose of this folder is to provide a reproducible procedure for generating RF-Score-VS predictions on the benchmark datasets used in this study.

---

## Method Overview

RF-Score-VS is a **random forest based scoring function for virtual screening**. According to the official repository, the standalone implementation corresponds to **RF-Score-VS v2**, which uses descriptors based on counts of atom types within a **12 Å radius**, divided into **2 Å bins**. :contentReference[oaicite:1]{index=1}

In this benchmark study, RF-Score-VS was used as a classical machine learning scoring function to evaluate how well a random forest based rescoring method can distinguish active ligands from decoys and compare with other machine learning and physics-based affinity predictors.

---

## Original Repository

Official repository:

```text
https://github.com/oddt/rfscorevs
```
The official repository states that the standalone scoring function is distributed separately as platform-specific binaries and that usage instructions for the binary are provided alongside those binaries. It also notes support for Linux, Windows, and macOS.

---

## Supported Input Formats

The standalone RF-Score-VS documentation supports the following ligand formats:

- SDF

- MOL

- MOL2

- PDBQT

- PDB

Protein receptors are provided with the --receptor argument, and file format is determined from the extension when not explicitly specified.

---

## Execution Environment

RF-Score-VS predictions in this study were run in a **Windows environment** using the standalone executable.

The workflow consisted of:

1- Preparing separate benchmark folders

2- Matching each receptor PDB file with its corresponding ligand SDF file

3- Running RF-Score-VS in batch mode using a custom Windows .bat loop

---

## Dataset Organization

Three benchmark folders were prepared:

- DUD-E_actives/

- DUD-E_decoys/

- PDB/

Each folder contains paired input files for the same complex:

- receptor file: *_protein.pdb

- ligand file: *_ligand.sdf

Example structure:

```text
RF-Score-VS/
├── README.md
├── rf-score-vs.exe
├── run_rfscorevs_loop.bat
├── DUD-E_actives/
│   ├── 1abc_protein.pdb
│   ├── 1abc_ligand.sdf
│   └── ...
├── DUD-E_decoys/
│   ├── 2def_protein.pdb
│   ├── 2def_ligand.sdf
│   └── ...
└── PDB/
    ├── 3ghi_protein.pdb
    ├── 3ghi_ligand.sdf
    └── ...
```

---

## Basic Usage

The official RF-Score-VS documentation describes rescoring with commands of the form:
```text
rf-score-vs --receptor protein.pdb ligands.sdf -O ligands_rescored.sdf
```

It also documents CSV output using:

```text
rf-score-vs --receptor protein.pdb ligands.sdf -o csv --field "name" --field "RFScoreVS_v2"
```

The repository states that RF-Score-VS predictions are reported in **-pK units **, and that **higher scores indicate better predicted binding**.

---

## Workflow Used in This Study

In this benchmark, the standalone Windows executable was run on each receptor-ligand pair separately.

A custom batch script was used to:

1- Search each folder for receptor files matching *_protein.pdb

2- Derive the corresponding ligand filename *_ligand.sdf

3- Run RF-Score-VS only when the ligand file exists

4- Save the rescoring result as a CSV file for each complex

---

## Batch Script

The following Windows batch script was used to process all complexes in a folder:


```text
@echo off
setlocal enabledelayedexpansion

set DATA_DIR=actives

for %%P in (%DATA_DIR%\*_protein.pdb) do (
    set BASE=%%~nP
    set BASE=!BASE:_protein=!
    set LIG_FILE=%DATA_DIR%\!BASE!_ligand.sdf
    set OUT_FILE=%DATA_DIR%\!BASE!.csv

    REM Check ligand exists
    if exist "!LIG_FILE!" (
            echo Running RF-Score-VS for !BASE!
            rf-score-vs.exe --receptor "%%P" "!LIG_FILE!" -o csv -O "!OUT_FILE!"
        
        )

    ) else (
        echo [SKIP] Missing ligand for !BASE!
    )
)

echo Done.
pause

```

This script was adapted to run separately for each benchmark folder, including the DUD-E actives, DUD-E decoys, and PDB benchmark sets.

---

## Output Format

Predictions were saved as individual CSV files, one per receptor-ligand pair.

According to the RF-Score-VS documentation, the CSV output appends the prediction in the column:
```text
RFScoreVS_v2
```
The official documentation states that this value is the RF-Score-VS prediction and that higher values indicate stronger predicted binding.

---

## Reproducibility Notes

- The standalone RF-Score-VS executable was used in a Windows environment

- Each receptor-ligand pair was scored separately

- A custom batch script was used to automate prediction across benchmark folders

- Outputs were saved as CSV files

---

## Citation

If you use RF-Score-VS in your work, please cite the official paper listed in the repository:


```bibtex
@article{wojcikowski2017rfscorevs,
  title={Performance of machine-learning scoring functions in structure-based virtual screening},
  author={Wójcikowski, Maciej and Ballester, Pedro J. and Siedlecki, Pawel},
  journal={Scientific Reports},
  volume={7},
  number={1},
  pages={46710},
  year={2017},
  doi={10.1038/srep46710}
}

```
---
## Disclaimer

This folder documents the workflow used to run RF-Score-VS predictions for the benchmark study.

The RF-Score-VS executable and source materials belong to the original authors and should be obtained from the official repository and associated binary distribution. 
