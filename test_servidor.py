import pytest
from unittest.mock import patch, MagicMock
from servidor import app, connect_db

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
        (2, "Sem Saída", "Rua", "Centro", "São Paulo", "04552999", "mansão", 1000000.00, "2022-05-30"),
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
            {"id": 2, "logradouro": "Sem Saída", "tipo_logradouro": "Rua", "bairro": "Centro", "cidade": "São Paulo", "cep": "04552999", "tipo": "mansão", "valor": 1000000.00, "data_aquisicao": "2022-05-30"},
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