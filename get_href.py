import os,re
import pandas as pd

def get_group_href(save_path, file_name):
    """
    attention to get link from file_name and save to save_file

    :param save_path: file_name = 'hand/Water-Hardening Steel-25-1.mht'
    :param file_name: save_file = 'get_link/Water-Hardening Steel-25-1.csv'
    :return:
    """

    save_file = os.path.join(save_path, os.path.basename(file_name).split('.')[0] + '.csv')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    with open(file_name, 'r') as f:
        text = f.read()
        text = text.replace('=\n', '')
        href_list = re.findall(r'href=3D"(.*MatGUID.*)"', text)

        defuse_str = '3D'
        href_list = [i.replace(defuse_str, '') for i in href_list]
        print(href_list[0])

        title_list = re.findall(r'href=3D.*MatGUID.*>(.*?)</a>', text)
        if len(title_list) != len(href_list):
            print('wrong')
        else:
            data = {'href': href_list, 'title': title_list}
            data_frame = pd.DataFrame(data)
            data_frame.to_csv(save_file, index=False)
    return

if __name__ == '__main__':
    """
    hand is the folder that you want to get link from
    """
    for _, _, files in os.walk('hand'):
        for file in files:
            get_group_href('get_link', 'hand/' + file)
