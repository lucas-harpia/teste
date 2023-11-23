import sqlite3


def inserir_dados_do_arquivo(nome_arquivo, nome_tabela, conexao_banco):
    # Abrir o arquivo de texto
    with open(nome_arquivo, 'r', encoding='ISO-8859-1') as arquivo:
        linhas = arquivo.readlines()

        # Conectar ao banco de dados
        conexao = sqlite3.connect(conexao_banco)
        cursor = conexao.cursor()

        # Loop através das linhas do arquivo
        for linha in linhas:
            # Montar a instrução SQL de inserção sem remover as aspas e dividir os valores
            sql_insert = f"INSERT INTO {nome_tabela} VALUES ({', '.join(['?' for _ in linha.split(';')])})"

            # Executar a instrução SQL
            cursor.execute(sql_insert, linha.split(';'))

        # Commit e fechar a conexão
        conexao.commit()
        conexao.close()


# inserir_dados_do_arquivo("arquivo_alterado.csv", "estabelecimento", '../cnpj.db')
