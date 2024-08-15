import os
from utils_formula import *

#### global variables
debug = False

### main
if debug:
    print('debug mode')
    compositions_f = 'debug-compositions.txt'
else:
    print('normal mode')
    compositions_f = 'excepts.txt'

catch_file = 'catch_items.txt'
except_file = 'except_items.txt'

if os.path.exists(catch_file):
    os.remove(catch_file)
if os.path.exists(except_file):
    os.remove(except_file)

with open(compositions_f, 'r') as f:
    lines = f.readlines()
    for line in lines:
        # split the last : into 2-parts
        line = line.rstrip('\n')  # remove newline character
        line_list = line.rsplit(':', 1)  # split the last ':' into 2 parts
        link, formula = line_list[0], line_list[1]

        expanded_formula = parse_formula(formula)
        if is_in('file-list.txt', expanded_formula):
            write_match_results(catch_file, link, expanded_formula)
        else:
            
            factor = 2
            factor_2_f = factor_formula(expanded_formula, factor)
            if is_in('file-list.txt', factor_2_f):
                write_match_results(catch_file, link, factor_2_f)
            else:
                print('Parse formula not found:', expanded_formula)
                print('     Formula * 2 not found:', factor_2_f)
                write_except_results(except_file, line)
    
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

case 3:
    Ba6Lu2(WO6)3
    Ba6 Lu2 O18 W3
"""
