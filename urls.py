from itertools import product
import json

def map_urls(base_url):
    """
    Mapeia todas as URLs possíveis do site da EMBRAPA.

    :param base_url: a URL da homepage
    :return: url_dict: dicionário com todas as urls por opt do site
    """
    # Dicionário de opções de cada página e seus respectivos parâmetros
    options_params = {
        "opt_02": ["ano"],
        "opt_03": ["ano", "subopt"],
        "opt_04": ["ano"],
        "opt_05": ["ano", "subopt"],
        "opt_06": ["ano", "subopt"],
    }

    # Dicionário para armazenar todas as URLs geradas
    url_dict = {}

    # Lista com todos os anos possíveis de serem consultados
    all_years = range(1970, 2023)

    # Gerar URLs para cada opção
    for option, params in options_params.items():
        # Verificar se há subopções para esta opção
        if "subopt" in params:
            # Determinar o número de subopções para cada opção
            num_suboptions = get_num_suboptions(option)
            # Gerar URLs para cada subopção
            for subopt_num in range(1, num_suboptions + 1):
                # Gerar todas as combinações possíveis de parâmetros
                param_combinations = product(all_years,
                                             [subopt_num])
                # Para cada combinação nas combinações de parâmetros
                for combination in param_combinations:
                    url = generate_url(base_url, option, params, combination)
                    key_str = str(option) + "_subopt_0" + str(combination[1]) + "_" + str(combination[0])
                    url_dict[key_str] = url
        else:
            # Se não houver subopções, gerar URLs apenas com os anos
            param_combinations = product(all_years)
            for combination in param_combinations:
                url = generate_url(base_url, option, params, combination)
                key_str = str(option) + "_" + str(combination[0])
                url_dict[key_str] = url
    return url_dict

def get_num_suboptions(option:str):
  """Retorna o número de subpções para cada opção de página do site"""
  if option == "opt_03":
    return 4
  elif option == "opt_05":
    return 5
  elif option == "opt_06":
    return 4
  else:
    return 0

def generate_url(base_url, option, params, combination):
    """
    Gera uma única URL com base nos parâmetros fornecidos.

    :param base_url: a URL base
    :param option: a opção
    :param params: os parâmetros
    :param combination: a combinação de valores para os parâmetros
    :return: url: a URL gerada
    """
    # Construir a URL com os valores daquela combinação
    url_params = "&".join([f"{param}={value}" for param, value in zip(params, combination)])
    url = f"{base_url}?{url_params}&opcao={option}"
    return url

def get_url_for_option(url_dict, option, year, suboption=None):
    """
    Retorna a URL correspondente para uma determinada opção, ano e subopção (opcional).

    :param url_dict: Dicionário contendo as URLs mapeadas por opção.
    :param option: Opção desejada.
    :param year: Ano desejado.
    :param suboption: Subopção desejada (opcional).
    :return: A URL correspondente à combinação de opção, ano e subopção (se fornecida).
    """
    # Construir a chave para procurar no dicionário
    if suboption is not None:
        key = f"opt_0{option}_subopt_0{suboption}_{year}"
    else:
        key = f"opt_0{option}_{year}"

    # Verificar se a chave existe no dicionário
    if key in url_dict:
        # Retorna a URL correspondente
        return url_dict[key]

    # Se a combinação de opção, ano ou subopção (se fornecida) não existir, retornar None
    return None