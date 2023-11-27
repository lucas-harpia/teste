import requests
import os
from bs4 import BeautifulSoup
from src.estabelecimento.download_estabelecimento import download_and_extract
from src.telegram import add_log, send_telegram_message as send, send_all_logs


def busca_novo_estabelecimento():
    results = []

    send('----PLUGIN-CNPJ-INICIADO-TABELA-ESTABELECIMENTO----')
    add_log('----PLUGIN-CNPJ-CONSOLIDADO-TABELA-ESTABELECIMENTO----\n')

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
                add_log(f'Novo link encontrado: {link_novo_estabelecimento}\n')

                dest_filename = os.path.join(script_dir, nome_arquivo)
                download_and_extract(link_novo_estabelecimento, dest_filename)

        with open(arquivo_path, 'r') as arquivo:
            content = arquivo.readlines()
        add_log('A lista de links de estabelecimento está atualizada.\n')
        add_log(f'Lista atualizada de links de estabelecimentos no Banco de Dados:\n' + ''.join(content))
        send_all_logs()
    else:
        add_log(f'Falha na requisição HTTP: Status code {response.status_code}')
        send_all_logs()

busca_novo_estabelecimento()
