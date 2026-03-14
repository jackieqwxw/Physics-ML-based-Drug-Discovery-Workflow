@echo off
REM =========================================================
REM Yuel Prediction Script
REM
REM Study:
REM The Last Mile Problem: A Critical Assessment of
REM Physics-based and AI Tools in Virtual Screening
REM
REM Lab:
REM Kireev Lab
REM University of Missouri-Columbia
REM
REM Author: Hamza Hentabli
REM
REM Method:
REM Yuel Compound-Protein Interaction Predictor
REM https://bitbucket.org/dokhlab/yuel
REM
REM Reference:
REM Wang J., Dokholyan N. V.
REM J. Chem. Inf. Model. 2022
REM DOI: 10.1021/acs.jcim.1c01531
REM =========================================================

set DATA_FILE=data\PDB.csv
set MODEL=models\pdbbind.model

python yuel.py predict ^
--data=%DATA_FILE% ^
--compound_column=Ligand ^
--compound_type_column=CompType ^
--protein_column=Sequence ^
--affinity_column=Affinity ^
--comp_size=64 ^
--nfeat=32 ^
--prot_size=2048 ^
--model=%MODEL%

pause