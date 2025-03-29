import pandas as pd

# df = pd.DataFrame(data)
# df.to_csv('Students_Grading_Dataset.csv', index=False)

def processar_dados():
    try:
        dados = pd.read_csv('Students_Grading_Dataset.csv')

    except FileNotFoundError:
        print("Erro: Arquivo 'Students_Grading_Dataset.csv' não encontrado.")

processar_dados()