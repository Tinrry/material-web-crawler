import os
from utils_formula import *

#### global variables
debug = False


### main
if debug:
    print('debug mode')
    compositions_f = 'debug-compositions.txt'
    catch_items = 'catch_items.txt'
    except_items = 'except_items.txt'
else:
    print('normal mode')
    compositions_f = 'excepts.txt'
    catch_items = 'factor_2_CIF.txt'
    except_items = 'excepts-2.txt'

if os.path.exists(catch_items):
    os.remove(catch_items)
if os.path.exists(except_items):
    os.remove(except_items)

with open(compositions_f, 'r') as f:
    lines = f.readlines()
    for line in lines:
        # split the last : into 2-parts
        line = line.rstrip('\n')  # remove newline character
        line_list = line.rsplit(':', 1)  # split the last ':' into 2 parts
        link, formula = line_list[0], line_list[1]

        reduced_formula, sorted_formula = prepare_formula(formula)
        # save_results('file-list.txt', line, link, reduced_formula)

        # expand reduced formula * 2, save the results weather it is in the file-list.txt.
        # factor = 2
        # factor_2_f = factor_formula(sorted_formula, factor)
        # save_results('file-list.txt', line, link, factor_2_f)

        # if formula have quotation marks, expansion

        
        if debug:
            print(f'link: {link}, formula: {formula}, reduced_formula: {reduced_formula}, factor_2_f: {factor_2_f}')
    
print('Done!')

"""
exception items:
case 1:
    TaVSe8I
    I Se8 Ta V
    I2Se16Ta2V2

case 2:
    Tm3Lu(Sc4Bi3)4
    Bi12Lu1Sc16Tm3
    Bi12Lu1Sc16Tm3.CIF
"""