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
    """Gera gráficos para visualização dos dados."""
    if df is None or df.empty:
        print("Nenhum dado disponível para gráficos.")
        return

    # Gráfico de dispersão: sono vs nota
    if all(col in df.columns for col in ['Sleep_Hours_per_Night', 'Final_Score']):
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Sleep_Hours_per_Night'], df['Final_Score'], alpha=0.5)
        plt.title('Relação entre Horas de Sono e Nota Final')
        plt.xlabel('Horas de Sono por Noite')
        plt.ylabel('Nota Final')
        plt.grid(True)
        plt.show()
    else:
        print("\nDados insuficientes para gerar gráfico de Sono vs Nota.")

    # Gráfico de barras: idade vs nota média
    if all(col in df.columns for col in ['Age', 'Midterm_Score']):
        df['Faixa Etária'] = pd.cut(df['Age'], 
                                   bins=[0, 17, 21, 24, 100],
                                   labels=['<18', '18-21', '22-24', '25+'])
        
        age_score = df.groupby('Faixa Etária')['Midterm_Score'].mean()
        
        plt.figure(figsize=(10, 6))
        age_score.plot(kind='bar', color='skyblue')
        plt.title('Média de Notas por Faixa Etária')
        plt.xlabel('Faixa Etária')
        plt.ylabel('Média da Nota')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()
    else:
        print("\nDados insuficientes para gerar gráfico de Idade vs Nota.")


def main():
    print("=== Análise de Dados de Estudantes ===")
    
    df = carregar_arquivo()
    if df is not None:
        exibir_resumo_estatistico(df)
        df = limpar_dados(df)
        
        while True:
            print("\nMenu Principal:")
            print("1. Consultar estatísticas")
            print("2. Gerar gráficos")
            print("3. Sair")
            
            opcao = input("Escolha uma opção, sendo 1, 2 ou 3: ")
            
            if opcao == '1':
                consultar_dados(df)
            elif opcao == '2':
                gerar_graficos(df)
            elif opcao == '3':
                print("Análise finalizada :)")
                break
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
