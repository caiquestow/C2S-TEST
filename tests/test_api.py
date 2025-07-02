import requests

BASE_URL = "http://127.0.0.1:8000"

# Teste 1: Buscar todos os veículos (sem filtro)
def test_busca_todos():
    resp = requests.get(f"{BASE_URL}/veiculos")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Precisa ter itens no banco de dados

# Teste 2: Buscar veículos por marca e categoria
def test_busca_marca_categoria():
    params = {"marca": ["Honda"], "categoria": ["Sedan"]}
    resp = requests.get(f"{BASE_URL}/veiculos", params=params)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # Garante a verificação somente quando houver resultado
    for v in data:
        assert v["marca"].lower() == "honda"
        assert v["categoria"].lower() == "sedan" 