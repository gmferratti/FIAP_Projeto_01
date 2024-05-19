import pytest
from unittest.mock import patch
import pandas as pd

from embrapa_api.preprocessing.preprocessors import ExportacaoPreprocessor


@pytest.fixture
def exportacao_preprocessor():
    """Fixture for creating an instance of ExportacaoPreprocessor."""
    processor = ExportacaoPreprocessor()
    processor.exportacao_paths = {
        'Vinhos': {'url': 'fake_url_vinhos', 'path': 'fake_path_vinhos'},
        'Sucos': {'url': 'fake_url_sucos', 'path': 'fake_path_sucos'},
    }
    return processor


def test_load_data_success(exportacao_preprocessor):
    """Test successful data loading from a specified URL."""
    produto_exportacao = "Vinhos"
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
        result = exportacao_preprocessor.load_data(produto_exportacao)

        mock_read_csv.assert_called_once_with(
            exportacao_preprocessor.exportacao_paths[produto_exportacao]["url"], sep=';'
        )
        assert not result.empty
        assert result.equals(mock_data)


def test_load_data_failure_no_config(exportacao_preprocessor):
    """Test that loading data raises a ValueError when no path is configured."""
    with pytest.raises(ValueError):
        exportacao_preprocessor.load_data("Inexistente")


def test_process_export_data(exportacao_preprocessor):
    """Test processing of export data."""
    produto_exportacao = "Vinhos"
    sample_data = pd.DataFrame(
        {"Id": [1], "País": ["Brasil"], "2020.1": [1000], "2020": [100]}
    )
    expected_output = pd.DataFrame(
        {
            "NM_PAIS": ["Brasil"],
            "DT_ANO": ["2020"],
            "NM_ITEM": ["Vinhos"],
            "QTD_EXPORTADO_KG": [100],
            "VL_VALOR_EXPORTADO_USD": [1000],
        }
    ).sort_values(['NM_PAIS', 'DT_ANO'])

    with patch.object(exportacao_preprocessor, 'load_data', return_value=sample_data):
        result = exportacao_preprocessor._processa_exportacao(produto_exportacao)
        assert result.reset_index(drop=True).equals(expected_output)


def test_preprocess_integration(exportacao_preprocessor):
    """Test the integration of the preprocess method."""
    # Adjust mock side_effect to ensure it covers all expected calls
    side_effects = [
        pd.DataFrame(
            {
                "NM_PAIS": ["Brasil"],
                "DT_ANO": ["2020"],
                "NM_ITEM": ["Vinhos"],
                "QTD_EXPORTADO_KG": [100],
                "VL_VALOR_EXPORTADO_USD": [1000],
            }
        ),
        pd.DataFrame(
            {
                "NM_PAIS": ["França"],
                "DT_ANO": ["2020"],
                "NM_ITEM": ["Sucos"],
                "QTD_EXPORTADO_KG": [200],
                "VL_VALOR_EXPORTADO_USD": [1200],
            }
        ),
    ]

    with patch.object(
        exportacao_preprocessor, '_processa_exportacao', side_effect=side_effects
    ) as mock_method:
        result = exportacao_preprocessor.preprocess()

        # Make sure that each mocked return value is used correctly
        assert mock_method.call_count == len(side_effects)
        assert not result.empty
        assert result.shape[0] == 2  # Expecting two entries
        assert set(result["NM_PAIS"]) == {"Brasil", "França"}
