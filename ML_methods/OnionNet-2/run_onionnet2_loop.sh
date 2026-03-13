#!/bin/bash

# ==========================================
# OnionNet-2 batch prediction script
# ==========================================

# Base dataset path
DATASET_PATH="PDB"

# index file
INDEX_FILE="$DATASET_PATH/index.csv"

# Model files (update paths if needed)
SCALER_FPATH="model/train_scaler.scaler"
MODEL_FPATH="model/62shell_saved-model.h5"

OUTPUT_CSV="onionnet2_predictions.csv"

echo "Preparing output file..."

# create header
head -n 1 "$INDEX_FILE" > $OUTPUT_CSV
sed -i '1s/$/,prediction/' $OUTPUT_CSV

# read csv skipping header
tail -n +2 "$INDEX_FILE" | while IFS=',' read -r proteinpath ligandpath rest
do

    rec_fpath="$DATASET_PATH/${proteinpath:2}"
    lig_fpath="$DATASET_PATH/${ligandpath:2}"

    tmp_out="tmp_prediction.txt"

    python predict.py \
        -rec_fpath "$rec_fpath" \
        -lig_fpath "$lig_fpath" \
        -shape 84,124,1 \
        -scaler "$SCALER_FPATH" \
        -model "$MODEL_FPATH" \
        -shells 62 \
        -out_fpath "$tmp_out"

    # extract prediction value
    pred_pKa=$(cat $tmp_out | tail -n 1)

    echo "${proteinpath},${ligandpath},${pred_pKa}" >> $OUTPUT_CSV

done

echo "Finished. Results saved in $OUTPUT_CSV"