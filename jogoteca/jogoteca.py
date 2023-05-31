# importando flask
from flask import Flask
# importando sql alchemy para mexer no banco de dados
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# puxando configurações do arquivo config.py
app.config.from_pyfile('config.py')
# iniciando conexão com o banco de dados    
db=SQLAlchemy(app)

# importando todas as rotas. Deve ficar em baixo da iniciação do banco(linha 9)
from views import * 
if __name__ == '__main__':
    # rodando aplicação
    app.run(debug=True)
    

        