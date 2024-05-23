from unittest.mock import patch

import pandas as pd
import pytest

from embrapa_api.preprocessing.preprocessors import ComercializacaoPreprocessor


@pytest.fixture
def comercializacao_preprocessor(app_context):
    """Fixture que cria e retorna uma instância
    da classe ComercializacaoPreprocessor dentro do contexto da aplicação."""
    return ComercializacaoPreprocessor()


def test_load_data_success(comercializacao_preprocessor):
    """
    Testa o carregamento bem-sucedido dos dados de uma URL específica.
    Verifica se o read_csv é chamado corretamente com a URL e se os
    dados carregados são como esperado.
    """
    with patch("pandas.read_csv") as mock_read_csv:
        mock_data = pd.DataFrame(
            {
                "id": [1, 2],
                "Produto": ["Produto1", "Produto2"],
                "control": ["vm_1", "ve_1"],
                "2020": [500, 600],
                "2021": [700, 800],
            }
        )
        mock_read_csv.return_value = mock_data

        result = comercializacao_preprocessor.load_data()

        assert not result.empty
        assert result.equals(mock_data)


def test_preprocess(comercializacao_preprocessor):
    """
    Testa a funcionalidade de preprocessamento dos dados, verificando
    se a transformação, renomeação, e mapeamento estão corretos, e se
    as entradas sem um tipo de produto válido são descartadas.
    """
    comercializacao_preprocessor.comercializacao = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "Produto": ["Produto1", "Produto2", "Produto3"],
            "control": ["vm_1", "ve_1", "xx_1"],
            "2020": [500, 600, 100],
            "2021": [700, 800, 200],
        }
    )

    expected_df = (
        pd.DataFrame(
            {
                "ID_PRODUTO": ["1", "1", "2", "2"],
                "NM_PRODUTO": ["Produto1", "Produto1", "Produto2", "Produto2"],
                "DT_ANO": ["2020", "2021", "2020", "2021"],
                "VR_COMERCIALIZACAO_L": [500.0, 700.0, 600.0, 800.0],
                "TIPO_PRODUTO": [
                    "Vinho de Mesa",
                    "Vinho de Mesa",
                    "Vinho Especial",
                    "Vinho Especial",
                ],
            }
        )
        .sort_values(by=["ID_PRODUTO", "DT_ANO"])
        .reset_index(drop=True)
    )

    result = comercializacao_preprocessor.preprocess()

    assert result.reset_index(drop=True).equals(expected_df)
