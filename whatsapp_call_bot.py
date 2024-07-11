import requests

# Configuración de la API Flask
BASE_URL = 'http://127.0.0.1:5000'

def enviar_mensaje_whatsapp(to, message):
    url = f'{BASE_URL}/enviar_mensaje'
    data = {
        "to": to,
        "message": message
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Mensaje enviado:', response.json())
    else:
        print('Error al enviar mensaje:', response.status_code, response.text)

def hacer_llamada(to):
    url = f'{BASE_URL}/hacer_llamada'
    data = {
        "to": to
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Llamada realizada:', response.json())
    else:
        print('Error al realizar llamada:', response.status_code, response.text)

if __name__ == "__main__":
    # Ejemplo de uso
    enviar_mensaje_whatsapp("whatsapp:+1234567890", "Hola desde Python!")
    hacer_llamada("+1234567890")
