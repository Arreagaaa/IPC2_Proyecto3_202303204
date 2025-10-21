from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import requests
import json

BACKEND_URL = 'http://127.0.0.1:5001'


def index(request):
    """Vista principal del sistema"""
    return render(request, 'index.html')


def upload_configuration(request):
    """Cargar XML de configuración (recursos, categorías, clientes, instancias)"""
    if request.method == 'POST' and request.FILES.get('xmlfile'):
        xml_file = request.FILES['xmlfile']
        content = xml_file.read()

        try:
            response = requests.post(
                f'{BACKEND_URL}/configuracion',
                data=content,
                headers={'Content-Type': 'application/xml'}
            )

            if response.status_code == 200:
                data = response.json()
                return render(request, 'result.html', {
                    'success': True,
                    'message': data.get('message', ''),
                    'data': data
                })
            else:
                return render(request, 'result.html', {
                    'success': False,
                    'error': response.json().get('error', 'Error desconocido')
                })
        except Exception as e:
            return render(request, 'result.html', {
                'success': False,
                'error': str(e)
            })

    return render(request, 'upload_configuration.html')


def upload_consumption(request):
    """Cargar XML de consumos"""
    if request.method == 'POST' and request.FILES.get('xmlfile'):
        xml_file = request.FILES['xmlfile']
        content = xml_file.read()

        try:
            response = requests.post(
                f'{BACKEND_URL}/consumo',
                data=content,
                headers={'Content-Type': 'application/xml'}
            )

            if response.status_code == 200:
                data = response.json()
                return render(request, 'result.html', {
                    'success': True,
                    'message': data.get('message', ''),
                    'data': data
                })
            else:
                return render(request, 'result.html', {
                    'success': False,
                    'error': response.json().get('error', 'Error desconocido')
                })
        except Exception as e:
            return render(request, 'result.html', {
                'success': False,
                'error': str(e)
            })

    return render(request, 'upload_consumption.html')


def initialize_system(request):
    """Inicializar/limpiar el sistema"""
    if request.method == 'POST':
        try:
            response = requests.post(f'{BACKEND_URL}/inicializar')

            if response.status_code == 200:
                data = response.json()
                return render(request, 'result.html', {
                    'success': True,
                    'message': data.get('message', 'Sistema inicializado correctamente')
                })
            else:
                return render(request, 'result.html', {
                    'success': False,
                    'error': response.json().get('error', 'Error al inicializar')
                })
        except Exception as e:
            return render(request, 'result.html', {
                'success': False,
                'error': str(e)
            })

    return render(request, 'initialize.html')


def query_data(request):
    """Consultar datos actuales del sistema"""
    try:
        response = requests.get(f'{BACKEND_URL}/consultar')

        if response.status_code == 200:
            data = response.json()
            return render(request, 'query_data.html', {
                'success': True,
                'data': data
            })
        else:
            return render(request, 'query_data.html', {
                'success': False,
                'error': response.json().get('error', 'Error al consultar datos')
            })
    except Exception as e:
        return render(request, 'query_data.html', {
            'success': False,
            'error': str(e)
        })


def student_info(request):
    """Información del estudiante"""
    return render(request, 'student_info.html')
