import pytest

from app import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app({'TESTING': True, 'USE_LOCAL_DATA': True})
    yield app


@pytest.fixture(scope='module')
def app_context(app):
    with app.app_context():
        yield
