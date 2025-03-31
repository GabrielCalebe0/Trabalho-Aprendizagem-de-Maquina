import pandas as pd
import matplotlib.pyplot as plt 
import os

def carregar_dados():
    # Opcão de escolha que arquivo CSV ou JSON para carregar os dados e exemplo do nome de arquivo que consta em nosso sistema.
    arquivo = input("Digite o caminho do arquivo CSV ou JSON (exemplo: Students-grading-dataset.csv ou Students-grading-dataset.json): ")

    # Verifica se o arquivo existe e caso esteja incorreto avisar que não foi encontrado.
    if not os.path.isfile(arquivo):
        print(f"Erro: O arquivo {arquivo} não foi encontrado.")
        return None

    # Carrega o arquivo CSV ou JSON
    if arquivo.endswith("Students_Grading_Dataset.csv"):
        dados = pd.read_csv(arquivo)
    elif arquivo.endswith("Students_Grading_Dataset.json"):
        dados = pd.read_json(arquivo)
    else:
        print("Erro: O arquivo deve ser CSV ou JSON.")
        return None
    
    return dados

def resumo_estatistico(dados):
    """Exibe um resumo estatístico dos dados."""
    print("\nResumo Estatístico dos Dados:")
    print(dados.describe())

def analises_especificas(dados):
    """Realiza as análises específicas solicitadas."""
    # Quantidade total de dados carregados
    total_dados = len(dados)
    print(f"\nQuantidade total de dados carregados: {total_dados}")

    # Contagem de homens e mulheres (assumindo que a coluna 'gender' exista)
    if 'gender' in dados.columns:
        genero_contagem = dados['gender'].value_counts()
        print(f"\nQuantidade de homens e mulheres:\n{genero_contagem}")
    else:
        print("\nA coluna 'gender' não está presente nos dados.")

    # Quantidade de registros sem dados sobre a educação dos pais (assumindo a coluna 'parental_level_of_education')
    if 'parental_level_of_education' in dados.columns:
        registros_sem_educacao_pais = dados['parental_level_of_education'].isna().sum()
        print(f"\nQuantidade de registros sem dados sobre a educação dos pais: {registros_sem_educacao_pais}")
    else:
        print("\nA coluna 'parental_level_of_education' não está presente nos dados.")

def visualizacao(dados):
    """Gera gráficos de visualização com base nos dados."""
    # Gráfico de gênero
    if 'gender' in dados.columns:
        genero_contagem = dados['gender'].value_counts()
        genero_contagem.plot(kind='bar', title="Distribuição por Gênero", color=['blue', 'pink'])
        plt.xlabel('Gênero')
        plt.ylabel('Contagem')
        plt.xticks(rotation=0)
        plt.show()

    # Gráfico de educação dos pais
    if 'parental_level_of_education' in dados.columns:
        educacao_pais_contagem = dados['parental_level_of_education'].value_counts()
        educacao_pais_contagem.plot(kind='bar', title="Distribuição por Nível de Educação dos Pais", color='green')
        plt.xlabel('Nível de Educação dos Pais')
        plt.ylabel('Contagem')
        plt.xticks(rotation=45)
        plt.show()

def main():
    """Função principal para executar o analisador de dados."""
    # Carregar os dados
    dados = carregar_dados()

    if dados is not None:
        # Exibir resumo estatístico
        resumo_estatistico(dados)

        # Realizar análises específicas
        analises_especificas(dados)

        # Visualização dos dados
        visualizacao(dados)

if __name__ == "__main__":
    main()