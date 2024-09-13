from find_subset_gnome import get_composition
import os
import subprocess

subset_dir = 'by_composition_2047'
if not os.path.exists(subset_dir):
    os.makedirs(subset_dir)


# get subset CIF from by_composition directory using index in compositions.txt
with open('compositions.txt') as f:
    lines = f.readlines()
    for line in lines:
        _, reduced_f = line.rsplit(':', 1)
        # get the composition from the reduced formula
        composition = get_composition(reduced_f, csv_file='stable_materials_summary.csv')
        if composition is not None:
            cif_file = f'./by_composition/{composition}.CIF'
            if os.path.exists(cif_file):
                subprocess.run(['cp', cif_file, subset_dir])
            else:
                print(f'No CIF found in by_composition folder.')
        else:
            print(f'No composition found for {reduced_f}')
            continue
