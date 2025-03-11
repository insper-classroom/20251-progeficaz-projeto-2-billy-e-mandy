from flask import Flask, request, jsonify
from utils import connect_db


app = Flask(__name__)

@app.route('/')
@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    # conectar colm a base
    conn = connect_db()
    if conn is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()
    sql = "SELECT * from imoveis"
    cursor.execute(sql)

    results = cursor.fetchall()
    if not results:
        return jsonify({"erro": "Nenhum imovel encontrado"}), 404
    
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
    return jsonify({"imoveis": imoveis}), 200



@app.route('/imoveis', methods=['POST'])
def add_imoveis():
    novo_imovel = request.json
    conn = connect_db()
    if conn is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
    
    cursor = conn.cursor()
    sql = "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, (novo_imovel['logradouro'], novo_imovel['tipo_logradouro'], novo_imovel['bairro'], novo_imovel['cidade'], novo_imovel['cep'], novo_imovel['tipo'], novo_imovel['valor'], novo_imovel['data_aquisicao']))
    conn.commit()
    conn.close()
    return jsonify({"imovel": novo_imovel}), 201

    
@app.route('/imoveis/<int:id>', methods=['GET'])
def get_imoveis_por_id(id):
    # conectar colm a base
    conn = connect_db()

    if conn is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()
    sql = "SELECT * from imoveis WHERE id = %s"
    cursor.execute(sql, (id,))
    imovel = cursor.fetchone()

    if not imovel:
        return jsonify({"erro": "Nenhum imovel com esse id encontrado"}), 404
   
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

    return jsonify({"imoveis": imovel_dict}), 200


@app.route('/imoveis/tipo/<string:tipo>', methods=['GET'])
def get_imoveis_por_tipo(tipo):
    # conectar colm a base
    conn = connect_db()

    if conn is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()
    sql = "SELECT * from imoveis WHERE tipo =%s"
    cursor.execute(sql, (tipo,))
    results = cursor.fetchall()
    conn.commit()
    conn.close()    

    if not results:
        return jsonify({"erro": "Nenhum imovel com esse tipo encontrado"}), 404
    
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
    return jsonify({"imoveis": imoveis}), 200
    


@app.route('/imoveis/cidade/<string:cidade>', methods=['GET'])
def get_imoveis_por_cidade(cidade):
    # conectar colm a base
    conn = connect_db()

    if conn is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    # se chegou até, tenho uma conexão válida
    cursor = conn.cursor()
    sql = "SELECT * from imoveis WHERE cidade = %s"
    cursor.execute(sql, (cidade,))
    results = cursor.fetchall()
    conn.commit()
    conn.close()

    if not results:
        return jsonify({"erro": "Nenhum imovel com essa cidade encontrado"}), 404


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

    return jsonify({"imoveis": imoveis}), 200



if __name__ == '__main__':
    app.run(debug=True)

