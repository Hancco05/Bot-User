import subprocess
import re
from flask import Flask, request, jsonify
from twilio.rest import Client
from pydub import AudioSegment
from pydub.playback import play

# Configuración de Twilio
TWILIO_ACCOUNT_SID = 'tucuenta'
TWILIO_AUTH_TOKEN = 'tuauthcuenta'
TWILIO_PHONE_NUMBER = '+tunumero'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
app = Flask(__name__)

# Función para reproducir sonido de alerta
def reproducir_alerta():
    sonido = AudioSegment.from_file("alerta.mp3")
    play(sonido)

# Función para detectar llamadas entrantes
def detectar_llamadas():
    result = subprocess.run(['adb', 'logcat', '-d', 'PhoneStateListener'], capture_output=True, text=True)
    llamadas = []
    for line in result.stdout.splitlines():
        if "RINGING" in line:
            match = re.search(r'RINGING (\d+)', line)
            if match:
                numero = match.group(1)
                llamadas.append(numero)
    return llamadas

@app.route('/llamadas', methods=['GET'])
def obtener_llamadas():
    llamadas = detectar_llamadas()
    if llamadas:
        reproducir_alerta()
    return jsonify(llamadas)

# Función para detectar mensajes de WhatsApp
def detectar_mensajes_whatsapp():
    result = subprocess.run(['adb', 'logcat', '-d', 'NotificationListener'], capture_output=True, text=True)
    mensajes = []
    for line in result.stdout.splitlines():
        if "WhatsApp" in line and "mensaje recibido" in line:
            match = re.search(r'mensaje recibido de (\w+): (.+)', line)
            if match:
                contacto = match.group(1)
                mensaje = match.group(2)
                mensajes.append({'contacto': contacto, 'mensaje': mensaje})
    return mensajes

@app.route('/mensajes_whatsapp', methods=['GET'])
def obtener_mensajes_whatsapp():
    mensajes = detectar_mensajes_whatsapp()
    if mensajes:
        reproducir_alerta()
    return jsonify(mensajes)

# Función para enviar mensajes de WhatsApp
@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    to = data['to']
    message = data['message']
    client.messages.create(body=message, from_=f'whatsapp:{TWILIO_PHONE_NUMBER}', to=f'whatsapp:{to}')
    return jsonify({'status': 'mensaje enviado'})

# Función para hacer una llamada
@app.route('/hacer_llamada', methods=['POST'])
def hacer_llamada():
    data = request.get_json()
    to = data['to']
    call = client.calls.create(
        twiml='<Response><Say>Esta es una llamada de prueba desde tu bot de Python</Say></Response>',
        from_=TWILIO_PHONE_NUMBER,
        to=to
    )
    return jsonify({'status': 'llamada realizada', 'call_sid': call.sid})

if __name__ == "__main__":
    app.run(debug=True)
