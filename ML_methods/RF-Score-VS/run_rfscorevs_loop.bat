REM =========================================================
REM RF-Score-VS Batch Prediction Script
REM
REM Developed for benchmarking machine learning scoring
REM functions in virtual screening.
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
REM RF-Score-VS Reference:
REM Wójcikowski M., Ballester P.J., Siedlecki P.
REM Performance of machine-learning scoring functions in
REM structure-based virtual screening.
REM Scientific Reports, 7, 46710 (2017)
REM DOI: 10.1038/srep46710
REM =========================================================


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

        REM Check output CSV does NOT exist
        if not exist "!OUT_FILE!" (
            echo Running RF-Score-VS for !BASE!
            rf-score-vs.exe --receptor "%%P" "!LIG_FILE!" -o csv -O "!OUT_FILE!"
        ) else (
            echo [SKIP] CSV exists for !BASE!
        )

    ) else (
        echo [SKIP] Missing ligand for !BASE!
    )
)

echo Done.
pause
