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

def write_match_results(file, link, formula):
    write_line = f'{link}:{formula}\n'
    with open(file, 'a') as f:
        f.write(write_line)


def write_except_results(file, line):
    with open(file, 'a') as f:
        f.write(f'{line}\n')
            

def factor_formula(formula, factor):
    expanded_elements = defaultdict(int)
    elements = re.findall(r'([A-Z][a-z]*)([\d]*)', formula)
    elements = sorted(elements, key=lambda x: x[0])
    for element, count in elements:
        count = int(count) if count else 1
        expanded_elements[element] = count * factor
    return ''.join(f'{element}{count}' for element, count in expanded_elements.items())

   
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
    elements = sorted(elements, key=lambda x: x[0])
    for element, count in elements:
        count = int(count) if count else 1
        final_elements[element] += count

    # 生成等价的字符串
    result_formula = ''.join(f'{element}{count}' for element, count in final_elements.items())
    return result_formula


### test
def test_parse_formula():
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
