from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.env')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'db_escola'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}


# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None


app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_imoveis():

    # conectar colm a base
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()

    sql = "SELECT * from imoveis"
    cursor.execute(sql)

    results = cursor.fetchall()
    if not results:
        resp = {"erro": "Nenhum imovel encontrado"}
        return resp, 404
    else:
        imoveis = []
        for imovel in results:
            imovel_dict = {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8]
            }
            imoveis.append(imovel_dict)

        resp = {"imoveis": imoveis}
        return resp, 200
    
@app.route('/<int:id>', methods=['GET'])
def get_imoveis_por_id(id):

    # conectar colm a base
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()

    sql = "SELECT * from imoveis WHERE id = %s"
    cursor.execute(sql, (id,))

    results = cursor.fetchone()
    if not results:
        resp = {"erro": "Nenhum imovel com esse id encontrado"}
        return resp, 404
    else:
        imoveis = []
        for imovel in results:
            imovel_dict = {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8]
            }
            imoveis.append(imovel_dict)

        resp = {"imoveis": imoveis}
        return resp, 200



if __name__ == '__main__':
    app.run(debug=True)