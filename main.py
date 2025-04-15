import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função que ira carregar os dados
def carregar_arquivo():
    caminho = input("Digite o caminho do arquivo .csv ou .json: ")

    # Opções de arquivos disponiveis para leitura
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
    print(f'\n--- Resumo Estatístico dos Dados ---\n')

    # Quantidade dos registros
    total_registros = len(df)
    print(f"Quantidade total de registros: {total_registros}")
    (f'Resumo: {total_registros} registros carregados.')

    # 2. Quantidade de homens e mulheres
    if "Gender" in df.columns:
        quantidade_homens = (df['Gender'] == 'Male').sum()
        quantidade_mulheres = (df['Gender'] == 'Female').sum()

        print(f"Quantidade de homens: {quantidade_homens}")
        print(f"Quantidade de mulheres: {quantidade_mulheres}")
        (f'Resumo: {quantidade_homens} homens e {quantidade_mulheres} mulheres.')
    else:
        print("Coluna 'Gender' não encontrada no dataset.")

    # 3. Quantidade de dados sobre a educação dos pais
    if "Parent_Education_Level" in df.columns:
        registros_sem_educacao_pais = df['Parent_Education_Level'].isna().sum()
        print(f"Registros sem dados sobre a educação dos pais: {registros_sem_educacao_pais}")
        (f'Resumo: {registros_sem_educacao_pais} registros sem dados sobre educação dos pais.')
    else:
        print("Coluna 'Parent_Education_Level' não encontrada no dataset.")

def limpar_dados(df):
    print("\n--- Iniciando limpeza dos dados ---")

    # Removendo registro vazio
    if 'Parent_Education_Level' in df.columns:
        antes = len(df)
        df = df.dropna(subset=['Parent_Education_Level'])
        depois = len(df)
        print(f"Registros removidos por falta de informação sobre a educação dos pais: {antes - depois}")
    else:
        print("Coluna 'Parent_Education_Level' não encontrada no dataset.")

    if 'Attendance (%)' in df.columns:
        nulos_antes = df['Attendance (%)'].isna().sum()
        attendance_median = df['Attendance (%)'].median()
        df['Attendance (%)'] = df['Attendance (%)'].fillna(attendance_median)
        nulos_depois = df['Attendance (%)'].isna().sum()
        print(f"Valores nulos em 'Attendance (%)' preenchidos com a mediana: {nulos_antes - nulos_depois}")
    else:
        print("Coluna 'Attendance (%)' não encontrada no dataset.")

    # Somatório de Attendance
    if 'Attendance (%)' in df.columns:
        somatorio = df['Attendance (%)'].sum()
        print(f"Somatório de 'Attendance (%)': {somatorio}")
    else:
        print("Coluna 'Attendance (%)' não encontrada no dataset.")

    print("--- Limpeza concluída ---")
    return df

def consultar_dados(df):
    print("\n--- Consulta de Estatísticas ---")

    # Listar colunas disponíveis
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

    if not colunas_numericas:
        print("Não há colunas disponíveis para análise.")
        return

    print("Colunas disponíveis:")
    for i, col in enumerate(colunas_numericas, start=1):
        print(f"{i}. {col}")

    escolha = input("\nDigite o nome da coluna que deseja consultar: ")

    if escolha in colunas_numericas:
        print(f"\nEstatísticas da coluna '{escolha}':")
        print(f"- Média: {df[escolha].mean():.2f}")
        print(f"- Mediana: {df[escolha].median():.2f}")

        try:
            moda = df[escolha].mode()
            if not moda.empty:
                print(f"- Moda: {moda[0]:.2f}")
            else:
                print("- Moda: Não existe moda (valores únicos)")
        except:
            print("- Moda: Erro ao calcular a moda")

        print(f"- Desvio Padrão: {df[escolha].std():.2f}")
    else:
        print(f"\nColuna '{escolha}' não encontrada ou não é numérica.")

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

def main():
    df = carregar_arquivo()
    if df is not None:
        exibir_resumo_estatistico(df)
        df_cleaned = limpar_dados(df)
        consultar_dados(df_cleaned)
        gerar_graficos(df_cleaned)
        
if __name__ == "__main__":
    main()