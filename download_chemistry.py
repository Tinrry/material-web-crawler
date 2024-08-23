import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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

base_href = 'https://next-gen.materialsproject.org/materials?formula=P'
mp_href = 'https://next-gen.materialsproject.org/materials/mp-568348?formula=P'

# TODO 同一个元素，可能有很多个能量为0的结构
def find_zero_energy_href(driver, chemistry):
    base_href = 'https://next-gen.materialsproject.org/materials?formula=' + chemistry

    mp_href = None
    driver.get(base_href)
    time.sleep(10)
    elements = driver.find_elements(By.ID, 'row-0')
    energy = elements[0].find_elements(By.XPATH, 'div')[6].text
    print(f'energy {energy}')
    if int(energy) == 0:
        # extended_href = elements[0].find_elements(By.XPATH, 'div')[1].get_attribute('a href')
        extended_href = elements[0].find_elements(By.XPATH, 'div')[1].find_elements(By.XPATH, 'a')[0].get_attribute('href')
        print(f'extended_href {extended_href}')
    return extended_href

from download_gnome_files import login

if __name__ == "__main__":
    driver = webdriver.Firefox()
    login(driver)
    mp_href = find_zero_energy_href(driver, 'P')
    driver.close()
