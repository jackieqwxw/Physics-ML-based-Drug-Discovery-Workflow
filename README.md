# Physics-ML-based-Drug-Discovery-Workflow

## Software Environment
Tested on:
- AMBER 22
- Schrödinger 2024-2
- GROMACS 2022
- gmx_MMPBSA v1.6.x
- Gaussian 16
- Open Babel
- SLURM-based HPC environment

## Required User Inputs
- Ligand structures (SDF)
- Protein structure (PDB)

## Provided by This Repository
- Parameterization scripts
- MD input templates
- MM/PB(GB)SA workflows
- FEP setup and analysis scripts

## Quick Start (Minimal Example)
1. Prepare ligand SDF and protein PDB
2. Run ligand parameterization:
   cd LigPara && sbatch LigPara.sh ligands.sdf 0
3. Compute free energies using MM/PB(GB)SA:
   cd MMPBSA && sbatch gmxmmpbsa.sh
4. Compute free energies using FEP:
   cd FEP && sbatch FEP.sh

## Common Pitfalls
- Ensure ligands with different net charges are separated into different SDF files
- Separate complexes with and without ions
- Check periodic boundary conditions before MM/PB(GB)SA
- Ensure consistent atom naming between topology and trajectory
