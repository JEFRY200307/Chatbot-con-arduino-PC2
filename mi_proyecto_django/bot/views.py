from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import os
import requests
import json

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
NUMERO_USUARIO = os.getenv("USER_NUMBER")

def enviar_mensaje(mensaje, telefono):
    url = f'https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {"body": mensaje}
    }
    requests.post(url, headers=headers, json=data)

@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse('Token inválido', status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        # Aquí copia la lógica de tu Flask POST
        # Puedes importar obtener_datos desde tu nuevo servicio de lectura
        return JsonResponse({'status': 'ok'})