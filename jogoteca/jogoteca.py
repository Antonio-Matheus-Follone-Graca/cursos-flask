# importando flask
from flask import Flask, render_template 
 

app = Flask(__name__)

# criando uma rota 
# ao  acessar /inicio na url a função retorna o seguinte código
@app.route('/inicio')
# funcao para a rota
def ola():
    # renderizando página html da pasta template com o render_template
    return render_template('lista.html', titulo= 'Jogos') # passando variável para o lista.html

# rodando aplicação
app.run()