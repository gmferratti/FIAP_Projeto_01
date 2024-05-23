import io

from flask import Blueprint, jsonify, render_template, request, send_file

from app import cache
from embrapa_api.preprocessing.preprocessors import (
    ComercializacaoPreprocessor,
    ExportacaoPreprocessor,
    ImportacaoPreprocessor,
    ProcessamentoPreprocessor,
    ProducaoPreprocessor,
)

bp = Blueprint('main', __name__)


@bp.route('/')
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


@bp.route('/download_producao')
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


@bp.route('/download_processamento')
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


@bp.route('/download_comercializacao')
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


@bp.route('/download_importacao')
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


@bp.route('/download_exportacao')
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


@bp.route('/producao')
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


@bp.route('/processamento')
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


@bp.route('/comercializacao')
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


@bp.route('/importacao')
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


@bp.route('/exportacao')
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


@bp.route('/get_producao_data')
@cache.cached(timeout=3600, key_prefix='producao_data')
def get_producao_data():
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


@bp.route('/get_processamento_data')
@cache.cached(timeout=3600, key_prefix='processamento_data')
def get_processamento_data():
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


@bp.route('/get_comercializacao_data')
@cache.cached(timeout=3600, key_prefix='comercializacao_data')
def get_comercializacao_data():
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


@bp.route('/get_importacao_data')
@cache.cached(timeout=3600, key_prefix='importacao_data')
def get_importacao_data():
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


@bp.route('/get_exportacao_data')
@cache.cached(timeout=3600, key_prefix='exportacao_data')
def get_exportacao_data():
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
