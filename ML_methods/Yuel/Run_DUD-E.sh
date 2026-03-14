#!/bin/bash
# =========================================================
# Yuel Prediction Script
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
# Yuel: Structure-free compound–protein interaction predictor
# https://bitbucket.org/dokhlab/yuel
#
# Reference:
# Wang J., Dokholyan N. V.
# Yuel: Improving the Generalizability of Structure-Free
# Compound–Protein Interaction Prediction.
# J. Chem. Inf. Model. 2022.
# DOI: 10.1021/acs.jcim.1c01531
# =========================================================

DATA_FILE=data/DUD-E.csv
MODEL=models/pdbbind.model

python yuel.py predict \
--data=$DATA_FILE \
--compound_column=Ligand \
--compound_type_column=CompType \
--protein_column=Sequence \
--affinity_column=Affinity \
--comp_size=64 \
--nfeat=32 \
--prot_size=2048 \
--model=$MODEL