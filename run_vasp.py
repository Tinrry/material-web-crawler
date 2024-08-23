import re
import shutil
import os
import subprocess
import sys
import time

def get_file_list():
    with open('compositions.txt', 'r') as f:
        vasp_files = []
        lines = f.readlines()
        for line in lines[:10]:
            _, reduced_f = line.rsplit(':', 1)
            vasp_files.append(reduced_f.strip())
        return vasp_files
    

def unzip_gnome_zip(vasp_files):
    for vasp_file in vasp_files:
        gnome_file = os.path.join('./mp-vasp-2047', vasp_file)
        gnome_zip = os.path.join('./mp-vasp-2047', vasp_file + ' MPRelaxSet.zip')
        if os.path.exists(gnome_file):
            continue
        print(f'unzip {gnome_zip} to {gnome_file}')
        # run the command and return the process
        subprocess.Popen(['unzip', gnome_zip, '-d', gnome_file])
    return

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

def sync_POTCAR(potentials_dir):
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
    os.chdir(work_dir)

# run vasp use sbatch 
# TODO 
# if I run in qlab200 , I need rsync input files from qstation01, and implement a for loop to run all the materials.
def run_vasp_sbatch(material_file):
    # this is run on station01
    os.chdir(material_file)
    # check if the OUTCAR file is run completely
    if os.path.exists('OUTCAR'):
        # if that file exists, then return
        with open('OUTCAR', 'r') as f:
            lines = f.readlines()
            if 'Voluntary context switches' in lines[-1]:
                print(f'{material_file} already run, skip')
                return
            else:
                print(f'{material_file} not run completely, rerun')

    print(f'running vasp in {material_file}')
    subprocess.run([f'ln -sf /online/home/hhzheng/material-web-crawler/vasp_sbatch.sh vasp_sbatch.sh'], shell=True)
    subprocess.run(['sbatch', 'vasp_sbatch.sh'])
    os.chdir(work_dir)


def compare_results():
    # then compare the results, this is consult to ZHANG JINGTONG
    # CHECK OK
    return True


# ==== global variables ====
potentials_dir_qstation01 = '/data/projects/vasp/potpaw_PBE.54'        # qstation01
potentials_dir_qlab200 = '/online/home/hhzheng/vasp/potpaw_PBE.54'  # qlab200
work_dir = os.getcwd()              


if __name__ == '__main__':
    vasp_files = get_file_list()
    unzip_gnome_zip(vasp_files)
    for vasp_file in vasp_files[:10]:
        os.chdir(work_dir)
        gnome_file = os.path.join(work_dir, 'mp-vasp-2047', vasp_file)
        generate_file = os.path.join(work_dir, 'cif2mprelaxset', vasp_file)
        sync_POTCAR(potentials_dir=potentials_dir_qlab200)

        run_vasp_sbatch(generate_file)
        run_vasp_sbatch(gnome_file)
        time.sleep(2)
