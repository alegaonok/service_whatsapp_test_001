from whatsapp_service_002.app import app

def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"message": "Servidor ok"}


def test_route_not_found():
    client = app.test_client()

    response =client.get("/ruta_inexistente")

    assert response.status_code == 404
