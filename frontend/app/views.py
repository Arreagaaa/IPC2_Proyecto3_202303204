from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import requests
import json

BACKEND_URL = 'http://127.0.0.1:5001'


def index(request):
    """Vista principal del sistema"""
    # Obtener estadísticas del backend
    try:
        response = requests.get(f'{BACKEND_URL}/summary')
        if response.status_code == 200:
            data = response.json()
            summary = data.get('summary', {})
        else:
            summary = {'resources': 0, 'clients': 0,
                       'instances': 0, 'invoices': 0}
    except:
        summary = {'resources': 0, 'clients': 0, 'instances': 0, 'invoices': 0}

    return render(request, 'index.html', {'summary': summary})


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


# ========== NUEVAS VISTAS SEMANA 3 ==========

def billing(request):
    """Página de facturación con selector de rango de fechas"""
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not start_date or not end_date:
            return render(request, 'billing.html', {
                'error': 'Debe proporcionar fechas de inicio y fin'
            })

        try:
            response = requests.post(
                f'{BACKEND_URL}/api/facturar',
                json={'start_date': start_date, 'end_date': end_date},
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                data = response.json()
                return render(request, 'billing_result.html', {
                    'success': True,
                    'message': data.get('message', ''),
                    'invoices': data.get('invoices', []),
                    'count': data.get('count', 0),
                    'start_date': start_date,
                    'end_date': end_date
                })
            else:
                return render(request, 'billing.html', {
                    'error': response.json().get('error', 'Error al generar facturas')
                })
        except Exception as e:
            return render(request, 'billing.html', {
                'error': str(e)
            })

    return render(request, 'billing.html')


def create_resource(request):
    """Crear un nuevo recurso"""
    if request.method == 'POST':
        try:
            data = {
                'id': int(request.POST.get('id')),
                'name': request.POST.get('name'),
                'abbreviation': request.POST.get('abbreviation'),
                'metric': request.POST.get('metric'),
                'type': request.POST.get('type'),
                'value_per_hour': float(request.POST.get('value_per_hour'))
            }

            response = requests.post(
                f'{BACKEND_URL}/api/crearRecurso',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 201:
                result = response.json()
                return render(request, 'result.html', {
                    'success': True,
                    'message': result.get('message', 'Recurso creado exitosamente')
                })
            else:
                return render(request, 'create_resource.html', {
                    'error': response.json().get('error', 'Error al crear recurso')
                })
        except Exception as e:
            return render(request, 'create_resource.html', {
                'error': str(e)
            })

    return render(request, 'create_resource.html')


def create_category(request):
    """Crear una nueva categoría"""
    if request.method == 'POST':
        try:
            data = {
                'id': int(request.POST.get('id')),
                'name': request.POST.get('name'),
                'description': request.POST.get('description', ''),
                'workload': request.POST.get('workload'),
                'configurations': []
            }

            response = requests.post(
                f'{BACKEND_URL}/api/crearCategoria',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 201:
                result = response.json()
                return render(request, 'result.html', {
                    'success': True,
                    'message': result.get('message', 'Categoría creada exitosamente')
                })
            else:
                return render(request, 'create_category.html', {
                    'error': response.json().get('error', 'Error al crear categoría')
                })
        except Exception as e:
            return render(request, 'create_category.html', {
                'error': str(e)
            })

    return render(request, 'create_category.html')


def create_client(request):
    """Crear un nuevo cliente"""
    if request.method == 'POST':
        try:
            data = {
                'nit': request.POST.get('nit'),
                'name': request.POST.get('name'),
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'address': request.POST.get('address', ''),
                'email': request.POST.get('email', '')
            }

            response = requests.post(
                f'{BACKEND_URL}/api/crearCliente',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 201:
                result = response.json()
                return render(request, 'result.html', {
                    'success': True,
                    'message': result.get('message', 'Cliente creado exitosamente')
                })
            else:
                return render(request, 'create_client.html', {
                    'error': response.json().get('error', 'Error al crear cliente')
                })
        except Exception as e:
            return render(request, 'create_client.html', {
                'error': str(e)
            })

    return render(request, 'create_client.html')


def create_instance(request):
    """Crear una nueva instancia"""
    if request.method == 'POST':
        try:
            data = {
                'client_nit': request.POST.get('client_nit'),
                'id': int(request.POST.get('id')),
                'configuration_id': int(request.POST.get('configuration_id')),
                'name': request.POST.get('name'),
                'start_date': request.POST.get('start_date')
            }

            response = requests.post(
                f'{BACKEND_URL}/api/crearInstancia',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 201:
                result = response.json()
                return render(request, 'result.html', {
                    'success': True,
                    'message': result.get('message', 'Instancia creada exitosamente')
                })
            else:
                return render(request, 'create_instance.html', {
                    'error': response.json().get('error', 'Error al crear instancia')
                })
        except Exception as e:
            return render(request, 'create_instance.html', {
                'error': str(e)
            })

    # Obtener clientes y configuraciones para los selectores
    try:
        response = requests.get(f'{BACKEND_URL}/consultar')
        if response.status_code == 200:
            data = response.json()
            return render(request, 'create_instance.html', {
                'clients': data.get('clients', []),
                'categories': data.get('categories', [])
            })
    except:
        pass

    return render(request, 'create_instance.html', {'clients': [], 'categories': []})


def cancel_instance_view(request):
    """Cancelar una instancia existente"""
    if request.method == 'POST':
        try:
            data = {
                'client_nit': request.POST.get('client_nit'),
                'instance_id': int(request.POST.get('instance_id')),
                'end_date': request.POST.get('end_date')
            }

            response = requests.post(
                f'{BACKEND_URL}/api/cancelarInstancia',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                result = response.json()
                return render(request, 'result.html', {
                    'success': True,
                    'message': result.get('message', 'Instancia cancelada exitosamente')
                })
            else:
                return render(request, 'cancel_instance.html', {
                    'error': response.json().get('error', 'Error al cancelar instancia')
                })
        except Exception as e:
            return render(request, 'cancel_instance.html', {
                'error': str(e)
            })

    # Obtener clientes con instancias vigentes
    try:
        response = requests.get(f'{BACKEND_URL}/consultar')
        if response.status_code == 200:
            data = response.json()
            return render(request, 'cancel_instance.html', {
                'clients': data.get('clients', [])
            })
    except:
        pass

    return render(request, 'cancel_instance.html', {'clients': []})


def view_invoices(request):
    """Ver todas las facturas generadas"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/facturas')

        if response.status_code == 200:
            data = response.json()
            return render(request, 'invoices.html', {
                'success': True,
                'invoices': data.get('invoices', []),
                'count': data.get('count', 0)
            })
        else:
            return render(request, 'invoices.html', {
                'success': False,
                'error': response.json().get('error', 'Error al consultar facturas')
            })
    except Exception as e:
        return render(request, 'invoices.html', {
            'success': False,
            'error': str(e)
        })


def pending_consumptions(request):
    """Ver consumos pendientes de facturar"""
    try:
        response = requests.get(f'{BACKEND_URL}/consumos/pendientes')

        if response.status_code == 200:
            data = response.json()
            return render(request, 'pending_consumptions.html', {
                'success': True,
                'consumptions': data.get('consumptions', []),
                'count': data.get('count', 0)
            })
        else:
            return render(request, 'pending_consumptions.html', {
                'success': False,
                'error': response.json().get('error', 'Error al consultar consumos pendientes')
            })
    except Exception as e:
        return render(request, 'pending_consumptions.html', {
            'success': False,
            'error': str(e)
        })
