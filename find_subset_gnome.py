def get_composition(reduced_f='Cs(ZrS2)3', csv_file='stable_materials_summary.csv'):
    # get the composition of the reduced formula from the csv file
    import pandas as pd
    with open(csv_file, 'r') as file:
        df = pd.read_csv(file, header=0)
        df.head()
        if reduced_f in df['Reduced Formula'].values:
            composition = df.loc[df['Reduced Formula'] == reduced_f].values[0][1]
            print(f'reduced_f: {reduced_f}, composition: {composition}')
            return composition



def func():
    with open('input.txt', 'r') as file:
        formulates = file.readlines()
        for reduced_f in formulates:
            print(reduced_f)
            composition = get_composition(reduced_f, csv_file)


csv_file = 'stable_materials_summary.csv'

if __name__ == '__main__':
    get_composition()