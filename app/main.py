import requests
import datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request, make_response
from functools import wraps
import jwt

from app.tables import extract_table
from app.urls import get_url_for_option, map_urls

# Fazendo a segurança do nosso ambiente
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
#TO_DO: switch para leitura local ou via scraper
#TO_DO: logger informando a alteração
#TO_DO: autenticação JWT

# Essa será a chave para codificar e decodificar o JWT
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_padrao_secreta')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://localhost:5000/route?token=xxx

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is only available for people with valid tokens.'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({
            'user': auth.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route("/")
def index():
    # Definindo a url da Homepage
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"

    # Mapeando todas as urls possíveis
    url_dict = map_urls(base_url)

    # Pegando uma url de exemplo
    url = get_url_for_option(url_dict, option=6, year=2008, suboption=4)

    response = requests.get(url)

    # Extrair o conteúdo HTML da resposta
    html_content = response.text

    # Parsear o conteúdo HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extrair a tabela
    main_table = extract_table(soup)

    return render_template("index.html", table_data=main_table)


if __name__ == "__main__":
    app.run(debug=True)
