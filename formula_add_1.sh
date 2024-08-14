#!/bin/bash

# 输入字符串
input="Cs6TbErBr12"

# 使用grep和sed提取元素和数字
elements=$(echo "$input" | grep -oE '[A-Z][a-z]*[0-9]*' | sed 's/\([A-Z][a-z]*\)\([0-9]*\)/\1 \2/' | awk '{if ($2 == "") $2 = 1; print $1 $2}')

# 将结果合并成一行，并输出结果
elements=$(echo "$elements" | tr -d '\n')
echo "$elements"