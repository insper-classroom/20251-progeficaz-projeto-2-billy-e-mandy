import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import connect_db
from config import config
from servidor import app


@pytest.fixture
def client():
    """Cria um cliente de teste para a API."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client









@patch("servidor.connect_db")  # Substituímos a função que conecta ao banco por um Mock
def test_get_imoveis(mock_connect_db, client):
    """Testa a rota /imoveis sem acessar o banco de dados real."""

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos o retorno do banco de dados
    mock_cursor.fetchall.return_value = [
        (1, "José Eiras Pinheiro", "Rua", "Barra da Tijuca", "Rio de Janeiro", "21240004", "casa em condomínio", 150000.00, "2018-01-31"),
        (2, "Sem Saída", "Rua", "Centro", "São Paulo", "04552999", "mansao", 1000000.00, "2022-05-30"),
    ]

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    # Fazemos a requisição para a API
    response = client.get("/imoveis")

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "imoveis": [
            {"id": 1, "logradouro": "José Eiras Pinheiro", "tipo_logradouro": "Rua", "bairro": "Barra da Tijuca", "cidade": "Rio de Janeiro", "cep": "21240004", "tipo": "casa em condomínio", "valor": 150000.00, "data_aquisicao": "2018-01-31"},
            {"id": 2, "logradouro": "Sem Saída", "tipo_logradouro": "Rua", "bairro": "Centro", "cidade": "São Paulo", "cep": "04552999", "tipo": "mansao", "valor": 1000000.00, "data_aquisicao": "2022-05-30"},
        ]
    }
    assert response.get_json() == expected_response











@patch("servidor.connect_db")
def test_get_imoveis_vazio(mock_connect_db, client):
    """Testa a rota /imoveis quando o banco de dados não tem imoveis."""

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos que o banco de dados não retorna nenhum aluno
    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn

    # Fazemos a requisição para a API
    response = client.get("/imoveis")

    # Verificamos se o código de status da resposta é 404 (Nenhum aluno encontrado)
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Nenhum imovel encontrado"}










@patch("servidor.connect_db")  # Substituímos a função que conecta ao banco por um Mock
def test_get_imoveis_por_id(mock_connect_db, client):
    """Testa a rota /imoveis sem acessar o banco de dados real."""

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos o retorno do banco de dados
    mock_cursor.fetchone.return_value = (1, "José Eiras Pinheiro", "Rua", "Barra da Tijuca", "Rio de Janeiro", "21240004", "casa em condomínio", 150000.00, "2018-01-31")
    

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    id = 1

    # Fazemos a requisição para a API
    response = client.get(f"/imoveis/{id}")

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "imoveis": {"id": 1, "logradouro": "José Eiras Pinheiro", "tipo_logradouro": "Rua", "bairro": "Barra da Tijuca", "cidade": "Rio de Janeiro", "cep": "21240004", "tipo": "casa em condomínio", "valor": 150000.00, "data_aquisicao": "2018-01-31"}  
    }
    assert response.get_json() == expected_response









@patch("servidor.connect_db")  # Substituímos a função que conecta ao banco por um Mock
def test_get_imoveis_por_tipo(mock_connect_db, client):
    """Testa a rota /imoveis sem acessar o banco de dados real."""

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos o retorno do banco de dados
    mock_cursor.fetchall.return_value = [
        (2, "Sem Saída", "Rua", "Centro", "São Paulo", "04552999", "mansao", 1000000.00, "2022-05-30")
    ]
    

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    tipo = 'mansao'

    # Fazemos a requisição para a API
    response = client.get(f"/imoveis/tipo/{tipo}")

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "imoveis": [ 
            {"id": 2, "logradouro": "Sem Saída", "tipo_logradouro": "Rua", "bairro": "Centro", "cidade": "São Paulo", "cep": "04552999", "tipo": "mansao", "valor": 1000000.00, "data_aquisicao": "2022-05-30"} 
        ] 
    }
    assert response.get_json() == expected_response







@patch("servidor.connect_db")
def test_get_imoveis_por_tipo_vazio(mock_connect_db, client):
    """Testa a rota /imoveis quando o banco de dados não tem imoveis."""

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos que o banco de dados não retorna nenhum aluno
    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn

    tipo = 'mansao'

    # Fazemos a requisição para a API
    response = client.get(f"/imoveis/tipo/{tipo}")

    # Verificamos se o código de status da resposta é 404 (Nenhum aluno encontrado)
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Nenhum imovel com esse tipo encontrado"}








@patch("servidor.connect_db")  # Substituímos a função que conecta ao banco por um Mock
def test_get_imoveis_por_cidade(mock_connect_db, client):
    """Testa a rota /imoveis sem acessar o banco de dados real."""

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos o retorno do banco de dados
    mock_cursor.fetchall.return_value = [
        (2, "Sem Saída", "Rua", "Centro", "São Paulo", "04552999", "mansao", 1000000.00, "2022-05-30"),
    ]
    

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    cidade = 'São Paulo'

    # Fazemos a requisição para a API
    response = client.get(f"/imoveis/cidade/{cidade}")

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "imoveis": [ 
            {"id": 2, "logradouro": "Sem Saída", "tipo_logradouro": "Rua", "bairro": "Centro", "cidade": "São Paulo", "cep": "04552999", "tipo": "mansao", "valor": 1000000.00, "data_aquisicao": "2022-05-30"} 
        ] 
    }
    assert response.get_json() == expected_response








@patch("servidor.connect_db")
def test_get_imoveis_por_cidade_vazia(mock_connect_db, client):
    """Testa a rota /imoveis quando o banco de dados não tem imoveis."""

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos que o banco de dados não retorna nenhum aluno
    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn

    cidade = 'São Paulo'

    # Fazemos a requisição para a API
    response = client.get(f"/imoveis/cidade/{cidade}")

    # Verificamos se o código de status da resposta é 404 (Nenhum aluno encontrado)
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Nenhum imovel com essa cidade encontrado"}








@patch("servidor.connect_db")
def test_add_imoveis(mock_connect_db, client):
    """Testa a rota /imoveis sem acessar o banco de dados real."""

   
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

   
    mock_connect_db.return_value = mock_conn

    imovel = {
        "logradouro": "Rua Elvira Ferraz",
        "tipo_logradouro": "Rua",
        "bairro": "Vila olimpia",
        "cidade": "São Paulo",
        "cep": "12345678",
        "tipo": "apartamento",
        "valor": 1000000.00,
        "data_aquisicao": "2020-01-01"
    }

  
    response = client.post("/imoveis", json=imovel)

    assert response.status_code == 201

    expected_response = {
        "imovel": imovel
    }
    assert response.get_json() == expected_response









@patch("servidor.connect_db")
def test_update_imoveis(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn

    id = 2

    imovel = {
        "id": 2,
        "logradouro": "Rua Elvira Ferraz",
        "tipo_logradouro": "Rua",
        "bairro": "Vila olimpia",
        "cidade": "São Paulo",
        "cep": "12345678",
        "tipo": "apartamento",
        "valor": 1000000.00,
        "data_aquisicao": "2020-01-01" 
    }

    # Verifica se o imóvel existe 
    mock_cursor.fetchone.return_value = {"id": id}
    mock_cursor.rowcount = 1 

    response = client.put(f"/imoveis/{id}", json=imovel)
    assert response.status_code == 200

    # Verifica se função realmente executou o UPDATE 
    # Pode ser que a função não executou o UPDATE ou os campos não tenham sido alterados corretamente
    mock_cursor.execute.assert_called_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        ("Rua Elvira Ferraz", "Rua", "Vila olimpia", "São Paulo", "12345678", "apartamento", 1000000.00, "2020-01-01", 2)
    )

    # Verifica se a alteração foi salva
    # A alteração pode até ser feita mas nada garante que ela não seja salva. 
    mock_conn.commit.assert_called_once()
    # Essa linha garante verifica isso 

    expected_response = {"mensagem": "Imóvel atualizado com sucesso!"}
    assert response.get_json() == expected_response





@patch("servidor.connect_db")
def test_update_imovel_not_found(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn

    id = 2

    imovel = {
        "id": 1,
        "logradouro": "Rua Quatá",
        "tipo_logradouro": "Rua",
        "bairro": "Vila olimpia",
        "cidade": "São Paulo",
        "cep": "12345678",
        "tipo": "apartamento",
        "valor": 100000000000000.00,
        "data_aquisicao": "2020-01-01" 
    }

    # Verifica o caso de imóvel não encontrado 
    mock_cursor.fetchone.return_value = None 

    response = client.put(f"/imoveis/{id}", json=imovel)
    assert response.status_code == 404
    assert response.get_json() == {"erro": f"Erro ao atualizar imóvel de id:{id}"}




def test_delete_imovel(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn

    id = 1

    # Verifica se o imóvel existe 
    mock_cursor.fetchone.return_value = {"id": id}
    mock_cursor.rowcount = 1 

    response = client.put(f"/imoveis/{id}")
    assert response.status_code == 200

    mock_cursor.execute.assert_called_with(
        "DELETE FROM imoveis WHERE id = %s",
        (id,)
    )

    mock_conn.commit.assert_called_once()

    expected_response = {"mensagem": "Imóvel deletado com sucesso!"
    }

    assert response.get_json() == expected_response



def erro_test_delete_imovel(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn

    id = 1

    # Verifica se o imóvel existe 
    mock_cursor.fetchone.return_value = {"id": id}
    mock_cursor.rowcount = 1 

    response = client.put(f"/imoveis/{id}")
    assert response.status_code == 200

    mock_cursor.execute.assert_called_with(
        "DELETE FROM imoveis WHERE id = %s",
        (id,)
    )

    mock_conn.commit.assert_called_once()

    expected_response = {
        "mensagem": "Imóvel deletado com sucesso!"
    }

    assert response.get_json() == expected_response