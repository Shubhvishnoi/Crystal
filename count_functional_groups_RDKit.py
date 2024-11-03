#########################################################################################################
# This code, generously shared by Actuate Lab, is freely available for use, modification, and sharing   #
# under the GNU General Public License. It serves as open-access code for extracting data from CIFs     #
# (input - SMILES notation) and provide output in a CSV file. Contributions to enhance and expand the   #
# codebase are encouraged.                                                                              #
#                                                                                                       #
#               ------------------------------------------------------------------------                #
# GitHub Profile: https://github.com/Shubhvishnoi                                                       #
# S. Vishnoi, Postdoctoral Fellow, Department of Physics, University of Limerick | Date: 11/01/2024.    #
#########################################################################################################



import os
import pandas as pd
from rdkit import Chem

# Define the path to the directory containing SMILES files
smiles_directory = "/path-to-cif/smiles_files"  # Update this path
output_csv_file = "functional_group_counts_rdkit.csv"

# Define functional group SMARTS patterns #Make any required correction. Just a few functional group examples, not regioursly tested.
functional_group_smarts = {
    'Hydroxyl': 'C(O)',                      # Alcohol
    'Aldehyde': 'C=O',                       # Aldehyde
    'Ketone': 'C(=O)C',                      # Ketone
    'Carboxylic Acid': 'C(=O)O',             # Carboxylic acid
    'Amino': 'N',                            # Amino group
    'Amide': 'C(=O)N',                       # Amide group
    'Ester': 'C(=O)O',                       # Ester group
    'Nitrile': 'C#N',                        # Nitrile
    'Alkane': '[C;!R]',                      # Alkanes
    'Alkene': 'C=C',                         # Alkenes
    'Alkyne': 'C#C',                         # Alkynes
    'Ether': 'C-O-C',                        # Ether
    'Cycloalkane': 'C1CCCCC1',               # Cyclohexane
    'Cycloalkene': 'C1=CC=CC=C1',            # Cyclohexene
    'Aromatic Ring': 'c1ccccc1',             # Benzene
    'Furan': 'O=C1C=CC=C1',                  # Furan
    'Pyridine': 'c1ccncc1',                  # Pyridine
    'Pyrrole': 'C1=CNC=C1',                  # Pyrrole
}

# Initialize a list to store results
results = []

# Loop through all SMILES files in the directory
for filename in os.listdir(smiles_directory):
    if filename.endswith('.smiles'):
        file_path = os.path.join(smiles_directory, filename)
        try:
            with open(file_path, 'r') as file:
                smiles = file.readline().strip()  # Read the first line for SMILES representation
                
                # Check if the SMILES string is empty
                if not smiles:
                    print(f"Warning: Empty SMILES string in file: {filename}")
                    continue
                
                # Convert SMILES to RDKit molecule
                mol = Chem.MolFromSmiles(smiles)
                
                if mol is None:
                    print(f"Could not convert SMILES to molecule for file: {filename}. Invalid SMILES: '{smiles}'")
                    continue

                # Initialize counts for each functional group
                counts = {'Filename': filename}
                for group_name, smarts in functional_group_smarts.items():
                    pattern = Chem.MolFromSmarts(smarts)
                    if pattern is None:
                        print(f"Could not convert SMARTS for group: {group_name}")
                        continue
                    # Count occurrences of the functional group
                    count = len(mol.GetSubstructMatches(pattern))
                    counts[group_name] = count

                # Append counts to results
                results.append(counts)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Convert results to a DataFrame
df = pd.DataFrame(results)

# Save results to a CSV file
df.to_csv(output_csv_file, index=False)
print(f"Functional group counts saved to {output_csv_file}")
