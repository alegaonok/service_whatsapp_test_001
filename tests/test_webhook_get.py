from whatsapp_service_002.app import app

def test_webhook_verification_success(monkeypatch):
    client = app.test_client()

    monkeypatch.setattr(
        "whatsapp_service_002.app.WEBHOOK_VERIFY_TOKEN",
        "token_de_prueba"
    )

    response = client.get(
        "/webhook",
        query_string={
        "hub.mode": "subscribe",
        "hub.verify_token": "token_de_prueba",
        "hub.challenge": "123456"
        }
    )

    assert response.status_code == 200
    assert response.text == "123456"

def test_webhook_verification_failure(monkeypatch):
    client = app.test_client()

    monkeypatch.setattr(
        "whatsapp_service_002.app.WEBHOOK_VERIFY_TOKEN",
        "token_correcto"
    )

    response = client.get(
        "/webhook",
        query_string={
            "hub.mode": "subscribe",
            "hub.verify_token": "token_de_prueba",
            "hub.challenge": "123456" 
        }
    )

    assert response.status_code == 403
    assert response.text == "Forbidden"
