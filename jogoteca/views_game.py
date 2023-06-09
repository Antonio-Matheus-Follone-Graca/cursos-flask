from flask import  render_template, request, redirect, session,flash, url_for, send_from_directory
# importando aplicação do projeto e banco do jogoteca.py
from jogoteca import app, db
from models import Jogos, Usuarios # models 

# importando função de recuperar imagem que está no arquivo helpers.py
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo, FormularioUsuario
import  time
# arquivo aonde ficam as rotas e  criando uma  index 
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
    
    # chamando formulário do helpers.py e mandando para a página novo.html
    form = FormularioJogo()
    return render_template('novo.html', titulo = 'Novo jogo',form = form)

# rota para editar com o parametro id
@app.route('/editar/<int:id>')
def editar(id):
    # se não houver usuário logado na sessão. Senão existir session["usuario_logado"]
    # se usuario_logado for igual a None
    if 'usuario_logado' not in session or session["usuario_logado"] == None :
        # passando a url da página que o usuário tentou acessar
        return redirect(url_for('login',proxima = url_for('editar')))
    # select de acordo com o id
    jogo = Jogos.query.filter_by(id= id).first()
    # chamando formulário do flask do helpers.py
    form = FormularioJogo()
    # setando valores nos campos do form de acordo com os valores do select
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    # recuperando capa do jogo
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo = 'Editando jogo', jogo =id ,capa_jogo= capa_jogo, form = form )

# rota de atualizar 
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        # select pelo id recebido via formulário
        jogo = Jogos.query.filter_by(id = request.form['id']).first()
        # atualizando campos
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        db.session.add(jogo)
        db.session.commit()
        # mudando arquivo da imagem
        arquivo = request.files['arquivo']
        # caminho da imagem
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        # função de deletar arquivo duplicado, do arquivo helpers.py
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
        

    return redirect(url_for('index'))

# rota para deletar
@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session["usuario_logado"] == None :
        return redirect(url_for('login'))
    # deletando pelo id
    Jogos.query.filter_by(id = id).delete()
    db.session.commit()
    flash('jogo deletado com sucesso')
    return  redirect(url_for('index'))
    
   
# rota que faz o cadastro e permitindo método post, por padrão o método é get
@app.route('/criar', methods=['POST',])
def criar():
    # pegando o flask forms do novo.html
    form = FormularioJogo(request.form)
    # se o formulário não estiver validado
    if not  form.validate_on_submit():
        return redirect(url_for('novo'))
        
    # request pega as informações do formulário 
    nome = form.nome.data
    categoria =  form.categoria.data
    console = form.console.data
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
    # recebendo informações do campo de imagem
    arquivo = request.files['arquivo']
    # caminho da pasta uploads, variável UPLOAD_PATH está no arquivo config.gs
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    # upando imagem para a pasta uploads e nomeando arquivo da imagem 
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))
    


    
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    # procurando arquivo capa_padrao.png com o módulo  send_from_directory
    return send_from_directory('uploads',nome_arquivo)
    
# rota para caso o usuário digite um rota inexistente
@app.errorhandler(404)
def page_not_found(error):
    return render_template('erro.html')


