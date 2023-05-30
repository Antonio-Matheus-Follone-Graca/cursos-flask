# importando flask
from flask import Flask, render_template, request, redirect, session,flash

 
 # criando classe
class Jogo:
    def __init__(self,nome,categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


#
jogo1= Jogo('Tetris','Puzzle','Atati')
jogo2= Jogo('God of war','Hack n slash','Ps2')
jogo3= Jogo('Mortal Kombat','Luta','Ps2')
lista = [jogo1,jogo2,jogo3]

app = Flask(__name__)
app.secret_key= 'alura'

# criando uma rota 
# ao  acessar /inicio na url a função retorna o seguinte código
# rota index
@app.route('/')
# funcao para a rota
def index():
    # renderizando página html da pasta template com o render_template
    return render_template('lista.html', titulo= 'Jogos',  jogos=lista) # passando variável para o lista.html

# rota para página de  cadastro
@app.route('/novo')
def novo():
    return render_template('novo.html', titulo = 'Novo jogo')



# rota que faz o cadastro e permitindo método post, por padrão o método é get
@app.route('/criar', methods=['POST',])
def criar():
    # request pega as informações de um formulário 
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    # passando para objeto
    jogo= Jogo(nome,categoria,console)
    # passando para a lista de array
    lista.append(jogo)
    # redirecionando para a rota index
    return redirect('/')
    
# rota para página de login
@app.route('/login')
def login():
        return render_template('login.html')     
# rodando aplicação e ativando debug para a apliacação ficar se atualizando toda hora    

# rota que faz o logar 

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if 'alohomora' == request.form['senha']:
        # iniciando sessão
        session['usuario_logado'] = request.form['usuario']
        # mandando mensagem 
        flash(f'{session["usuario_logado"]} logado com sucesso!')
        return redirect('/')
    else:
        flash('Usuário não logado')
        return redirect('/login')
    

# rota para deslogar
@app.route('/logout')
def logout():
    # deixando o session vazio o usuário é deslogado
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    # redirecionando 
    return redirect('/')
app.run(debug=True)
        