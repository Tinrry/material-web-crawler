import pandas as pd
def get_composition(reduced_f='Cs(ZrS2)3', csv_file='stable_materials_summary.csv'):
    reduced_f = reduced_f.strip()
    # get the composition of the reduced formula from the csv file
    with open(csv_file, 'r') as file:
        df = pd.read_csv(file, header=0)
        if reduced_f in df['Reduced Formula'].values:
            composition = df.loc[df['Reduced Formula'] == reduced_f].values[0][1]
            print(f'reduced_f: {reduced_f}, composition: {composition}')
            return composition
        else:
            print(f'reduced_f: {reduced_f} not found in the csv file')
            return None

def get_formula(c_item='Nd7Os1Pr3Si5', csv_file='stable_materials_summary.csv'):
    c_item = c_item.strip()
    df = pd.read_csv(csv_file, header=0)
    if c_item in df['Composition'].values:
        reduced_f = df.loc[df['Composition'] == c_item].values[0][3]
        print(f'c_item: {c_item}, reduced_f: {reduced_f}')
        return reduced_f
    else:
        print(f'c_item: {c_item} not found in the csv file')
        return None

def is_in_txt(reduced_f, downloaded_file):
    with open(downloaded_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if reduced_f == line:
                return True
        return False
        
def func():
    # 这里面的化学式是Reduced Formula
    with open('compositions.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            url, reduced_f = line.rsplit(':', 1)

            
            if is_in_txt(reduced_f, downloaded_file):
                print(f"Reduced formula is in downloaded input.txt: {reduced_f}")
            else:
                print(f"Reduced formula is not in downloaded input.txt: {reduced_f}")
                # this url are not download, so add to subset.txt
                with open('subset.txt', 'a') as file:
                    file.write(f"{url}\n")

        
downloaded_file = 'input.txt'
csv_file = 'stable_materials_summary.csv'

if __name__ == '__main__':
    func()
