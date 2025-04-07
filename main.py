import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Função para carregar o arquivo
def carregar_arquivo():
    caminho = input("Digite o caminho do arquivo .csv ou .json: ")

    # Verificando se o arquivo existe e retornando os dados
    try:
        if caminho.endswith('.csv'):
            return pd.read_csv('Students_Grading_Dataset.csv')
        elif caminho.endswith('.json'):
            return pd.read_json('Students_Grading_Dataset.json')
        else:
            print("Formato de arquivo inválido! Só aceitamos CSV ou JSON.")
            return None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None

def exibir_resumo_estatistico(df):
    print("\nResumo estatístico:")
    print(df.describe())

    # Quantidade de dados carregados
    print(f"\nQuantidade de dados carregados: {df.shape[0]}")

    # Quantidade de homens e mulheres
    if 'Gender' in df.columns:
        print(f"\nQuantidade de homens e mulheres:")
        print(df['Gender'].value_counts())
    else:
        print("\nColuna 'Gender' não encontrada no dataset.")

    # Registros sem dados sobre a educação dos pais
    if 'Parent_Education_Level' in df.columns:
        registros_sem_educacao_pais = df['Parent_Education_Level'].isna().sum()
        print(f"\nQuantidade de registros sem dados sobre a educação dos pais: {registros_sem_educacao_pais}")
    else:
        print("\nColuna 'Parent_Education_Level' não encontrada no dataset.")

# Função para limpar os dados
def limpar_dados(df):
    # Remover registros com a educação dos pais vazia
    if 'Parent_Education_Level' in df.columns:
        df_cleaned = df.dropna(subset=['Parent_Education_Level'])
    else:
        df_cleaned = df

    # Preencher os valores nulos de Attendance com a mediana
    if 'Attendance (%)' in df_cleaned.columns:
        attendance_median = df_cleaned['Attendance (%)'].median()
        df_cleaned['Attendance (%)'].fillna(attendance_median, inplace=True)
    
    # Exibir o somatório de Attendance
    if 'Attendance (%)' in df_cleaned.columns:
        print(f"\nSomatório de Attendance: {df_cleaned['Attendance (%)'].sum()}")
    
    return df_cleaned

# Função para consultar dados
def consultar_dados(df):
    coluna = input("\nDigite o nome da coluna para consulta (ex: Midterm_Score, Final_Score, etc.): ")
    if coluna in df.columns:
        print(f"\nConsultando dados da coluna {coluna}:")
        print(f"Média: {df[coluna].mean()}")
        print(f"Mediana: {df[coluna].median()}")
        print(f"Moda: {df[coluna].mode()[0]}")
        print(f"Desvio padrão: {df[coluna].std()}")
    else:
        print(f"\nColuna {coluna} não encontrada no dataset.")

# Função para gerar gráficos
def gerar_graficos(df):
    # Gráfico de dispersão: "horas de sono" vs "nota final"
    if 'Sleep_Hours_per_Night' in df.columns and 'Final_Score' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Sleep_Hours_per_Night'], df['Final_Score'])
        plt.title('Horas de Sono vs Nota Final')
        plt.xlabel('Horas de Sono')
        plt.ylabel('Nota Final')
        plt.show()
    else:
        print("\nColunas 'Sleep_Hours_per_Night' ou 'Final_Score' não encontradas no dataset.")
    
    # Gráfico de barras: idade x média das notas intermediárias (Midterm_Score)
    if 'Age' in df.columns and 'Midterm_Score' in df.columns:
        df['Age_group'] = pd.cut(df['Age'], bins=[0, 17, 21, 24, np.inf], labels=['Até 17', '18 a 21', '21 a 24', '25 ou mais'])
        age_group_avg = df.groupby('Age_group')['Midterm_Score'].mean()

        age_group_avg.plot(kind='bar', figsize=(10, 6), title='Idade x Média das Notas de Midterm')
        plt.xlabel('Faixa Etária')
        plt.ylabel('Média das Notas de Midterm')
        plt.show()
    else:
        print("\nColunas 'Age' ou 'Midterm_Score' não encontradas no dataset.")
    
    # Gráfico de pizza: distribuição de idades
    if 'Age_group' in df.columns:
        age_group_counts = df['Age_group'].value_counts()
        age_group_counts.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 8), title='Distribuição das Idades')
        plt.ylabel('')
        plt.show()
    else:
        print("\nColuna 'Age_group' não encontrada no dataset.")

# Função principal
def main():
    df = carregar_arquivo()
    if df is not None:
        exibir_resumo_estatistico(df)
        df_cleaned = limpar_dados(df)
        consultar_dados(df_cleaned)
        gerar_graficos(df_cleaned)
        
if __name__ == "__main__":
    main()