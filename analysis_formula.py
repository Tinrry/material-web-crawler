import os
import re

if os.path.exists('factor_2_CIF.txt'):
    os.remove('factor_2_CIF.txt')

with open('excepts.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # split the last : into 2-parts
        line = line.rstrip('\n')  # remove newline character
        line_list = line.rsplit(':', 1)  # split the last ':' into 2 parts
        link, formula = line_list[0], line_list[1]

        formula_list = re.findall(r'([A-Z]+[a-z*])([\d]*)', formula)
        sorted_formula = sorted(formula_list)
        formula_1 = list(map(lambda x: x[0] + (x[1] or '1' ), sorted_formula))
        reduced_formula = ''.join(formula_1)

        # expand reduced formula * 2
        factor = 2
        expanded_formula = ''
        expanded_formula = list(map(lambda i: i[0] + str(int(i[1] or '1') * factor), sorted_formula))
        factor_2_f = ''.join(expanded_formula)

        # find the factor_2_f in the file-list.txt
        with open('file-list.txt', 'r') as f:
            file_lines = f.readlines()
            for file_line in file_lines:
                if factor_2_f in file_line:
                    # got it
                    # print(f'factor_2_f: {factor_2_f} found in file_line: {file_line}')
                    write_line = f'{link}:{factor_2_f}\n'
                    with open('factor_2_CIF.txt', 'a') as f:
                        f.write(write_line)
                    break
            else:
                # not found
                print(f'factor_2_f: {factor_2_f} not found in file-list.txt')
                with open('excepts-2.txt', 'a') as f:
                    f.write(f'{line}\n')
    
print('Done!')

""" exception example
AlO6TcYb2 this should match Al2O12Tc2Yb4
"""
