from flask import Flask, request

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
    entry = data["entry"]

    print(entry)
    print(type(entry))

    entry_item = entry[0]
    print(f"El entry_item: {entry_item}")
    print(type(entry_item))

    changes = entry_item["changes"]
    print(f"changes es: {changes}")
    print(type(changes))

    value = changes[0]
    print(f"Values contiene: {value}")
    print(type(value))

    value_dict = value["value"]
    print(f"El value dict es: {value_dict}")
    print(type(value_dict))

    messages = value_dict["messages"]
    print(f"Contenido de messages es : {messages}")
    print(type(messages))

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

    return {
        "message": "Datos Recibidos.",
        "data": data
    }, 200


@app.errorhandler(404)
def not_found(error):
    return {"error": "Ruta no encontrada"}, 404
