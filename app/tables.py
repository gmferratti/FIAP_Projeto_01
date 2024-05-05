def extract_table(soup):
    '''Extrai a tabela principal da página HTML.'''
    # Extraindo a tabela principal
    tabela_principal = None
    for table in soup.find_all('table'):
        if 'tb_dados' in table.get('class', []):
            tabela_principal = table
            break

    # Verificando se a tabela principal foi encontrada
    if tabela_principal:
        # Extraindo os cabeçalhos da tabela
        cabecalhos = [
            th.text.strip()
            for th in tabela_principal.find('thead').find('tr').find_all('th')
        ]

        # Extraindo os dados da tabela
        dados = []
        for row in tabela_principal.find('tbody').find_all('tr'):
            dados_row = [td.text.strip() for td in row.find_all('td')]
            dados.append(dados_row)

        # Extraindo o rodapé da tabela
        rodape = [
            td.text.strip()
            for td in tabela_principal.find('tfoot').find('tr').find_all('td')
        ]

        tabela = {"cabecalhos": cabecalhos, "dados": dados, "rodape": rodape}

    return tabela
