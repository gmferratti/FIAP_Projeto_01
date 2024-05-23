from flasgger import Swagger
from flask import Flask
from flask_caching import Cache

cache = Cache()


def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.update(config)

    cache_config = {'CACHE_TYPE': 'flask_caching.backends.simplecache.SimpleCache'}
    cache.init_app(app, config=cache_config)

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Embrapa Wine Data API",
            "description": """
            API para consultar e baixar dados de produção, processamento,
             comercialização, importação e exportação de vinhos.
            """,
            "version": "1.0.0",
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http"],
    }
    _ = Swagger(app, template=swagger_template)

    with app.app_context():
        from app.routes import bp

        app.register_blueprint(bp)

    return app
