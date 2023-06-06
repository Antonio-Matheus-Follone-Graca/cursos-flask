# importando flask e  importando sql alchemy para mexer no banco de dados
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
app = Flask(__name__)
# puxando configurações do arquivo config.py e  iniciando conexão com o banco de dados
app.config.from_pyfile('config.py')  
db=SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)



# importando todas as rotas. Deve ficar em baixo da iniciação do banco(linha 9)
from views_game import * 
from views_user import *
if __name__ == '__main__':
    # rodando aplicação
    app.run(debug=True)
    

        