# chave que a biblioteca flask-login pede, pode ser string
SECRET_KEY= 'alura'

# variavel para conexão com banco de dados, parametro a aplicação que está rodando
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'jogoteca'   
    )
