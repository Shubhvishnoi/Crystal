####################################################################
# Script to extract the details of number of atoms per unit cell.
# Github: https://github.com/Shubhvishnoi
# Date: 20/01/2024
####################################################################

import os
import csv
from pymatgen.io.cif import CifParser

def get_atoms_per_unit_cell(cif_file_path):
    parser = CifParser(cif_file_path)
    structure = parser.get_structures()[0]
    num_atoms = len(structure)
    return num_atoms

def process_cif_files(directory):
    # Get a list of all CIF files in the directory
    cif_files = [file for file in os.listdir(directory) if file.endswith(".cif")]

    output_csv_path = 'output.csv'
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Crystal', 'Number_of_atoms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for cif_file in cif_files:
            cif_file_path = os.path.join(directory, cif_file)
            num_atoms = get_atoms_per_unit_cell(cif_file_path)
            
            crystal_name = os.path.splitext(cif_file)[0]
            writer.writerow({'Crystal': crystal_name, 'Number_of_atoms': num_atoms})

    print(f"Results written to {output_csv_path}")

cif_directory = 'CIF_files'
process_cif_files(cif_directory)
