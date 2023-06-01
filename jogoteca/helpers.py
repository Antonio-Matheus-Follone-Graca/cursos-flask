import os
from jogoteca import app 

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