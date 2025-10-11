from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests

BACKEND_URL = 'http://127.0.0.1:5001/api/crearConfiguracion'


def index(request):
    return render(request, 'index.html')


def upload_xml(request):
    if request.method == 'POST' and request.FILES.get('xmlfile'):
        xml_file = request.FILES['xmlfile']
        content = xml_file.read()
        # Enviar al backend
        try:
            response = requests.post(BACKEND_URL, data=content, headers={
                                     'Content-Type': 'application/xml'})
            return JsonResponse({'status': response.status_code, 'response': response.json()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido o falta archivo'}, status=400)
