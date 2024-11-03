#!/bin/bash

# Directory containing CIF files
cif_directory="/path-to-cif" # Update this path
output_directory="${cif_directory}/smiles_files"

# Create output directory if it doesn't exist
mkdir -p "$output_directory"

# Convert each CIF file to SMILES
for cif_file in "$cif_directory"/*.cif; do
    # Extract filename without extension
    filename=$(basename "$cif_file" .cif)
    # Convert to SMILES
    obabel "$cif_file" -O "$output_directory/$filename.smiles"
done

echo "CIF to SMILES conversion completed."
