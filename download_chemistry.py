import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from download_gnome_files import login


# get periodic table
periodic_table = [
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
    'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
    'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
    'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
    'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
    'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr',
    'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
]

base_href = 'https://next-gen.materialsproject.org/materials?formula=Bi' # 2 个链接
mp_href = 'https://next-gen.materialsproject.org/materials/mp-568348?formula=P'   # 1 个链接  


def find_zero_energy_href(driver, chemistry):
    base_href = 'https://next-gen.materialsproject.org/materials?formula=' + chemistry

    mp_href = []
    driver.get(base_href)
    time.sleep(10)

    row = -1
    while True:
        row += 1
        try:
            elements = driver.find_elements(By.ID, f'row-{row}')            # error will happen Ne just one row with 0 energy. dont worry.
            energy = elements[0].find_elements(By.XPATH, 'div')[6].text
        except Exception as e:
            print(f'Error: {e}')
            return mp_href
        
        if energy == '0':
            # extended_href = elements[0].find_elements(By.XPATH, 'div')[1].get_attribute('a href')
            extended_href = elements[0].find_elements(By.XPATH, 'div')[1].find_elements(By.XPATH, 'a')[0].get_attribute('href')
            # print(f'extended_href {extended_href}')
            mp_href.append(extended_href)
        else:
            print(f'energy {energy} break.')
            break
    return mp_href

import os


if __name__ == "__main__":

    driver = webdriver.Firefox()
    login(driver)

    # if os.path.exists('chemistry_href.txt'):
    #     os.remove('chemistry_href.txt')
    for chemistry in periodic_table[8:]:
        mp_href = find_zero_energy_href(driver, chemistry)
        # write mp_href to txt file
        with open('chemistry_href.txt', 'a') as file:
            for href in mp_href:
                file.write(f'{href}\n')
    driver.close()
