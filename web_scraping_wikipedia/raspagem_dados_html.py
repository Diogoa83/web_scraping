import pandas as pd

url = 'https://www.ibge.gov.br/explica/pib.php'

tabela = pd.read_html(url)
tabela = tabela[0]
data  = pd.DataFrame(tabela)





print(tabela.info())


tabela.to_excel('tabela_pib_estados_brasileiros.xlsx')