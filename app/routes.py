import io

from flasgger import Swagger
from flask import Flask, jsonify, render_template, request, send_file
from flask_caching import Cache

from embrapa_api.preprocessing.preprocessors import (
    ComercializacaoPreprocessor,
    ExportacaoPreprocessor,
    ImportacaoPreprocessor,
    ProcessamentoPreprocessor,
    ProducaoPreprocessor,
)

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

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
swagger = Swagger(app, template=swagger_template)


@app.route('/')
def index():
    """Endpoint inicial com opções de navegação."""
    return render_template('index.html')


def generate_csv_response(data, filename):
    output = io.StringIO()
    data.to_csv(output, index=False)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename,
    )


@app.route('/download_producao')
def download_producao():
    """Endpoint para baixar o CSV de Produção.
    ---
    responses:
      200:
        description: CSV de Produção
        content:
          text/csv:
            schema:
              type: string
              format: binary
    """
    preprocessor = ProducaoPreprocessor()
    data = preprocessor.preprocess()
    return generate_csv_response(data, "producao.csv")


@app.route('/download_processamento')
def download_processamento():
    """Endpoint para baixar o CSV de Processamento.
    ---
    responses:
      200:
        description: CSV de Processamento
        content:
          text/csv:
            schema:
              type: string
              format: binary
    """
    preprocessor = ProcessamentoPreprocessor()
    data = preprocessor.preprocess()
    return generate_csv_response(data, "processamento.csv")


@app.route('/download_comercializacao')
def download_comercializacao():
    """Endpoint para baixar o CSV de Comercialização.
    ---
    responses:
      200:
        description: CSV de Comercialização
        content:
          text/csv:
            schema:
              type: string
              format: binary
    """
    preprocessor = ComercializacaoPreprocessor()
    data = preprocessor.preprocess()
    return generate_csv_response(data, "comercializacao.csv")


@app.route('/download_importacao')
def download_importacao():
    """Endpoint para baixar o CSV de Importação.
    ---
    responses:
      200:
        description: CSV de Importação
        content:
          text/csv:
            schema:
              type: string
              format: binary
    """
    preprocessor = ImportacaoPreprocessor()
    data = preprocessor.preprocess()
    return generate_csv_response(data, "importacao.csv")


@app.route('/download_exportacao')
def download_exportacao():
    """Endpoint para baixar o CSV de Exportação.
    ---
    responses:
      200:
        description: CSV de Exportação
        content:
          text/csv:
            schema:
              type: string
              format: binary
    """
    preprocessor = ExportacaoPreprocessor()
    data = preprocessor.preprocess()
    return generate_csv_response(data, "exportacao.csv")


@app.route('/producao')
def producao():
    """Endpoint para a tabela de Produção."""
    preprocessor = ProducaoPreprocessor()
    data = preprocessor.preprocess()
    unique_ids = data['ID_PRODUTO'].unique().tolist()
    return render_template(
        'table.html',
        title="Produção",
        endpoint="get_producao_data",
        unique_ids=unique_ids,
        filter_field="ID_PRODUTO",
    )


@app.route('/processamento')
def processamento():
    """Endpoint para a tabela de Processamento."""
    preprocessor = ProcessamentoPreprocessor()
    data = preprocessor.preprocess()
    unique_ids = data['ID_UVA_PROCESSADA'].unique().tolist()
    return render_template(
        'table.html',
        title="Processamento",
        endpoint="get_processamento_data",
        unique_ids=unique_ids,
        filter_field="ID_UVA_PROCESSADA",
    )


@app.route('/comercializacao')
def comercializacao():
    """Endpoint para a tabela de Comercialização."""
    preprocessor = ComercializacaoPreprocessor()
    data = preprocessor.preprocess()
    unique_ids = data['NM_PRODUTO'].unique().tolist()
    return render_template(
        'table.html',
        title="Comercialização",
        endpoint="get_comercializacao_data",
        unique_ids=unique_ids,
        filter_field="NM_PRODUTO",
    )


@app.route('/importacao')
def importacao():
    """Endpoint para a tabela de Importação."""
    preprocessor = ImportacaoPreprocessor()
    data = preprocessor.preprocess()
    unique_items = data['NM_ITEM'].unique().tolist()
    unique_countries = data['NM_PAIS'].unique().tolist()
    return render_template(
        'table.html',
        title="Importação",
        endpoint="get_importacao_data",
        unique_items=unique_items,
        unique_countries=unique_countries,
        filter_field="NM_ITEM",
    )


@app.route('/exportacao')
def exportacao():
    """Endpoint para a tabela de Exportação."""
    preprocessor = ExportacaoPreprocessor()
    data = preprocessor.preprocess()
    unique_items = data['NM_ITEM'].unique().tolist()
    unique_countries = data['NM_PAIS'].unique().tolist()
    return render_template(
        'table.html',
        title="Exportação",
        endpoint="get_exportacao_data",
        unique_items=unique_items,
        unique_countries=unique_countries,
        filter_field="NM_ITEM",
    )


def apply_pagination(df, start, length):
    return df.iloc[start : start + length]


def apply_filters(df, filters, filter_fields):
    for field in filter_fields:
        if field in filters and filters[field]:
            df = df[df[field] == str(filters[field])]
    return df


@cache.cached(timeout=3600, key_prefix='producao_data')
@app.route('/get_producao_data')
def get_producao_data():
    """Obter dados de Produção.
    ---
    parameters:
      - name: start
        in: query
        type: integer
        required: false
        description: Posição inicial para paginação
      - name: length
        in: query
        type: integer
        required: false
        description: Número de registros a serem retornados
      - name: ID_PRODUTO
        in: query
        type: string
        required: false
        description: Filtro pelo ID do Produto
    responses:
      200:
        description: Lista de registros de Produção
        schema:
          type: array
          items:
            type: object
            properties:
              ID_PRODUTO:
                type: integer
              NM_PRODUTO:
                type: string
              DT_ANO:
                type: string
              VR_PRODUCAO_L:
                type: number
              TIPO_PRODUTO:
                type: string
    """
    preprocessor = ProducaoPreprocessor()
    data = preprocessor.preprocess()
    total_records = len(data)

    # Aplicar filtros
    filters = request.args.to_dict()
    data = apply_filters(data, filters, ["ID_PRODUTO"])
    filtered_records = len(data)

    # Paginação
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    paginated_data = apply_pagination(data, start, length)

    return jsonify(
        {
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": paginated_data.to_dict(orient='records'),
        }
    )


@cache.cached(timeout=3600, key_prefix='processamento_data')
@app.route('/get_processamento_data')
def get_processamento_data():
    """Obter dados de Processamento.
    ---
    parameters:
      - name: start
        in: query
        type: integer
        required: false
        description: Posição inicial para paginação
      - name: length
        in: query
        type: integer
        required: false
        description: Número de registros a serem retornados
      - name: ID_UVA_PROCESSADA
        in: query
        type: string
        required: false
        description: Filtro pelo ID da Uva Processada
    responses:
      200:
        description: Lista de registros de Processamento
        schema:
          type: array
          items:
            type: object
            properties:
              ID_UVA_PROCESSADA:
                type: string
              NM_UVA:
                type: string
              DT_ANO:
                type: string
              QT_UVAS_PROCESSADAS_KG:
                type: number
              CD_TIPO_VINHO:
                type: string
              CD_TIPO_UVA:
                type: string
    """
    preprocessor = ProcessamentoPreprocessor()
    data = preprocessor.preprocess()
    total_records = len(data)

    # Aplicar filtros
    filters = request.args.to_dict()
    data = apply_filters(data, filters, ["ID_UVA_PROCESSADA"])
    filtered_records = len(data)

    # Paginação
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    paginated_data = apply_pagination(data, start, length)

    return jsonify(
        {
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": paginated_data.to_dict(orient='records'),
        }
    )


@cache.cached(timeout=3600, key_prefix='comercializacao_data')
@app.route('/get_comercializacao_data')
def get_comercializacao_data():
    """Obter dados de Comercialização.
    ---
    parameters:
      - name: start
        in: query
        type: integer
        required: false
        description: Posição inicial para paginação
      - name: length
        in: query
        type: integer
        required: false
        description: Número de registros a serem retornados
      - name: NM_PRODUTO
        in: query
        type: string
        required: false
        description: Filtro pelo Nome do Produto
    responses:
      200:
        description: Lista de registros de Comercialização
        schema:
          type: array
          items:
            type: object
            properties:
              ID_PRODUTO:
                type: integer
              NM_PRODUTO:
                type: string
              DT_ANO:
                type: string
              VR_COMERCIALIZACAO_L:
                type: number
              TIPO_PRODUTO:
                type: string
    """
    preprocessor = ComercializacaoPreprocessor()
    data = preprocessor.preprocess()
    total_records = len(data)

    # Aplicar filtros
    filters = request.args.to_dict()
    data = apply_filters(data, filters, ["NM_PRODUTO"])
    filtered_records = len(data)

    # Paginação
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    paginated_data = apply_pagination(data, start, length)

    return jsonify(
        {
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": paginated_data.to_dict(orient='records'),
        }
    )


@cache.cached(timeout=3600, key_prefix='importacao_data')
@app.route('/get_importacao_data')
def get_importacao_data():
    """Obter dados de Importação.
    ---
    parameters:
      - name: start
        in: query
        type: integer
        required: false
        description: Posição inicial para paginação
      - name: length
        in: query
        type: integer
        required: false
        description: Número de registros a serem retornados
      - name: NM_ITEM
        in: query
        type: string
        required: false
        description: Filtro pelo Nome do Item
      - name: NM_PAIS
        in: query
        type: string
        required: false
        description: Filtro pelo Nome do País
    responses:
      200:
        description: Lista de registros de Importação
        schema:
          type: array
          items:
            type: object
            properties:
              NM_PAIS:
                type: string
              DT_ANO:
                type: string
              NM_ITEM:
                type: string
              QTD_IMPORTADO_KG:
                type: number
              VL_VALOR_IMPORTADO_USD:
                type: number
    """
    preprocessor = ImportacaoPreprocessor()
    data = preprocessor.preprocess()
    total_records = len(data)

    # Aplicar filtros
    filters = request.args.to_dict()
    data = apply_filters(data, filters, ["NM_ITEM", "NM_PAIS"])
    filtered_records = len(data)

    # Paginação
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    paginated_data = apply_pagination(data, start, length)

    return jsonify(
        {
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": paginated_data.to_dict(orient='records'),
        }
    )


@cache.cached(timeout=3600, key_prefix='exportacao_data')
@app.route('/get_exportacao_data')
def get_exportacao_data():
    """Obter dados de Exportação.
    ---
    parameters:
      - name: start
        in: query
        type: integer
        required: false
        description: Posição inicial para paginação
      - name: length
        in: query
        type: integer
        required: false
        description: Número de registros a serem retornados
      - name: NM_ITEM
        in: query
        type: string
        required: false
        description: Filtro pelo Nome do Item
      - name: NM_PAIS
        in: query
        type: string
        required: false
        description: Filtro pelo Nome do País
    responses:
      200:
        description: Lista de registros de Exportação
        schema:
          type: array
          items:
            type: object
            properties:
              NM_PAIS:
                type: string
              DT_ANO:
                type: string
              NM_ITEM:
                type: string
              QTD_EXPORTADO_KG:
                type: number
              VL_VALOR_EXPORTADO_USD:
                type: number
    """
    preprocessor = ExportacaoPreprocessor()
    data = preprocessor.preprocess()
    total_records = len(data)

    # Aplicar filtros
    filters = request.args.to_dict()
    data = apply_filters(data, filters, ["NM_ITEM", "NM_PAIS"])
    filtered_records = len(data)

    # Paginação
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    paginated_data = apply_pagination(data, start, length)

    return jsonify(
        {
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": paginated_data.to_dict(orient='records'),
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
