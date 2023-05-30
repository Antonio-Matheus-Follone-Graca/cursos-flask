# importando flask
from flask import Flask

app = Flask(__name__)

# criando uma rota 

@app.route('/inicio')
# funcao para a rota
def ola():
    return '<h1> Olá mundo </h1>'

# rodando aplicação
app.run()