
import pybel
import os
import pandas as pd


def convert_sdf_to_mol2(input_sdf, output_dir):
    molecules = list(pybel.readfile("sdf", input_sdf))
    
    for i, mol in enumerate(molecules):
        # Define the output file name
        output_file = os.path.join(output_dir, f"molecule_{i+1}.mol2")
        mol.write("mol2", output_file, overwrite=True)
        
        print(f"Converted molecule {i+1} to {output_file}")



path = 'dataset/'

data = pd.read_csv(path+ 'index.csv') 
i = 0
for index, row in data.iterrows():
    
    rec_fpath =path+  row['proteinpath'][2:]
    lig_fpath =path+  row['ligandpath'][2:]
    
    pdb_file =lig_fpath[:-4]+ '.mol2'
    
    convert_sdf_to_mol2(lig_fpath, pdb_file)




# Example usage
input_sdf = "multi_molecule.sdf"  # Path to your input SDF file
output_dir = "output_mol2_files"  # Directory to save the output MOL2 files

convert_sdf_to_mol2(input_sdf, output_dir)