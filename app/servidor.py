from flask import Flask, request, jsonify
from app.utils import connect_db


app = Flask(__name__)

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



if __name__ == '__main__':
    app.run(debug=True)