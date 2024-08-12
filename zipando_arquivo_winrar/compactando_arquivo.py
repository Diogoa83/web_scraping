# import os
# import zipfile

# def zip_folder(caminho_do_arquivo, output_path):
#     with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for root, dirs, files in os.walk(caminho_do_arquivo):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 arcname = os.path.relpath(file_path, start=caminho_do_arquivo)
#                 zipf.write(file_path, arcname)

# folder_to_zip = r"C:\Users\diogoantonio\Documents\Python Scripts"
# output_zip = r"C:\Users\diogoantonio\Documents\Python Scripts.zip"

# zip_folder(folder_to_zip, output_zip)



# import subprocess
# import os

# def rar_folder(caminho_do_arquivo, caminho_para_enviar):
#     caminho_do_winrar = r"C:\Program Files\WinRAR\WinRAR.exe"
    
#     # Comando para criar um arquivo RAR
#     command = [
#         caminho_do_winrar,
#         'a',  # Comando para adicionar arquivos ao RAR
#         '-r',  # Comando para adicionar arquivos recursivamente
#         caminho_para_enviar,  # Caminho do arquivo RAR de saída
#         caminho_do_arquivo  # Caminho da pasta a ser compactada
#     ]
    
#     # Executa o comando
#     subprocess.run(command, check=True)

# folder_to_rar = r"C:\Users\jesusda\Documents\VSCode Projetos"
# caminho_para_enviar = r"C:\Users\jesusda\Documents\VSCode Projetos.rar"

# rar_folder(folder_to_rar, caminho_para_enviar)


import subprocess

def rar_folder(caminho_do_arquivo, caminho_para_enviar):
    caminho_do_winrar = r"C:\Program Files\WinRAR\WinRAR.exe"
    
    command = [
        caminho_do_winrar,
        'a',  # Comando para adicionar arquivos ao RAR
        '-r',  # Comando para adicionar arquivos recursivamente
        caminho_para_enviar,  # Caminho do arquivo RAR de saída
        caminho_do_arquivo  # Caminho da pasta a ser compactada
    ]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    for line in process.stdout:
        if "100%" in line:
            print("Compactação concluída com 100%!")
    
    process.wait()  # Espera o processo terminar

    if process.returncode == 0:
        print("Processo finalizado com sucesso.")
    else:
        print("Ocorreu um erro durante a compactação.")

folder_to_rar = r"C:\Users\jesusda\Documents\VSCode Projetos"
caminho_para_enviar = r"C:\Users\jesusda\Documents\VSCode Projetos.rar"

rar_folder(folder_to_rar, caminho_para_enviar)
