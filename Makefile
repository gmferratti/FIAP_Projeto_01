.PHONY: create_env install install_dev clean lint test run

# Nome fixo para o ambiente virtual
VENV_NAME=fiap

# Comando para criar o ambiente virtual usando Conda
create_env:
	conda create --name $(VENV_NAME) python=3.10 -y
	

# Usar comando 'conda activate fiap' manualmente

# Comando para instalar dependências de produção
install:
	pip install -r requirements.txt

# Comando para instalar dependências de desenvolvimento
install-dev:
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	flake8 .
	black --check .
	isort --check .

lint-all:
	black . && \
	flake8 && \
	isort .

run:
	python run.py
