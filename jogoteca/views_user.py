from jogoteca import app
from flask import  render_template, request, redirect, session,flash, url_for
from flask_bcrypt import check_password_hash
from models import  Usuarios # models 
from helpers import  FormularioUsuario
# rota para página de login
@app.route('/login')
def login():
    # pegando a página que o usuário tentou acessar atráves da url, pois caso esteja deslogado e tente acessar o site o mandara para a página de login
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima = proxima, form = form)     
# rodando aplicação e ativando debug para a apliacação ficar se atualizando toda hora    



# rota que faz o logar 

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    # select de usuarios pelo nick
    usuario = Usuarios.query.filter_by(nickname = form.nickname.data).first()
    # chegando a senha criptografada do registro no banco do usuário com a senha informada no formulário
    senha = check_password_hash(usuario.senha,form.senha.data)
    # se o nick  digitado pelo usuário existe e a comparação de senha retorna true 
    if usuario and senha:
        # acessando campo senha 
        # salvando nickname na session para logar o usuário
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
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