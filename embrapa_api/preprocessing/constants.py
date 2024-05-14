"""Constants used in the preprocessing module."""

from embrapa_api.config import CSV_FILES_FOLDER

# producao
TIPO_PRODUTO_MAP = {
    "vm": "Vinho de Mesa",
    "vv": "Vinho Fino de Mesa",
    "su": "Suco",
    "de": "Derivados",
}
EXPECTED_AGG_PRODUCTS = set(
    ['DERIVADOS', 'SUCO', 'VINHO DE MESA', 'VINHO FINO DE MESA (VINIFERA)']
)
PRODUCAO_FILE_PATH = f'{CSV_FILES_FOLDER}/producao_vinho/Producao.csv'


# Processamento
PROCESSAMENTO_PATHS = {
    "Viniferas": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv',
        "path": f'{CSV_FILES_FOLDER}/processamento_vinho/ProcessaViniferas.csv',
    },
    "Americanas": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv',
        "path": f'{CSV_FILES_FOLDER}/processamento_vinho/ProcessaAmericanas.csv',
    },
    "Uvas de mesa": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv',
        "path": f'{CSV_FILES_FOLDER}/processamento_vinho/ProcessaMesa.csv',
    },
    "Sem Classe": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemClasse.csv',
        "path": f'{CSV_FILES_FOLDER}/processamento_vinho/ProcessaSemclass.csv',
    },
}
