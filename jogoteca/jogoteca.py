# importando flask
from flask import Flask, render_template, request, redirect, session,flash, url_for
# importando sql alchemy para mexer no banco de dados
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key= 'alura'

# variavel para conexão com banco de dados, parametro a aplicação que está rodando
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'jogoteca'   
    )
    
db=SQLAlchemy(app)
    


# preparando tabelas para o sqlalchemy
class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    
    

# criando uma rota 
# ao  acessar /inicio na url a função retorna o seguinte código
# rota index
@app.route('/')
# funcao para a rota
def index():
    # fazendo select da tabela de jogos
    lista = Jogos.query.order_by(Jogos.id)
    # renderizando página html da pasta template com o render_template
    return render_template('lista.html', titulo= 'Jogos',  jogos=lista) # passando variável para o lista.html

# rota para página de  cadastro
@app.route('/novo')
def novo():
    # se não houver usuário logado na sessão. Senão existir session["usuario_logado"]
    # se usuario_logado for igual a None
    if 'usuario_logado' not in session or session["usuario_logado"] == None :
        # passando a url da página que o usuário tentou acessar
        return redirect(url_for('login',proxima = url_for('novo')))
    
    return render_template('novo.html', titulo = 'Novo jogo')



# rota que faz o cadastro e permitindo método post, por padrão o método é get
@app.route('/criar', methods=['POST',])
def criar():
    # request pega as informações de um formulário 
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    # select da tabela Jogos
    jogo = Jogos.query.filter_by(nome = nome).first()
    
    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('index'))
    
    # cadastrando jogo novo
    novo_jogo = Jogos(nome = nome, categoria = categoria, console = console)
    # insert 
    db.session.add(novo_jogo)
    db.session.commit()
    
    return redirect(url_for('index'))
    
# rota para página de login
@app.route('/login')
def login():
    # pegando a página que o usuário tentou acessar atráves da url, pois caso esteja deslogado e tente acessar o site o mandara para a página de login
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)     
# rodando aplicação e ativando debug para a apliacação ficar se atualizando toda hora    

# rota que faz o logar 

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    # select de usuarios pelo nick
    usuario = Usuarios.query.filter_by(nickname = request.form['usuario']).first()
    # se o nick  digitado pelo usuário existe 
    if usuario:
        # acessando campo senha 
        if request.form['senha'] == usuario.senha:
            # salvando nickname na session para logar o usuário
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))
    
    if 'alohomora' == request.form['senha']:
        # iniciando sessão
        session['usuario_logado'] = request.form['usuario']
        # mandando mensagem 
        flash(f'{session["usuario_logado"]} logado com sucesso!')
        proxima_pagina = request.form['proxima']
        
        # quando o usuário logar, manda ele para a página que ele estava tentanto acessar enquanto estava deslogado
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado')
        # usando url for para procurar a rota. Nesse caso atráves da função
        return redirect(url_for('login'))
    

# rota para deslogar
@app.route('/logout')
def logout():
    # deixando o session vazio o usuário é deslogado
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    # redirecionando 
    # usando url for para procurar a rota. Nesse caso atráves da função
    return redirect(url_for('index'))

app.run(debug=True)
        