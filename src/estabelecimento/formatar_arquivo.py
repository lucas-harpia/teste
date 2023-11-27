import csv
import os
from src.telegram import add_log, send_all_logs


def formatar_arquivo(input_filename):
    linhas_modificadas = []

    arquivo_csv = 'arquivo_format.csv'
    arquivo_csv_saida = 'arquivo_alterado.csv'

    with open(input_filename, 'r', encoding='latin-1') as txt_file, open(arquivo_csv, 'w', encoding='utf-8', newline='') as csv_file:
        # Lê linhas do arquivo de texto e escreve no arquivo CSV
        csv_writer = csv.writer(csv_file, delimiter=';')
        for line in txt_file:
            values = line.strip().split(';')

            # Remove as aspas dos valores
            values = [valor.strip('\"') for valor in values]

            csv_writer.writerow(values)

    # Abre o arquivo CSV novamente para leitura e manipulação
    with open(arquivo_csv, 'r', encoding='utf-8') as csv_file:
        leitor_csv = csv.reader(csv_file, delimiter=';')

        for linha in leitor_csv:
            # Juntar os valores do primeiro, segundo e terceiro campo
            novo_valor = linha[0] + linha[1] + linha[2]

            # Adicionar o novo valor no último campo
            linha.append(str(novo_valor))

            # Remover o segundo e o terceiro campo
            del linha[1:3]

            # Adicionar a linha modificada à lista
            linhas_modificadas.append(linha)

    # Salva as alterações em um novo arquivo CSV
    with open(arquivo_csv_saida, 'w', encoding='utf-8', newline='') as csv_saida:
        csv_writer_saida = csv.writer(csv_saida, delimiter=';')
        csv_writer_saida.writerows(linhas_modificadas)

    os.remove('arquivo_atualizacao.txt')
    os.remove(arquivo_csv)
    add_log(f'Arquivo Formatado.\n')
    # inserir_dados_do_arquivo(arquivo_csv_saida, 'estabelecimento', '../cnpj.db')
