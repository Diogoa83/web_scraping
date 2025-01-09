def extrair_zip():
    import os
    import zipfile
    from datetime import datetime
    import shutil

    caminho_pasta = r"/opt/airflow/scripts/sinan" 
    caminho_destino = r"/opt/airflow/scripts/sinan_" 

    def deletar_arquivos_anteriores_a_data_atual():
        agora = datetime.now()
        for arquivo in os.listdir(caminho_pasta):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))
                if data_modificacao.date() < agora.date():
                    os.remove(caminho_arquivo)
                    print(f'Arquivo {arquivo} deletado, pois é anterior à data atual.')

    def extrair_arquivos_zip():
        arquivos = os.listdir(caminho_pasta)
        dengue_count = 1
        chikon_count = 1

        for arquivo in arquivos:
            if arquivo.endswith('.zip'):
                caminho_arquivo = os.path.join(caminho_pasta, arquivo)
                
                with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                    zip_ref.extractall(caminho_pasta)

                print(f'{arquivo} extraído com sucesso!')

                # RENOMEANDO TODOS OS ARQUIVOS SERÃO RENOMEADOS PARA DENGON1, 2 E CHIKON1, 2
                for nome_arquivo in zip_ref.namelist():
                    caminho_original = os.path.join(caminho_pasta, nome_arquivo)
                    if nome_arquivo.startswith('DENGON'):
                        novo_nome = f'dengue{dengue_count}.dbf'
                        dengue_count += 2
                    elif nome_arquivo.startswith('CHIKON'):
                        novo_nome = f'chikon{chikon_count}.dbf'
                        chikon_count += 2
                    else:
                        continue
                    
                    caminho_novo = os.path.join(caminho_pasta, novo_nome)
                    if os.path.exists(caminho_novo):  
                        os.remove(caminho_novo)
                    if os.path.exists(caminho_original):  
                        os.rename(caminho_original, caminho_novo)
                        print(f'{nome_arquivo} renomeado para {novo_nome}')

    def limpar_pasta_destino():
        """Remove todos os arquivos da pasta destino."""
        if os.path.exists(caminho_destino):
            for arquivo in os.listdir(caminho_destino):
                caminho_arquivo = os.path.join(caminho_destino, arquivo)
                if os.path.isfile(caminho_arquivo):
                    os.remove(caminho_arquivo)
                    print(f'Arquivo {arquivo} deletado da pasta destino.')

    def mover_arquivos_para_destino():
        limpar_pasta_destino()  # Esvazia a pasta destino antes de mover os arquivos

        if not os.path.exists(caminho_destino):
            os.makedirs(caminho_destino)
        
        for arquivo in os.listdir(caminho_pasta):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            if os.path.isfile(caminho_arquivo) and arquivo.endswith('.dbf'):
                caminho_destino_arquivo = os.path.join(caminho_destino, arquivo)
                shutil.move(caminho_arquivo, caminho_destino_arquivo)
                print(f'Arquivo {arquivo} movido para {caminho_destino}.')

    def deletar_arquivos_zip():
        for arquivo in os.listdir(caminho_pasta):
            if arquivo.endswith('.zip'):
                caminho_arquivo = os.path.join(caminho_pasta, arquivo)
                os.remove(caminho_arquivo)
                print(f'Arquivo ZIP {arquivo} deletado.')

    def limpar_pasta_origem():
        for arquivo in os.listdir(caminho_pasta):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
                print(f'Arquivo {arquivo} deletado da pasta de origem.')


    # Fluxo de execução
    deletar_arquivos_anteriores_a_data_atual()
    extrair_arquivos_zip()
    mover_arquivos_para_destino()
    deletar_arquivos_zip()
    limpar_pasta_origem()

extrair_zip()