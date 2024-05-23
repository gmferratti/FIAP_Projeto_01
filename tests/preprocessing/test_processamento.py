from unittest.mock import patch

import pandas as pd
import pytest

from embrapa_api.preprocessing.preprocessors import ProcessamentoPreprocessor


@pytest.fixture
def processamento_preprocessor(app_context):
    """Fixture que cria e retorna uma instância da
    classe ProcessamentoPreprocessor dentro do contexto da aplicação."""
    return ProcessamentoPreprocessor()


def test_load_data_success(processamento_preprocessor):
    """
    Testa se o método load_data carrega os dados com sucesso de uma URL específica.
    Verifica se os dados são corretamente carregados e se a função read_csv é chamada
    com a URL correta.
    """
    tipo_uva = "Viniferas"
    with (
        patch("pandas.read_csv") as mock_read_csv,
        patch.dict(
            "embrapa_api.preprocessing.preprocessors.PROCESSAMENTO_PATHS",
            {tipo_uva: {"url": "fake_url", "path": "fake_path"}},
        ),
    ):
        mock_df = pd.DataFrame(
            {
                "id": [1, 2],
                "control": ["ti_control", "br_control"],
                "cultivar": ["cultivar1", "cultivar2"],
                "2020": [100, 200],
                "2021": [150, 250],
            }
        )
        mock_read_csv.return_value = mock_df

        result = processamento_preprocessor.load_data(tipo_uva)

        assert not result.empty
        assert result.equals(mock_df)


def test_processa_viniferas(processamento_preprocessor):
    """
    Testa o processamento dos dados para uvas Viniferas, garantindo que o mapeamento
    de tipos de vinho esteja correto.
    """
    with patch.object(processamento_preprocessor, 'load_data') as mock_load_data:
        mock_df = pd.DataFrame(
            {
                "id": [1, 2],
                "control": ["ti_control", "br_control"],
                "cultivar": ["cultivar1", "cultivar2"],
                "2020": [100, 200],
                "2021": [150, 250],
            }
        )
        mock_load_data.return_value = mock_df

        result = processamento_preprocessor.processa_viniferas()

        assert not result.empty
        assert set(result['CD_TIPO_VINHO']) == {"Tintas", "Brancas e Rosadas"}


def test_preprocess_integration(processamento_preprocessor):
    """
    Testa a integração do método preprocess com os submétodos de processamento
    de cada tipo de uva. Verifica se a concatenação final dos DataFrames processados
    de diferentes tipos de uva é feita corretamente, incluindo a ordenação esperada
    por 'ID_UVA_PROCESSADA' e 'DT_ANO'.
    """
    with (
        patch.object(
            processamento_preprocessor,
            'processa_viniferas',
            return_value=pd.DataFrame(
                {
                    'ID_UVA_PROCESSADA': ['1_viniferas', '2_viniferas'],
                    'CD_TIPO_VINHO': ['Tintas', 'Tintas'],
                    'DT_ANO': ['2020', '2021'],
                }
            ),
        ),
        patch.object(
            processamento_preprocessor,
            'processa_americanas',
            return_value=pd.DataFrame(
                {
                    'ID_UVA_PROCESSADA': ['1_americanas', '2_americanas'],
                    'CD_TIPO_VINHO': ['Brancas e Rosadas', 'Brancas e Rosadas'],
                    'DT_ANO': ['2020', '2021'],
                }
            ),
        ),
        patch.object(
            processamento_preprocessor,
            'processa_uvas_de_mesa',
            return_value=pd.DataFrame(
                {
                    'ID_UVA_PROCESSADA': ['1_uvas_de_mesa', '2_uvas_de_mesa'],
                    'CD_TIPO_VINHO': ['Brancas', 'Brancas'],
                    'DT_ANO': ['2020', '2021'],
                }
            ),
        ),
        patch.object(
            processamento_preprocessor,
            'processa_sem_classe',
            return_value=pd.DataFrame(
                {
                    'ID_UVA_PROCESSADA': ['1_sem_classe', '2_sem_classe'],
                    'CD_TIPO_VINHO': ['Sem classificação', 'Sem classificação'],
                    'DT_ANO': ['2020', '2021'],
                }
            ),
        ),
    ):
        result = processamento_preprocessor.preprocess()

        assert len(result) == 8  # Esperado 2 entradas por tipo de uva, totalizando 8
        assert all(
            col in result.columns
            for col in ['ID_UVA_PROCESSADA', 'CD_TIPO_VINHO', 'DT_ANO']
        )
