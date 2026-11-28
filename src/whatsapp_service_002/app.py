import os
from dotenv import load_dotenv
from flask import Flask, request
import requests
from pydantic import ValidationError
from whatsapp_service_002.schemas.webhook import WebhookPayload

load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
WHATSAPP_RECIPIENT = os.getenv("WHATSAPP_RECIPIENT")
GRAPH_API_VERSION = "v27.0"
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")

GRAPH_API_URL = (
    f"https://graph.facebook.com/"
    f"{GRAPH_API_VERSION}/"
    f"{PHONE_NUMBER_ID}/messages"
)

app = Flask(__name__)

@app.route("/health", methods= ["GET"])
def health():
    return {"message": "Servidor ok"}, 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    print(data)

    if not isinstance(data, dict):
        return {
            "error": "El cuerpo de la peticion debe ser un objeto JSON"
        }, 400
    
    # Aca va mi Payload  
    # Este es mi Payload
    try: 
        payload = WebhookPayload.model_validate(data)

    except ValidationError as error:
        print(error.errors())
        for item in error.errors():
            print("TIPO:", item["type"])
            print("UBICACIÓN:", item["loc"])
            print("MENSAJE:", item["msg"])
            print("-------------------")
            print("UBICACIÓN COMPLETA:", item["loc"])
            
        return {
            "error": "Ele payload recibido no tiene una estructura valida",
            "details": error.errors(include_input=False)
        }, 400


    entry = payload.entry
    changes = entry[0].changes
    change = changes[0]
    value = change.value

    event_found = False


    if value.statuses is not None:
        statuses = value.statuses
        print("Evento de estado recibido:", len(statuses))
        event_found = True

    if value.messages is not None:
        messages = value.messages
        print("messages presente")
        event_found = True

        for message_item in messages:
            sender = message_item.value_from
            message_type = message_item.type

            if message_type == "text":
                body = message_item.text.body

                print(f"""
                    Remitente: {sender},
                    Mensaje: {body}
                """)

            else:
                print("Tipo de mensaje no soportado", message_type)


    return {
        "message": "Datos Recibidos.",
        "data": data
    }, 200
    
    # print(f"Contenido de messages es : {messages}")
    # print(type(messages))

    """
    messages_item = messages[0]
    print(f"El conetido de messages_item es : {messages_item}")
    print(type(messages_item))

    remitente = messages_item["from"]
    texto = messages_item["text"]
    print(f
        Remitente es: {remitente}
        texto es: {texto["body"]}
    )
    """


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        return challenge, 200

    return "Forbidden", 403


def send_message():
    payload = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_RECIPIENT,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        GRAPH_API_URL,
        headers=headers,
        json=payload,
        timeout=20
    )

    print("Status code:", response.status_code)
    print("Respuesta de Meta:", response.json())

    return response


@app.errorhandler(404)
def not_found(error):
    return {"error": "Ruta no encontrada"}, 404
