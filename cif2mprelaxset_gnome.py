from pymatgen.io.cif import CifParser
from pymatgen.io.vasp.sets import MPRelaxSet
from pymatgen.core.structure import Structure
from find_subset_gnome import get_composition


# read the reduced_formula from the compositions.txt
with open('compositions.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        _, reduced_f = line.rsplit(':', 1)
        # get the composition from the reduced formula
        composition = get_composition(reduced_f, csv_file='stable_materials_summary.csv')
        if composition is not None:
            cif_file = f'./by_composition/{reduced_f}.CIF'
            parser = CifParser(cif_file)
            # write the structure to the cif file
            structure = parser.get_structures(primitive=False)[0]
            # create the MPRelaxSet
            mpr = MPRelaxSet(structure, user_incar_settings={'ISIF': 3})
            # write the MPRelaxSet to the directory
            mpr.write_input('cif2mprelaxset', potcar_spec=True)
        else:
            print(f"composition is None for reduced_f: {reduced_f}")
        break