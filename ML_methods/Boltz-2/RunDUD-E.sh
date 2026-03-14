# =========================================================
# Boltz-2 Batch Prediction Script
#
# Developed for benchmarking machine learning scoring
# functions in virtual screening.
#
# Study:
# The Last Mile Problem: A Critical Assessment of
# Physics-based and AI Tools in Virtual Screening
#
# Lab:
# Kireev Lab
# University of Missouri-Columbia
#
# Author: Hamza Hentabli
#
# Method:
# Boltz-2 biomolecular interaction model
# https://github.com/jwohlwend/boltz
#
# Reference:
# Wohlwend J., et al.
# Boltz-2: A Biomolecular Foundation Model for Interaction
# Prediction and Binding Affinity Estimation
#
# =========================================================

#!/bin/bash
#SBATCH --job-name=boltz_gpu
#SBATCH --account=dkhf3-lab
#SBATCH --partition=dkhf3-lab-gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=boltz_%j.out
#SBATCH --error=boltz_%j.err

set -e

module purge
module load cuda

nvidia-smi

DATA_DIR="DUD-E"
TOTAL=315
COUNT=0

for yaml in ${DATA_DIR}/*.yaml; do
    COUNT=$((COUNT+1))
    echo "Running ${COUNT}/${TOTAL}: ${yaml}"

    boltz predict "${yaml}" --use_msa_server

done

echo "All jobs completed. Total processed: ${COUNT}/${TOTAL}"
