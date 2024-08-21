import re
import shutil
import os
import subprocess
import sys
import time

vasp_file = 'Al8CoNi3Ru4'
gnome_dir = './mp-vasp-2047'
generate_dir = './cif2mprelaxset'

potentials_dir = '/data/projects/vasp/potpaw_PBE.54'        # qstation01
POTCAR_file = 'POTCAR'

gnome_zip = os.path.join(gnome_dir, vasp_file, ' MPRelaxSet.zip')
gnome_file = os.path.join(gnome_dir, vasp_file)
subprocess.Popen(['unzip', gnome_zip, '-d', gnome_file])

with open(os.path.join(gnome_file, 'POTCAR.spec'), 'r') as spec_file:
    lines = spec_file.readlines()
    for atom in lines:
        atom = atom.strip()
        potcar_file = os.path.join(potentials_dir, atom, 'POTCAR')
        with open(potcar_file, 'r') as atom_file:
            lines = atom_file.readlines()
            with open(POTCAR_file, 'a') as whole_file:
                whole_file.writelines(lines)
    else:
        print('PAW_PBE not found in POTCAR file')
        sys.exit(1)
