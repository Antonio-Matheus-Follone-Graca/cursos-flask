import os
from jogoteca import app 
# importando flask forms
from flask_wtf import FlaskForm
from wtforms import StringField,validators, SubmitField, PasswordField
 

# classe do formulário
class FormularioJogo(FlaskForm):
    # cada atributo é um campo do formulário
    nome = StringField('Nome do jogo',[validators.DataRequired(),validators.Length(min =1, max=50)])
    categoria = StringField('Categoria',[validators.DataRequired(),validators.Length(min =1, max=40)])
    console = StringField('Console', [validators.DataRequired(),validators.Length(min =1, max=20)])
    # botão de submit
    salvar = SubmitField('Salvar')

# formulario do usuário 
class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname',[validators.DataRequired(),validators.Length(min =1, max=8)])
    senha = PasswordField('Senha',[validators.DataRequired(),validators.Length(min =1, max=100)])
    # botão de submit
    login = SubmitField('Login')

# função para recuperar imagem do jogo
def recupera_imagem(id):
    # for que percorre todos os arquivios da pasta upload
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        # se encontrou o capaid.jpg no diretório
        if f'capa{id}' in nome_arquivo:
            # retorna o caminho completo da imagem
            return nome_arquivo
    
    # senão retorna a capa padrão    
    return 'capa_padrao.PNG'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))