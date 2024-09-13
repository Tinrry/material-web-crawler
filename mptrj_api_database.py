import json


def process_item(item):

    subset_data = {
        "lattice": item.get("structure").get("lattice").get("matrix"),
        "atoms": [site.get("label") for site in item.get("structure").get("sites")],
        "positions": [site.get("xyz") for site in item.get("structure").get("sites")],
        "spin": "not available",
        "pseudopotentials": "not available",
        "calculation": "not available",
        "energy": item.get("corrected_total_energy"),
        "forces": item.get("force"),
        "stress": item.get("stress"),
    }
    return subset_data


def read_large_jsonl(file_path):
    processed_data = []
    with open(file_path, 'r') as f:
        for line in f:
            item = json.loads(line.strip())
            processed_item = process_item(item)
            processed_data.append(processed_item)
            if len(processed_data) == 10:
                # write to database
                with open(save_path, 'a') as f:
                    for item in processed_data:
                        f.write(json.dumps(item) + '\n')
                processed_data = []

    return processed_data

import os
# 示例文件路径
traj_file = "MPtrj_2022.9_full-processed.jsonl"
save_path = "MPtrj_2022.9_api.jsonl"
# if os.path.exists(save_path):
#     os.remove(save_path)      # too dangerous
processed_data = read_large_jsonl(traj_file)
