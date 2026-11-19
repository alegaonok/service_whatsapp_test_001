from whatsapp_service_002.app import app

def test_webhook_receive_text_message():
    client = app.test_client()

    payload = {
        "object": "whatsapp_business_account",
	"entry": [
            {
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "messages": [
                                {
                                    "from": "5491112345678",
                                    "type": "text",
                                    "text": {

                                        "body": "Hola"
}


}



]



}



}


]

}

] 


}

    response = client.post(
        "/webhook",
        json=payload
    )

    assert response.status_code == 200
    assert response.json["message"] == "Datos Recibidos."

def test_webhook_invalid_json():
    client = app.test_client()

    response = client.post(
        "/webhook",
        data = "esto no es un json",
        content_type = "application/json"
    )

    assert response.status_code == 400
    assert response.json == {
        "error": "El cuerpo de la peticion debe ser un objeto JSON"
    }

def test_webhook_not_json():
    client = app.test_client()

    response = client.post(
        "/webhook",
        json = ["Hola", "Chau"]
    )

    assert response.status_code == 400
    assert response.json == {
        "error": "El cuerpo de la peticion debe ser un objeto JSON"
    }

def test_webhook_receive_status_event():
    client = app.test_client()

    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "statuses": [
                                {
                                    "id": "wamid.test123",
                                    "status": "delivered"
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

    response = client.post(
        "/webhook",
        json=payload
    )

    assert response.status_code == 200

def test_webhook_missing_entry():
    client = app.test_client()

    response = client.post(
        "/webhook",
        json={}
    )

    assert response.status_code == 400

def test_webhook_entry_invalid_type():
    client = app.test_client()

    payload = {
        "entry": "esto deberia ser una lista"
    }

    response = client.post(
        "/webhook",
        json=payload
    )

    assert response.status_code == 400

def test_webhook_entry_empty():
    client = app.test_client()

    payload = {
        "entry": []
    }

    response = client.post(
        "/webhook",
        json=payload
    )

    assert response.status_code == 400

def test_webhook_entry_item_invalid_type():
    client = app.test_client()
   
    payload = {
        "entry": ["Esto deberia ser un diccionario"]
    }

    response = client.post(
        "/webhook",
        json=payload
    )

    assert response.status_code == 400

def test_webhook_missing_changes():
    client = app.test_client()

    payload = {
        "entry": [
            {}
        ]
    }

    response = client.post(
        "/webhook",
        json=payload
    )

    assert response.status_code == 400
    assert response.json == {
        "error": "Falta el campo 'changes'"
    }

def test_webhook_changes_not_list():
    client = app.test_client()

    payload = {
        "entry": [
            {"changes": "esto deberia de ser una lista"}
    ]
}
    response = client.post(
        "/webhook",
        json=payload
    )
    
    assert response.status_code == 400

def test_webhook_changes_empty():
    client = app.test_client()

    payload = {
        "entry": [
        {"changes": []}
    ]
}

    response = client.post(
        "/webhook",
        json=payload
)

    assert response.status_code == 400

def test_webhook_changes_is_dict():
    client = app.test_client()
  
    payload = {
        "entry": [
            {
                "changes": [
                "esto deberia ser un objeto JSON"
                ]
            }
        ]

    }
    
    response = client.post(
        "/webhook",
        json=payload
    )

    assert response.status_code == 400
