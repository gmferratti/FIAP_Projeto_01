from unittest.mock import patch

import pandas as pd
import pytest

from embrapa_api.preprocessing.preprocessors import ExportacaoPreprocessor


@pytest.fixture
def exportacao_preprocessor(app_context):
    """Fixture para criar uma instância da
    classe ExportacaoPreprocessor dentro do contexto da aplicação."""
    processor = ExportacaoPreprocessor()
    processor.exportacao_paths = {
        'Vinhos': {'url': 'fake_url_vinhos', 'path': 'fake_path_vinhos'},
        'Sucos': {'url': 'fake_url_sucos', 'path': 'fake_path_sucos'},
    }
    return processor


def test_load_data_success(exportacao_preprocessor):
    """
    Testa o carregamento bem-sucedido dos dados de uma URL específica.
    Verifica se o read_csv é chamado corretamente com a URL e se os
    dados carregados são como esperado.
    """
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

        assert not result.empty
        assert result.equals(mock_data)


def test_load_data_failure_no_config(exportacao_preprocessor):
    """
    Testa se o método load_data levanta um ValueError quando
    nenhum caminho está configurado para o tipo de produto especificado.
    """
    with pytest.raises(ValueError):
        exportacao_preprocessor.load_data("Inexistente")


def test_process_export_data(exportacao_preprocessor):
    """
    Testa o processamento dos dados de exportação, garantindo
    que os dados sejam transformados corretamente conforme esperado.
    """
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
    """
    Testa a integração do método preprocess com os submétodos de processamento
    de cada tipo de produto de exportação. Verifica se a concatenação final dos
    DataFrames processados de diferentes tipos de produtos é feita corretamente.
    """
    # Ajusta o efeito colateral do mock para garantir que cubra todas
    # as chamadas esperadas
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

        # Verifica se cada valor retornado do mock é usado corretamente
        assert mock_method.call_count == len(side_effects)
        assert not result.empty
        assert result.shape[0] == 2  # Esperando duas entradas
        assert set(result["NM_PAIS"]) == {"Brasil", "França"}
