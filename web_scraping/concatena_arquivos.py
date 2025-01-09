import os
import pandas as pd
from dbfread import DBF

caminho_dbf = r"/opt/airflow/scripts/sinan"
caminho_saida_csv = r"/opt/airflow/scripts/sinan_"

def concatenar_dbf_para_csv(prefixo, arquivo_saida):
    """
    Concatena todos os arquivos DBF com o mesmo prefixo (independentemente do tamanho)
    em um único DataFrame e salva como um arquivo CSV.
    """
    arquivos_filtrados = [
        arquivo for arquivo in os.listdir(caminho_dbf)
        if prefixo in arquivo and arquivo.endswith('.dbf')
    ]
    
    dataframes = []
    arquivos_processados = set()
    
    for arquivo in arquivos_filtrados:
        nome_base = os.path.splitext(arquivo)[0]
        if nome_base not in arquivos_processados:
            arquivos_similares = [
                arq for arq in arquivos_filtrados if nome_base in arq
            ]
            arquivos_processados.add(nome_base)
            
            for similar in arquivos_similares:
                caminho_arquivo = os.path.join(caminho_dbf, similar)
                try:
                    dbf_table = DBF(caminho_arquivo, encoding='latin1')
                    df = pd.DataFrame(iter(dbf_table))
                    dataframes.append(df)
                    print(f'Arquivo {similar} processado com sucesso.')
                except Exception as e:
                    print(f'Erro ao processar {similar}: {e}')

    if dataframes:
        df_concatenado = pd.concat(dataframes, ignore_index=True)
        caminho_saida = os.path.join(caminho_saida_csv, arquivo_saida)
        df_concatenado.to_csv(caminho_saida, index=False)
        print(f'Arquivo final salvo em {caminho_saida}')
    else:
        print(f'Nenhum arquivo encontrado para o prefixo {prefixo}.')

def deletar_arquivos_desnecessarios(pasta, excecoes):
    """
    Deleta todos os arquivos na pasta especificada que não estão na lista de exceções.
    """
    arquivos = [arquivo for arquivo in os.listdir(pasta)]
    for arquivo in arquivos:
        if arquivo not in excecoes:
            caminho_arquivo = os.path.join(pasta, arquivo)
            try:
                os.remove(caminho_arquivo)
                print(f'Arquivo {arquivo} excluído com sucesso.')
            except Exception as e:
                print(f'Erro ao excluir o arquivo {arquivo}: {e}')

concatenar_dbf_para_csv('CHIKON', 'CHIKON2024.csv')
concatenar_dbf_para_csv('DENGON', 'DENGON2024.csv')

deletar_arquivos_desnecessarios(caminho_dbf, ['CHIKON2024.csv', 'DENGON2024.csv'])
deletar_arquivos_desnecessarios(caminho_saida_csv, ['CHIKON2024.csv', 'DENGON2024.csv'])
