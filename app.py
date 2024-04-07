from flask import Flask, render_template
from bs4 import BeautifulSoup
from urls import map_urls, get_url_for_option
from tables import extract_table

import requests

app = Flask(__name__)

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

