import re
from collections import defaultdict


#### functions
def is_in(file, formula):
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if formula in line:
                return True
        return False


def save_results(total_file, catch_file, except_file, line, link, formula):
    if is_in(total_file, formula):
        write_line = f'{link}:{formula}\n'
        with open(catch_file, 'a') as f:
            f.write(write_line)
    else:
        print(f'formula: {formula} not found in file-list.txt')
        with open(except_file, 'a') as f:
            f.write(f'{line}\n')
            

def prepare_formula(formula):
    formula_list = re.findall(r'([A-Z][a-z]*)([\d]*)', formula)
    sorted_formula = sorted(formula_list)
    formula_1 = list(map(lambda x: x[0] + (x[1] or '1' ), sorted_formula))
    reduced_formula = ''.join(formula_1)
    return reduced_formula, sorted_formula


def factor_formula(formula, factor):
    expanded_formula = ''
    expanded_formula = list(map(lambda i: i[0] + str(int(i[1] or '1') * factor), formula))
    return ''.join(expanded_formula)


def parse_formula(formula):
    # 递归解析公式中的嵌套括号
    def expand(match):
        inner_formula, multiplier = match.groups()
        multiplier = int(multiplier)
        expanded_elements = defaultdict(int)
        
        # 解析内部公式
        elements = re.findall(r'([A-Z][a-z]*)([\d]*)', inner_formula)
        for element, count in elements:
            count = int(count) if count else 1
            expanded_elements[element] += count * multiplier
        
        return expanded_elements

    # 递归展开公式
    def recursive_expand(formula):
        while '(' in formula:
            # 将同一层级的括号展开
            formula = re.sub(r'\(([^()]+)\)(\d+)', lambda m: ''.join(f'{k}{v}' for k, v in expand(m).items()), formula)
        return formula

    # 初步展开公式
    expanded_formula = recursive_expand(formula)
    
    # 最终合并所有元素
    final_elements = defaultdict(int)
    elements = re.findall(r'([A-Z][a-z]*)([\d]*)', expanded_formula)
    for element, count in elements:
        count = int(count) if count else 1
        final_elements[element] += count

    # 生成等价的字符串
    result_formula = ''.join(f'{element}{count}' for element, count in final_elements.items())
    return result_formula


### test
formula = "(Sc4Bi3)4"
expanded_formula = parse_formula(formula)
assert expanded_formula == 'Sc16Bi12', 'Test failed!'
print('Test passed!')

formula = "Sc4Bi3"
expanded_formula = parse_formula(formula)
assert expanded_formula == 'Sc4Bi3', 'Test failed!'
print('Test passed!')

formula = "(Sc4Bi3)4(Sc4Bi3)4"
expanded_formula = parse_formula(formula)
assert expanded_formula == 'Sc32Bi24', 'Test failed!'
print('Test passed!')

formula = "(Sc4Bi3(P4Ci3)2)4(Sc4Bi3)4" 
expanded_formula = parse_formula(formula)
assert expanded_formula == 'Sc32Bi24P32Ci24', 'Test failed!'
print('Test passed!')


