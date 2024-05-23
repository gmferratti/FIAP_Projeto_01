from unittest.mock import patch

import pandas as pd
import pytest

from embrapa_api.preprocessing.preprocessors import ImportacaoPreprocessor


@pytest.fixture
def importacao_preprocessor(app_context):
    """Fixture para criar uma instância da classe
    ImportacaoPreprocessor dentro do contexto da aplicação."""
    return ImportacaoPreprocessor()


def test_load_data_success(importacao_preprocessor):
    """
    Testa o carregamento bem-sucedido dos dados de uma URL específica.
    Verifica se o read_csv é chamado corretamente com a URL e se os
    dados carregados são como esperado.
    """
    produto_importacao = "Vinhos"
    with patch('pandas.read_csv') as mock_read_csv:
        mock_data = pd.DataFrame(
            {
                "Id": [1, 2],
                "País": ["Brasil", "França"],
                "2020.1": [1000, 2000],
                "2020": [100, 200],
            }
        )
        mock_read_csv.return_value = mock_data
        importacao_preprocessor.importacao_paths = {
            produto_importacao: {"url": "fake_url", "path": "fake_path"}
        }

        result = importacao_preprocessor.load_data(produto_importacao)

        assert not result.empty
        assert result.equals(mock_data)


def test_load_data_failure(importacao_preprocessor):
    """
    Testa o comportamento de falha no carregamento de
    dados quando não há configuração de caminho. Verifica se
    o ValueError é levantado corretamente.
    """
    with pytest.raises(ValueError):
        importacao_preprocessor.load_data("Inexistente")


def test_process_import_data(importacao_preprocessor):
    """
    Testa o processamento dos dados de importação, verificando se o DataFrame
    resultante possui a estrutura esperada e se os valores são processados corretamente.
    """
    produto_importacao = "Vinhos"
    sample_data = pd.DataFrame(
        {"Id": [1], "País": ["Brasil"], "2020.1": [1000], "2020": [100]}
    )
    with patch.object(importacao_preprocessor, 'load_data', return_value=sample_data):
        result = importacao_preprocessor._processa_importacao(produto_importacao)
        expected_output = pd.DataFrame(
            {
                "NM_PAIS": ["Brasil"],
                "DT_ANO": ["2020"],
                "NM_ITEM": ["Vinhos"],
                "QTD_IMPORTADO_KG": [100],
                "VL_VALOR_IMPORTADO_USD": [1000],
            }
        )

        assert result.reset_index(drop=True).equals(expected_output)


def test_preprocess_integration(importacao_preprocessor):
    """
    Testa a integração do método preprocess com os submétodos de processamento
    de cada tipo de produto de importação.
    Verifica se a concatenação final dos DataFrames processados é feita corretamente.
    """
    product_types = importacao_preprocessor.importacao_paths.keys()

    # Cria uma lista de efeitos colaterais que fornece
    # um DataFrame para cada tipo de produto
    side_effects = [
        pd.DataFrame(
            {
                "NM_PAIS": [product],
                "DT_ANO": ["2020"],
                "NM_ITEM": [product],
                "QTD_IMPORTADO_KG": [100],
                "VL_VALOR_IMPORTADO_USD": [1000],
            }
        )
        for product in product_types
    ]

    with patch.object(
        importacao_preprocessor, '_processa_importacao', side_effect=side_effects
    ):
        result = importacao_preprocessor.preprocess()

        # Verifica se o número de entradas está correto
        assert len(result) == len(side_effects)
        # Verifica se todos os tipos de produtos estão representados nos resultados
        assert set(result["NM_ITEM"]) == set(product_types)
