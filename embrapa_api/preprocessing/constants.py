"""Constants used in the preprocessing module."""

from embrapa_api.config import CSV_FILES_FOLDER

# producao
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

# Comercializacao
COMERCIALIZACAO_FILE_PATH = f'{CSV_FILES_FOLDER}/comercializacao_vinho/Comercio.csv'

# Importacao
IMPORTACAO_PATHS = {
    "Vinhos": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv',
        "path": f'{CSV_FILES_FOLDER}/importacao/ImpVinhos.csv',
    },
    "Sucos": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv',
        "path": f'{CSV_FILES_FOLDER}/importacao/ImpSuco.csv',
    },
    "Espumantes": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv',
        "path": f'{CSV_FILES_FOLDER}/importacao/ImpEspumantes.csv',
    },
    "Frescas": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv',
        "path": f'{CSV_FILES_FOLDER}/importacao/ImpFrescas.csv',
    },
    "Passas": {
        "url": 'http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv',
        "path": f'{CSV_FILES_FOLDER}/importacao/ImpPassas.csv',
    },
}
