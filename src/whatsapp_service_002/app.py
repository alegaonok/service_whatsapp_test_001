import os
from dotenv import load_dotenv
from flask import Flask, request
import requests

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
    """
    if "message" not in data:
        return {
            "error": "El campo 'message' es obligatorio"
        }, 400
    if not isinstance(data["message"], str):
        return {
            "error": "El campo 'message' debe ser un texto"
        }, 400
    if not data["message"].strip():
        return {
            "error": "El campo 'message' no puede estar vacio"
        }, 400

    print(data)
    print(type(data))

    message = data["message"]
    print(message)
    print(type(message))

    sender = data.get("from")
    print(sender)
    print(type(sender))
    """
    if "entry" not in data:
        return {
            "error": "Falta el campo 'entry'"
        }, 400

    entry = data["entry"]

    if not isinstance(entry, list):
        return {
            "error": "El campo 'entry' debe ser una lista"
        }, 400

    if not entry:
        return {
            "error": "El campo 'entry' no puede estar vacio"
        }, 400

    print(entry)
    print(type(entry))

    entry_item = entry[0]

    if not isinstance(entry_item, dict):
        return {
            "error": "El campo 'entry_item' no debe ser una lista"
        }, 400
    
    print(f"El entry_item: {entry_item}")
    print(type(entry_item))

    if "changes" not in entry_item:
        return {
            "error": "Falta el campo 'changes'"
        }, 400
        
    changes = entry_item["changes"]
    
    print(f"changes es: {changes}")
    print(type(changes))

    value = changes[0]
    print(f"Values contiene: {value}")
    print(type(value))

    value_dict = value["value"]
    print(f"El value dict es: {value_dict}")
    print(type(value_dict))

    event_found = False

    if "statuses" in value_dict:
        statuses = value_dict["statuses"]
        print("Evento de estado recibido:", len(statuses))
        event_found = True

    if "messages" in value_dict:
        messages = value_dict["messages"]
        print("messages presente")
        event_found = True

        for message_item in messages:
            sender = message_item["from"]
            # validar si el mensaje es una foto, audio, text, etc
            message_type = message_item["type"]

            if message_type == "text":

                text = message_item["text"]
                body = text["body"]

                print(f"""
                    Remitente: {sender},
                    Mensaje: {body}
                """)

            else:
                print("Tipo de mensaje no soportado", message_type)

        
        if not event_found:
            print("Evento no encontrado")

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
