# Boltz-2 Benchmark Workflow

This directory documents the workflow used to run **Boltz-2** for the machine learning benchmark described in the manuscript:

**The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.**    

The purpose of this folder is to provide a reproducible workflow for generating **Boltz-2** binding affinity predictions on the benchmark datasets used in this study.

---

## Method Overview

Boltz is a family of biomolecular interaction models. According to the official repository, **Boltz-2** is a biomolecular foundation model that jointly models complex structures and binding affinities. The repository states that the model is designed for efficient affinity prediction and provides both code and model weights under the MIT license. 

In this benchmark study, Boltz-2 was used as an additional machine learning affinity predictor to evaluate its performance in comparison with physics-based methods and other AI scoring functions in virtual screening workflows.

---

## Original Repository

Official repository:

```text
https://github.com/jwohlwend/boltz
```

---

The workflow documented here uses the original Boltz implementation and command-line interface provided by the authors. The official repository documents inference with:

```text
boltz predict input_path --use_msa_server
```

where input_path can be a single YAML file or a directory of YAML files for batched processing.

---

## Installation

The official repository recommends installation in a fresh Python environment. It documents installation with:

```text
pip install boltz[cuda] -U
```

or, for development installation from GitHub:

```text
git clone https://github.com/jwohlwend/boltz.git
cd boltz
pip install -e .[cuda]
```

---

For CPU-only or non-CUDA systems, the repository notes that [cuda] should be removed, although GPU execution is expected to be much faster

## HPC Execution

Boltz-2 predictions in this study were run on an HPC environment.

The workflow consisted of two main steps:

    1- Preparing one YAML input file for each protein-ligand complex

    2- Running Boltz-2 predictions in batch mode using a shell script loop, This setup allowed automated execution across the benchmark dataset.

---

## Input Preparation

**Boltz-2** accepts YAML input files describing the biomolecules and the requested predictions. The official repository states that input\_path may refer either to a single YAML file or to a directory of YAML files for batched prediction.

In this study, one YAML file was prepared for each protein-ligand complex.

Typical organization:

```text
Boltz-2

├── README.md/
├── RunBDB.sh/
├── RunDUD-E.sh/
├── DUD-E/
│   ├── 3bz3_1.yaml
│   ├── 3bz3_2.yaml
│   └── ...
├── PDB/
│   ├── 1c5x.yaml
│   ├── 1cet.yaml
│   ├── 1d3d.yaml
│   ├── 1d3p.yaml
│   └── ...
├── outputs/
│   ├── boltz_results_1c5x.yaml
│   ├── boltz_results_1cet.yaml
│   ├── boltz_results_1d3d.yaml
│   └── ...
└── logs/
```
---
## Prediction Command

Boltz-2 predictions were run using the command documented in the official repository:
```text
        boltz predict input_path --use_msa_server
```
In our workflow, input_path referred either to a single YAML file or to a directory containing multiple YAML files. The --use_msa_server option was used during prediction, consistent with the official inference instructions.

Batch Prediction Workflow

To process all benchmark complexes automatically, a shell script loop was used.

The batch workflow performed the following steps:

        1-Read YAML input files prepared for each protein-ligand complex

        2-Submit a Boltz-2 prediction for each file

        3-Store prediction outputs in the output directory

        4-Save logs for monitoring and troubleshooting on HPC

Example execution pattern:

for f in yaml_inputs/*.yaml; do
   boltz predict "$f" --use_msa_server

done

If the official CLI was pointed to a directory directly, Boltz-2 could also process all YAML files in batch mode from that directory, as described in the repository documentation.

## Output Interpretation

The official repository describes two main affinity-related outputs:   affinity_pred_value  and affinity_probability_binary

According to the repository documentation:   affinity_probability_binary should be used to distinguish binders from decoys in hit discovery settings, affinity_pred_value is intended for comparing affinities among binders and is reported as log10(IC50), derived from IC50 values measured in μM.  In this study, Boltz-2 outputs were collected and organized for downstream comparison with other binding affinity predictors used in the benchmark.

---
##  Citation

If you use Boltz-2, please cite the official Boltz publications listed in the original repository. The repository provides citation information for both Boltz-2 and Boltz-1.

```text
@article{passaro2025boltz2,
  author = {Passaro, Saro and Corso, Gabriele and Wohlwend, Jeremy and Reveiz, Mateo and Thaler, Stephan and Somnath, Vignesh Ram and Getz, Noah and Portnoi, Tally and Roy, Julien and Stark, Hannes and Kwabi-Addo, David and Beaini, Dominique and Jaakkola, Tommi and Barzilay, Regina},
  title = {Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction},
  year = {2025},
  doi = {10.1101/2025.06.14.659707},
  journal = {bioRxiv}
}

@article{wohlwend2024boltz1,
  author = {Wohlwend, Jeremy and Corso, Gabriele and Passaro, Saro and Getz, Noah and Reveiz, Mateo and Leidal, Ken and Swiderski, Wojtek and Atkinson, Liam and Portnoi, Tally and Chinn, Itamar and Silterra, Jacob and Jaakkola, Tommi and Barzilay, Regina},
  title = {Boltz-1: Democratizing Biomolecular Interaction Modeling},
  year = {2024},
  doi = {10.1101/2024.11.19.624167},
  journal = {bioRxiv}
}
```



