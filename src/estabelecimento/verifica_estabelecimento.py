import requests
import os
from bs4 import BeautifulSoup
from src.estabelecimento.download_estabelecimento import download_and_extract
from src.telegram import send_telegram_message

results = []


def messages(message):
    results.append(message)


def busca_novo_estabelecimento():
    messages('----PLUGIN-CNPJ-INICIADO-TABELA-ESTABELECIMENTO----\n')
    all_prints = "\n".join(results)
    send_telegram_message(all_prints)

    messages('----PLUGIN-CNPJ-CONSOLIDADO-TABELA-ESTABELECIMENTO----\n')
    base_url = 'https://dadosabertos.rfb.gov.br/CNPJ/'
    response = requests.get(base_url)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    arquivo_path = os.path.join(script_dir, 'arquivos_estabelecimento.txt')

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)

        with open(arquivo_path, 'r') as arquivo:
            content = [linha.strip("'\n") for linha in arquivo.readlines()]

        for link in links:
            link_sem_aspas_nova_linha = link['href'].strip("'\n")
            if 'Estabelecimentos' in link_sem_aspas_nova_linha and link_sem_aspas_nova_linha not in content:
                with open(arquivo_path, 'a') as arquivo:
                    arquivo.write(link['href'] + '\n')
                link_novo_estabelecimento = base_url + link['href']
                nome_arquivo = link['href']

                messages(f'Novo link encontrado: {link_novo_estabelecimento}\n')
                messages(f'Começando o download do novo arquivo: {nome_arquivo}\n')

                # Adicionando o código para o download aqui
                dest_filename = os.path.join(script_dir, nome_arquivo)
                download_and_extract(link_novo_estabelecimento, dest_filename)

        with open(arquivo_path, 'r') as arquivo:
            content = arquivo.readlines()
        messages('A lista de links de estabelecimento está atualizada.\n')
        messages(f'Lista atualizada de links de estabelecimentos no Banco de Dados:\n' + ''.join(content))
    else:
        messages(f'Falha na requisição HTTP: Status code {response.status_code}')

    all_prints = "\n".join(results)
    send_telegram_message(all_prints)


busca_novo_estabelecimento()
