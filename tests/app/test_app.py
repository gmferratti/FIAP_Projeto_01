import pytest

from app import create_app


# Configuração do aplicativo Flask para testes
@pytest.fixture
def app():
    app = create_app(
        {
            'TESTING': True,
            'USE_LOCAL_DATA': True,
            'CACHE_TYPE': 'simple',
        }
    )
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# Testes para os endpoints
def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert "Opções de Navegação" in rv.data.decode('utf-8')


def test_download_producao(client):
    rv = client.get('/download_producao')
    assert rv.status_code == 200
    assert rv.mimetype == 'text/csv'
    assert "attachment; filename=producao.csv" in rv.headers['Content-Disposition']


def test_download_processamento(client):
    rv = client.get('/download_processamento')
    assert rv.status_code == 200
    assert rv.mimetype == 'text/csv'
    assert "attachment; filename=processamento.csv" in rv.headers['Content-Disposition']


def test_download_comercializacao(client):
    rv = client.get('/download_comercializacao')
    assert rv.status_code == 200
    assert rv.mimetype == 'text/csv'
    assert (
        "attachment; filename=comercializacao.csv" in rv.headers['Content-Disposition']
    )


def test_download_importacao(client):
    rv = client.get('/download_importacao')
    assert rv.status_code == 200
    assert rv.mimetype == 'text/csv'
    assert "attachment; filename=importacao.csv" in rv.headers['Content-Disposition']


def test_download_exportacao(client):
    rv = client.get('/download_exportacao')
    assert rv.status_code == 200
    assert rv.mimetype == 'text/csv'
    assert "attachment; filename=exportacao.csv" in rv.headers['Content-Disposition']
