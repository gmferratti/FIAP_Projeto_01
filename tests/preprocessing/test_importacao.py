import pytest
from unittest.mock import patch
import pandas as pd

from embrapa_api.preprocessing.preprocessors import ImportacaoPreprocessor


@pytest.fixture
def importacao_preprocessor():
    """Fixture for creating an instance of ImportacaoPreprocessor."""
    return ImportacaoPreprocessor()


def test_load_data_success(importacao_preprocessor):
    """Test successful data loading from a specified URL."""
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

        mock_read_csv.assert_called_once_with("fake_url", sep=';')
        assert not result.empty
        assert result.equals(mock_data)


def test_load_data_failure(importacao_preprocessor):
    """Test that loading data raises a ValueError when no path is configured."""
    with pytest.raises(ValueError):
        importacao_preprocessor.load_data("Inexistente")


def test_process_import_data(importacao_preprocessor):
    """Test processing of import data."""
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
    """Test the integration of the preprocess method."""
    product_types = importacao_preprocessor.importacao_paths.keys()

    # Create a side_effect list that provides a DataFrame for each product type
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

        # Assert that the number of entries is correct
        assert len(result) == len(side_effects)
        # Assert that all product types are represented in the results
        assert set(result["NM_ITEM"]) == set(product_types)
