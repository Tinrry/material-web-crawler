#!/bin/bash

# 输入字符串
input_file="debug-compositions.txt"
rm -f compositions-CIF.txt excepts.txt

while IFS= read -r line; do
    # 提取链接
    link=$(echo "$line" | awk -F':' '{print $1 ":" $2}')

    # 提取化学式
    formula=$(echo "$line" | awk -F':' '{print $3}')

    # 使用grep和sed提取元素和数字
    elements=$(echo "$formula" | grep -oE '[A-Z][a-z]*[0-9]*' | sed 's/\([A-Z][a-z]*\)\([0-9]*\)/\1 \2/' | awk '{if ($2 == "") $2 = 1; print $1 $2}')

    # 将结果合并成一行，并输出结果
    elements=$(echo "$elements" | sort | tr -d '\n')

    # 判断elements是否在file-list.txt中
    if grep -q "$elements" file-list.txt; then
        # 将结果写入文件
        echo $link":"$elements >> compositions-CIF.txt
    else
        echo "The formula $elements is not in file-list.txt"
        echo $line >> excepts.txt
    fi

done < "$input_file"
