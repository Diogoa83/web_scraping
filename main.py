
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import os
import pandas as pd



def acessar_arquivos_para_download(page):
    """Função para acessar o menu de download e baixar os arquivos."""
    print("Acessando o menu de downloads...")
    page.click('div#barraMenu\\:j_id52_span.rich-label-text-decor')
    time.sleep(5)

    page.click('span#barraMenu\\:j_id56\\:anchor')
    time.sleep(5)

    caminho = r"/opt/airflow/scripts/sinan"   

    while True:
        print("Verificando o status das solicitações...")
        # Localizar todos os elementos de status na terceira coluna da tabela
        status_elements = page.locator("table tbody tr td:nth-child(3) center")
        number_of_statuses = status_elements.count()
        print(f"Total de status encontrados: {number_of_statuses}")

        # Contar quantos "Processamento concluído" existem
        completed_status_count = 0
        for i in range(number_of_statuses):
            status_text = status_elements.nth(i).inner_text().strip()
            if "Processamento concluído" in status_text:
                completed_status_count += 1

        print(f"Número de 'Processamento concluído': {completed_status_count}")

        # Se todos os status estiverem como "Processamento concluído"
        if completed_status_count == number_of_statuses and number_of_statuses > 0:
            print("Todos os processos foram concluídos.")
            # Agora, baixa todos os arquivos disponíveis
            links = page.locator("a:text('Baixar arquivo DBF')")
            number_of_links = links.count()
            print(f"Total de links para download: {number_of_links}")

            for i in range(number_of_links):
                print(f"Baixando arquivo {i+1} de {number_of_links}...")
                with page.expect_download() as download_info:
                    links.nth(i).click()  
                download = download_info.value

                # Verifica se o caminho de destino existe
                if os.path.exists(caminho):
                    arquivo_destino = os.path.join(caminho, download.suggested_filename)
                    download.save_as(arquivo_destino)
                    print(f"Arquivo baixado e salvo em: {arquivo_destino}")
                else:
                    print(f"Caminho de destino não existe: {caminho}")
                time.sleep(2)  
            break  
        else:
            print("Nem todos os processos foram concluídos. Atualizando a página...")
            atualizar_botao = page.locator("input[value='Atualizar']")
            if atualizar_botao.is_visible():
                atualizar_botao.click()
                time.sleep(5)  
            else:
                print("Botão de atualização não encontrado. Tentando novamente...")
                time.sleep(5) 


def solicitar_dados(page, ano, doenca, codigo):
    print("funcao 2 'solicitar_dados' rodando")
    """Função para solicitar dados de um determinado ano e doença."""
    print(f"Solicitando {doenca} para o ano {ano}...")
    page.click('div#barraMenu\\:j_id52_span.rich-label-text-decor')
    time.sleep(5)
    page.click('span#barraMenu\\:j_id53\\:anchor')
    time.sleep(5)

    page.check('input[name="form:j_id124"]')
    time.sleep(5)
    page.fill('input[id="form\\:consulta_dataInicialInputDate"]', f'01/01/{ano}')
    time.sleep(5)
    page.fill('input[id="form\\:consulta_dataFinalInputDate"]', f'31/12/{ano}')
    time.sleep(5)
    page.select_option('select[id="form\\:tipoUf"]', '3')
    time.sleep(5)
    page.select_option('select[name="form:j_id120"]', codigo)
    time.sleep(5)
    page.click('input#form\\:j_id128', force=True)
    time.sleep(5)

def solicitar_dia_anterior(page, ano_anterior, doenca, codigo):
    print("funcao 3 'solicitar_dia_anterior' rodando")
    """Função para solicitar o dia 31/12 do ano anterior."""
    print(f"Solicitando {doenca} para o dia 31/12/{ano_anterior}...")
    page.click('div#barraMenu\\:j_id52_span.rich-label-text-decor')
    time.sleep(5)
    page.click('span#barraMenu\\:j_id53\\:anchor')
    time.sleep(5)

    page.check('input[name="form:j_id124"]')
    time.sleep(5)
    page.fill('input[id="form\\:consulta_dataInicialInputDate"]', f'31/12/{ano_anterior}')
    time.sleep(5)
    page.fill('input[id="form\\:consulta_dataFinalInputDate"]', f'31/12/{ano_anterior}')
    time.sleep(5)
    page.select_option('select[id="form\\:tipoUf"]', '3')
    time.sleep(5)
    page.select_option('select[name="form:j_id120"]', codigo)
    time.sleep(5)
    page.click('input#form\\:j_id128', force=True)
    time.sleep(5)

def perform_login(page, username, password):
    print("funcao 4 'perform_login' rodando")
    """Função para realizar o login com credenciais fornecidas."""
    page.fill('input[id="form\\:username"]', username)
    time.sleep(5)
    page.fill('input[id="form\\:password"]', password)
    time.sleep(5)
    page.click('input[name="form:j_id21"][value="Entrar"][class="botao"]')
    time.sleep(5) 

def is_logged_in(page):
    print("funcao 5 'is_logged_in' rodando")
    """Função para verificar se o login foi bem-sucedido."""
    try:
        page.wait_for_selector('div#barraMenu\\:j_id52_span.rich-label-text-decor', timeout=5000)
        return True
    except:
        return False

def test_login(page):
    print("funcao 6 'test_login' rodando")
    """Função principal para login e navegação."""
    page.goto("https://sinan.saude.gov.br/sinan/login/login.jsf")
    time.sleep(5)

    username = 'viniciusvieira'  
    password = 'vinieduvi'       

    perform_login(page, username, password)

    if not is_logged_in(page):
        print("Primeiro login falhou, tentando novamente...")
        perform_login(page, username, password)

        if not is_logged_in(page):
            raise Exception("Falha ao realizar login após duas tentativas.")
        else:
            print("Login bem-sucedido na segunda tentativa.")
    else:
        print("Login bem-sucedido na primeira tentativa.")

    #ano_atual = 2025
    ano_atual = datetime.today().year
    for ano in range(2023, ano_atual + 1):
        for doenca, codigo in [("FEBRE DE CHIKUNGUNYA", "1"), ("DENGUE", "0")]:
            solicitar_dados(page, ano, doenca, codigo)
            if ano == 2023:  # Solicitar dia anterior apenas para o primeiro ano
                solicitar_dia_anterior(page, ano - 1, doenca, codigo)

    acessar_arquivos_para_download(page)

def run():
    print("funcao 7 'run' rodando")
    """Função para iniciar o navegador."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            test_login(page)
        except Exception as e:
            print(f"Erro ao tentar executar o script: {e}")
        finally:
            print("Encerrando o navegador...")
            browser.close()

if __name__ == "__main__":
    run()

