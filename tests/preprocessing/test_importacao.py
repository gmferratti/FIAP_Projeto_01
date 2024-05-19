import pytest
from unittest.mock import patch
import pandas as pd

from embrapa_api.preprocessing.preprocessors import ImportacaoPreprocessor


@pytest.fixture
def importacao_preprocessor():
    """Fixture para criar uma instância da classe ImportacaoPreprocessor."""
    return ImportacaoPreprocessor()


def test_load_data_success(importacao_preprocessor):
    """
    Testa se o método load_data carrega os dados com sucesso de uma URL especificada.
    Verifica se os dados são corretamente carregados e se a função read_csv é chamada
    com a URL correta.
    """
    produto_importacao = "Vinhos"
    with patch("pandas.read_csv") as mock_read_csv, patch.dict(
        "embrapa_api.preprocessing.preprocessors.IMPORTACAO_PATHS",
        {produto_importacao: {"url": "fake_url", "path": "fake_path"}},
    ):
        mock_data = pd.DataFrame(
            {
                "Id": [1, 2],
                "País": ["Brasil", "França"],
                "2020.1": [1000, 2000],
                "2021.1": [1100, 2100],
                "2020": [500, 600],
                "2021": [550, 650],
            }
        )
        mock_read_csv.return_value = mock_data

        result = importacao_preprocessor.load_data(produto_importacao)

        assert not result.empty
        assert result.equals(mock_data)
        mock_read_csv.assert_called_once_with("fake_url", sep=';')


def test_processa_importacao(importacao_preprocessor):
    """
    Testa o processamento específico dos dados de importação,
    garantindo que as transformações e o mapeamento estejam corretos.
    """
    produto_importacao = "Vinhos"
    data = pd.DataFrame(
        {
            "Id": [1, 2],
            "País": ["Brasil", "França"],
            "2020.1": [1000, 2000],
            "2021.1": [1100, 2100],
            "2020": [500, 600],
            "2021": [550, 650],
        }
    )
    expected_output = (
        pd.DataFrame(
            {
                "NM_PAIS": ["Brasil", "Brasil", "França", "França"],
                "DT_ANO": ["2020", "2021", "2020", "2021"],
                "NM_ITEM": ["Vinhos", "Vinhos", "Vinhos", "Vinhos"],
                "QTD_IMPORTADO_KG": [500, 550, 600, 650],
                "VL_VALOR_IMPORTADO_USD": [1000, 1100, 2000, 2100],
            }
        )
        .sort_values(["NM_PAIS", "DT_ANO"])
        .reset_index(drop=True)
    )

    result = importacao_preprocessor._processa_importacao(data, produto_importacao)

    assert result.reset_index(drop=True).equals(expected_output)


def test_preprocess_integration(importacao_preprocessor):
    """
    Testa a integração do método preprocess, verificando se a concatenação final
    dos DataFrames processados de diferentes tipos de importação é feita corretamente.
    """
    with patch.object(
        importacao_preprocessor,
        'processa_vinhos',
        return_value=pd.DataFrame(
            {'NM_PAIS': ['Brasil'], 'DT_ANO': ['2020'], 'NM_ITEM': ['Vinhos']}
        ),
    ), patch.object(
        importacao_preprocessor,
        'processa_sucos',
        return_value=pd.DataFrame(
            {'NM_PAIS': ['França'], 'DT_ANO': ['2020'], 'NM_ITEM': ['Sucos']}
        ),
    ), patch.object(
        importacao_preprocessor,
        'processa_espumantes',
        return_value=pd.DataFrame(
            {'NM_PAIS': ['Itália'], 'DT_ANO': ['2020'], 'NM_ITEM': ['Espumantes']}
        ),
    ), patch.object(
        importacao_preprocessor,
        'processa_frescas',
        return_value=pd.DataFrame(
            {'NM_PAIS': ['Chile'], 'DT_ANO': ['2020'], 'NM_ITEM': ['Frescas']}
        ),
    ), patch.object(
        importacao_preprocessor,
        'processa_passas',
        return_value=pd.DataFrame(
            {'NM_PAIS': ['Argentina'], 'DT_ANO': ['2020'], 'NM_ITEM': ['Passas']}
        ),
    ):
        result = importacao_preprocessor.preprocess()

        assert not result.empty
        assert result.shape == (5, 3)
        assert set(result["NM_PAIS"].to_list()) == set([
            "Brasil", "França", "Itália", "Chile", "Argentina"
        ])
