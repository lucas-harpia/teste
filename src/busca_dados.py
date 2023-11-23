import os
import sqlite3


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def select_dados(chave_busca, valor):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(script_dir, 'cnpj.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory

    cursor = conn.cursor()

    # chaves_pesquisa = {
    #     'cpf': 'CPF_CNPJ_EMBARGADO',
    #     'cnpj': 'CPF_CNPJ_EMBARGADO',
    #     'nome': 'NOME_PESSOA_EMBARGADA_NO_ACCENTS',
    #     'razao': 'NOME_PESSOA_EMBARGADA_NO_ACCENTS',
    # }

    cursor.execute(f"SELECT * FROM empresas WHERE {chave_busca} = ?;", [valor])
    results = cursor.fetchall()
    conn.close()
    return results


print(select_dados('cnpj_basico', '41273593'))
