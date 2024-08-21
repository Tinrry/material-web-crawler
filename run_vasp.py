import re
import shutil
import os
import subprocess
import sys
import time

vasp_file = 'Al8CoNi3Ru4'
# generate_dir = './cif2mprelaxset'
work_dir = os.getcwd()

gnome_file = os.path.join('./mp-vasp-2047', vasp_file)
generate_file = os.path.join('./cif2mprelaxset', vasp_file)

potentials_dir = '/data/projects/vasp/potpaw_PBE.54'        # qstation01

def unzip_gnome_zip():
    # unzip the .zip file
    if os.path.exists(gnome_file):
        return
    gnome_zip = os.path.join('./mp-vasp-2047', vasp_file + ' MPRelaxSet.zip')
    # run the command and return the process
    return subprocess.Popen(['unzip', gnome_zip, '-d', gnome_file])

def generate_POTCAR(gnome_file, potentials_dir):
    POTCAR_file = 'POTCAR'
    if os.path.exists(POTCAR_file):
        os.remove(POTCAR_file)
    with open(os.path.join(gnome_file, 'POTCAR.spec'), 'r') as spec_file:
        lines = spec_file.readlines()
        for atom in lines:
            atom = atom.strip()
            atom_potcar = os.path.join(potentials_dir, atom, 'POTCAR')
            if os.path.exists(atom_potcar):
                with open(atom_potcar, 'r') as atom_file:
                    lines = atom_file.readlines()
                    with open(POTCAR_file, 'a') as whole_file:
                        whole_file.writelines(lines)
            else:
                print(f'{atom_potcar} not found in POTCAR file')
                sys.exit(1)
        return POTCAR_file

def sync_POTCAR():
    unzip_gnome_zip()
    # if POTCAR file exists, then return
    if os.path.exists(os.path.join(generate_file, 'POTCAR')) and os.path.exists(os.path.join(gnome_file, 'POTCAR')):
        print('fine, POTCAR file already exists, run vasp directly.')
        return
    
    POTCAR_file = generate_POTCAR(gnome_file, potentials_dir)
    shutil.copy(POTCAR_file, generate_file)
    shutil.copy(POTCAR_file, gnome_file)
    os.remove(POTCAR_file)
    return
    

def run_vasp(material_file):
    # this is run on station01
    os.chdir(material_file)
    print(f'running vasp in {material_file}')
    subprocess.run(['mpirun', '-np', '4', 'vasp_std'])
    os.chdir('..')

# run vasp use sbatch 
def run_vasp_sbatch(material_file):
    # this is run on station01
    os.chdir(material_file)
    print(f'running vasp in {material_file}')
    subprocess.run(['sbatch', 'vasp_sbatch.sh'])
    os.chdir('..')


if __name__ == '__main__':
    os.chdir(work_dir)
    sync_POTCAR()
    # run_vasp(generate_file)
    run_vasp(gnome_file)

    # then compare the results
    # TODO