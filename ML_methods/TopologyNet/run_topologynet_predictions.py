import os
import csv
from inference import predict
from sdf2mol2 import convert_sdf_to_mol2

# =========================================================
# TopologyNet Batch Prediction Script
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
# TopologyNet
# https://github.com/longyuxi/TopologyNet-2017
# =========================================================


def find_pairs(data_dir: str):
    """
    Find protein-ligand pairs in a folder.

    Expected naming:
    <base>_protein.pdb
    <base>_ligand.sdf
    """
    pairs = []

    for fname in os.listdir(data_dir):
        if fname.endswith("_protein.pdb"):
            base = fname[:-len("_protein.pdb")]
            protein_file = os.path.join(data_dir, fname)
            ligand_sdf = os.path.join(data_dir, f"{base}_ligand.sdf")

            if os.path.exists(ligand_sdf):
                pairs.append((base, protein_file, ligand_sdf))
            else:
                print(f"[SKIP] Missing ligand SDF for {base}: {ligand_sdf}")

    return sorted(pairs)


def get_expected_mol2_path(output_dir: str, sdf_path: str) -> str:
    """
    Guess the MOL2 filename produced by convert_sdf_to_mol2().
    Assumes the MOL2 file keeps the same stem as the input SDF.
    """
    stem = os.path.splitext(os.path.basename(sdf_path))[0]
    return os.path.join(output_dir, f"{stem}.mol2")


def run_predictions(data_dir: str, mol2_dir: str, output_csv: str):
    pairs = find_pairs(data_dir)

    if not pairs:
        print(f"No valid protein-ligand pairs found in: {data_dir}")
        return

    os.makedirs(mol2_dir, exist_ok=True)
    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "base_name",
            "protein_file",
            "ligand_sdf",
            "ligand_mol2",
            "prediction_pKd",
            "prediction_delta_G_kcal_mol",
            "time_taken_s",
            "status"
        ])

        for i, (base, protein_file, ligand_sdf) in enumerate(pairs, start=1):
            print(f"[{i}/{len(pairs)}] Processing {base}")

            try:
                # Convert SDF to MOL2
                convert_sdf_to_mol2(ligand_sdf, mol2_dir)

                ligand_mol2 = get_expected_mol2_path(mol2_dir, ligand_sdf)

                if not os.path.exists(ligand_mol2):
                    raise FileNotFoundError(
                        f"MOL2 file was not created as expected: {ligand_mol2}"
                    )

                # Run TopologyNet prediction
                result = predict(protein_file, ligand_mol2)

                writer.writerow([
                    base,
                    protein_file,
                    ligand_sdf,
                    ligand_mol2,
                    result.get("prediction (pKd, ??)", ""),
                    result.get("prediction (delta_G, kcal/mol)", ""),
                    result.get("time_taken (s)", ""),
                    "OK"
                ])

            except Exception as e:
                print(f"[ERROR] Failed on {base}: {e}")
                writer.writerow([
                    base,
                    protein_file,
                    ligand_sdf,
                    "",
                    "",
                    "",
                    "",
                    f"ERROR: {e}"
                ])

    print(f"Done. Results saved to: {output_csv}")


if __name__ == "__main__":
    DATA_DIR = "PDB_database"
    MOL2_DIR = "generated_mol2"
    OUTPUT_CSV = "outputs/topologynet_predictions.csv"

    run_predictions(DATA_DIR, MOL2_DIR, OUTPUT_CSV)