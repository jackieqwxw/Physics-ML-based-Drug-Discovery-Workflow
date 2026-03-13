## Boltz-2

# Boltz-2 Benchmark Workflow

This directory documents the workflow used to run \*\*Boltz-2\*\* for the machine learning benchmark described in the manuscript:

*“The Last Mile Problem: A Critical Assessment of Physics-based and AI Tools in Virtual Screening.”

The purpose of this folder is to provide a reproducible workflow for generating Boltz-2 binding affinity predictions on the benchmark datasets used in this study.

---



## Method Overview



Boltz is a family of biomolecular interaction models. According to the official repository, \*\*Boltz-2\*\* is a biomolecular foundation model that jointly models complex structures and binding affinities. The repository states that the model is designed for efficient affinity prediction and provides both code and model weights under the MIT license. :contentReference\[oaicite:1]{index=1}



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

boltz predict input\_path --use\_msa\_server

```



where input\_path can be a single YAML file or a directory of YAML files for batched processing.



---

## Installation



The official repository recommends installation in a fresh Python environment. It documents installation with:



```text

pip install boltz\[cuda] -U

```


or, for development installation from GitHub:



```text

git clone https://github.com/jwohlwend/boltz.git

cd boltz

pip install -e .\[cuda]

```

\---



For CPU-only or non-CUDA systems, the repository notes that \[cuda] should be removed, although GPU execution is expected to be much faster



## HPC Execution



Boltz-2 predictions in this study were run on an HPC environment.



The workflow consisted of two main steps:



Preparing one YAML input file for each protein-ligand complex



Running Boltz-2 predictions in batch mode using a shell script loop



This setup allowed automated execution across the benchmark dataset.



---



## Input Preparation



Boltz-2 accepts YAML input files describing the biomolecules and the requested predictions. The official repository states that input\_path may refer either to a single YAML file or to a directory of YAML files for batched prediction.

In this study, one YAML file was prepared for each protein-ligand complex.



Typical organization:



```text

Boltz-2/

├── README.md

├── run\_boltz2\_loop.sh

├── yaml\_inputs/

│   ├── complex\_001.yaml

│   ├── complex\_002.yaml

│   └── ...

├── outputs/

└── logs/

```





## Prediction Command



Boltz-2 predictions were run using the command documented in the official repository:



boltz predict input\_path --use\_msa\_server



In our workflow, input\_path referred either to a single YAML file or to a directory containing multiple YAML files. The --use\_msa\_server option was used during prediction, consistent with the official inference instructions.



Batch Prediction Workflow



To process all benchmark complexes automatically, a shell script loop was used.



The batch workflow performed the following steps:



Read YAML input files prepared for each protein-ligand complex



Submit a Boltz-2 prediction for each file



Store prediction outputs in the output directory



Save logs for monitoring and troubleshooting on HPC



Example execution pattern:



for f in yaml\_inputs/\*.yaml; do

&#x20;   boltz predict "$f" --use\_msa\_server

done



If the official CLI was pointed to a directory directly, Boltz-2 could also process all YAML files in batch mode from that directory, as described in the repository documentation.



Output Interpretation



The official repository describes two main affinity-related outputs:



affinity\_pred\_value



affinity\_probability\_binary



According to the repository documentation:



affinity\_probability\_binary should be used to distinguish binders from decoys in hit discovery settings



affinity\_pred\_value is intended for comparing affinities among binders and is reported as log10(IC50), derived from IC50 values measured in μM



In this study, Boltz-2 outputs were collected and organized for downstream comparison with other binding affinity predictors used in the benchmark.



Files in this Directory



Typical contents of this folder include:









If large prediction outputs are stored externally, this repository includes only the scripts and documentation necessary to reproduce the workflow.



Reproducibility Notes



The original Boltz codebase was used without re-implementation



Predictions were executed on HPC



One YAML file was prepared for each protein-ligand complex



A shell script loop was used to automate batch inference



Large output files are not included directly in this repository unless they are small enough for GitHub storage



##  Citation



If you use Boltz-2, please cite the official Boltz publications listed in the original repository. The repository provides citation information for both Boltz-2 and Boltz-1.





