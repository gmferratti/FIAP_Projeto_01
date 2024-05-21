from unittest.mock import call, patch

import pandas as pd
import pytest

from embrapa_api.preprocessing.preprocessors import ProducaoPreprocessor


@pytest.fixture
def producao_preprocessor():
    """Fixture que cria e retorna uma instância da classe ProducaoPreprocessor."""
    return ProducaoPreprocessor()


def test_load_data_success(producao_preprocessor):
    """
    Testa se o método load_data consegue carregar dados com sucesso de uma URL.
    Verifica se os dados carregados correspondem exatamente ao mock definido e
    se a função read_csv é chamada corretamente com a URL esperada.
    """
    with patch("pandas.read_csv") as mock_read_csv:
        # Setup our mock
        mock_df = pd.DataFrame(
            {
                "id": [1, 2],
                "produto": ["produto1", "produto2"],
                "control": ["control1", "control2"],
                "2020": [100, 200],
                "2021": [150, 250],
            }
        )
        mock_read_csv.return_value = mock_df

        # Execute
        result = producao_preprocessor.load_data()

        # Assert
        assert not result.empty
        assert result.equals(mock_df)
        mock_read_csv.assert_called_once_with(
            'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv', sep=';'
        )


def test_load_data_failure_url_then_success_local(producao_preprocessor):
    """
    Testa o comportamento de fallback do método load_data quando a tentativa de carregar
    dados de uma URL falha. Verifica se, após a falha, o método tenta carregar os dados
    de um caminho de arquivo local e confirma que os dados carregados são válidos.
    """
    with patch("pandas.read_csv") as mock_read_csv:
        # Configuração do mock para simular falha
        # na primeira chamada e sucesso na segunda
        mock_read_csv.side_effect = [
            Exception("Failed to fetch data from URL"),  # Primeira chamada falha
            pd.DataFrame(
                {  # Segunda chamada retorna DataFrame de fallback
                    "id": [1, 2],
                    "produto": ["produto1", "produto2"],
                    "control": ["control1", "control2"],
                    "2020": [100, 200],
                    "2021": [150, 250],
                }
            ),
        ]

        # Executa
        result = producao_preprocessor.load_data()

        # Assertiva
        assert not result.empty
        assert result.iloc[0]["produto"] == "produto1"
        assert mock_read_csv.call_count == 2
        assert mock_read_csv.call_args_list[0] == call(
            'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv', sep=';'
        )
        assert 'Producao.csv' in mock_read_csv.call_args_list[1][0][0]


def test_preprocess(producao_preprocessor):
    """
    Testa se o método preprocess transforma os dados corretamente conforme esperado.
    Este teste verifica a estrutura do DataFrame resultante e a correta conversão e
    mapeamento de valores específicos.
    """
    # Setup initial DataFrame
    producao_preprocessor.rw_producao = pd.DataFrame(
        {
            "id": [1],
            "produto": ["produto1"],
            "control": ["vm_produto1"],
            "2020": [100],
            "2021": [150],
        }
    )

    # Execute
    result = producao_preprocessor.preprocess()

    # Verify the structure and some data of the resulting DataFrame
    expected_columns = [
        "ID_PRODUTO",
        "NM_PRODUTO",
        "DT_ANO",
        "VR_PRODUCAO_L",
        "TIPO_PRODUTO",
    ]
    assert all(col in result.columns for col in expected_columns)
    assert result["NM_PRODUTO"].iloc[0] == "Produto1"
    assert result["TIPO_PRODUTO"].iloc[0] == "Vinho de Mesa"
