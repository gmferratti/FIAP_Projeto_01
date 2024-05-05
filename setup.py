from setuptools import find_packages, setup

setup(
    name='FIAP_Projeto_01',
    author='',
    description='',
    version='0.1.0',
    packages=find_packages(include=['embrapa_api', 'embrapa_api.*', 'app', 'app.*']),
)
