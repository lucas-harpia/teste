def contar_campos(input_filename):
    linhas_com_campos_diferentes = 0

    with (open(input_filename, 'r', encoding='latin-1') as arquivo):
        for linha in arquivo:
            campos = linha.strip().split(';')
            numero_de_campos = len(campos)
            if numero_de_campos != 29:
                print('OLHA O PILANTRA AQUI: ', numero_de_campos)
                linhas_com_campos_diferentes += 1

            print(f'Total de linhas com campos diferentes de 30: {linhas_com_campos_diferentes}')


# Substitua 'seuarquivo.csv' pelo nome do seu arquivo
contar_campos('arquivo_alterado.csv')