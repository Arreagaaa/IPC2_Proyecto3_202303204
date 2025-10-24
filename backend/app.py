from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
from pathlib import Path
from models import parser
from models.storage import XMLStorage
from models.domain import Resource, Category, Configuration, ConfigurationResource, Client, Instance
from models.validators import validate_nit, extract_first_date
from services.billing import BillingService

app = Flask(__name__)
CORS(app)  # Permitir CORS para Django frontend

DATA_DIR = Path(__file__).resolve().parent / 'instance' / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = DATA_DIR / 'db.xml'

# Inicializar almacenamiento y servicios
storage = XMLStorage(DB_FILE)
billing_service = BillingService(storage)


# Endpoint para configuraciones (version completa - XML masivo)
@app.route('/configuracion', methods=['POST'])
def upload_configuration_xml():
    data = request.data
    if not data:
        return jsonify({'error': 'No se proporcionó XML'}), 400
    try:
        resources, categories, clients, counts = parser.parse_configurations_xml(
            data.decode('utf-8'))

        # Almacenar entidades
        if resources:
            storage.add_resources(resources)
        if categories:
            storage.add_categories(categories)
        if clients:
            storage.add_clients(clients)

        return jsonify({
            'status': 'ok',
            'message': f"{counts['resources']} recursos, {counts['categories']} categorías, {counts['configurations']} configuraciones, {counts['clients']} clientes, {counts['instances']} instancias creadas",
            'counts': counts
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para consumos
@app.route('/consumo', methods=['POST'])
@app.route('/api/consumos', methods=['POST'])
def create_consumptions():

    data = request.data
    if not data:
        return jsonify({'error': 'No se proporcionó XML'}), 400
    try:
        parsed = parser.parse_consumptions_xml(data.decode('utf-8'))

        # Almacenar consumos
        for consumption in parsed:
            storage.add_consumption(
                nit=consumption['nit'],
                instance_id=consumption['instance_id'],
                time_hours=consumption['time'],
                date_time=consumption['date_time']
            )

        return jsonify({
            'status': 'ok',
            'message': f"{len(parsed)} consumos procesados",
            'count': len(parsed)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para inicializar/limpiar base de datos
@app.route('/inicializar', methods=['POST', 'GET'])
def initialize_system():

    try:
        storage.clear_all()
        return jsonify({
            'status': 'ok',
            'message': 'Sistema inicializado correctamente. Todos los datos han sido eliminados.'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para consultar datos actuales
@app.route('/consultar', methods=['GET'])
@app.route('/api/consultarDatos', methods=['GET'])
def query_data():

    try:
        data = storage.get_all_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para crear recurso individual (CRUD)
@app.route('/api/crearRecurso', methods=['POST'])
def create_resource():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        required = ['id', 'name', 'abbreviation',
                    'metric', 'type', 'value_per_hour']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400

        # Crear recurso
        resource = Resource(
            id=int(data['id']),
            name=data['name'],
            abbreviation=data['abbreviation'],
            metric=data['metric'],
            type=data['type'],
            value_per_hour=float(data['value_per_hour'])
        )

        storage.add_resources([resource])

        return jsonify({
            'status': 'ok',
            'message': f'Recurso "{resource.name}" creado exitosamente',
            'resource': {
                'id': resource.id,
                'name': resource.name,
                'type': resource.type,
                'value_per_hour': resource.value_per_hour
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para crear categoría con configuraciones (CRUD)
@app.route('/api/crearCategoria', methods=['POST'])
def create_category():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        required = ['id', 'name', 'workload']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400

        # Crear configuraciones
        configurations = []
        if 'configurations' in data and data['configurations']:
            for config_data in data['configurations']:
                resources = []
                if 'resources' in config_data:
                    for res in config_data['resources']:
                        resources.append(ConfigurationResource(
                            resource_id=int(res['resource_id']),
                            quantity=float(res['quantity'])
                        ))

                configurations.append(Configuration(
                    id=int(config_data['id']),
                    name=config_data['name'],
                    description=config_data.get('description', ''),
                    resources=resources
                ))

        # Crear categoría
        category = Category(
            id=int(data['id']),
            name=data['name'],
            description=data.get('description', ''),
            workload=data['workload'],
            configurations=configurations
        )

        storage.add_categories([category])

        return jsonify({
            'status': 'ok',
            'message': f'Categoría "{category.name}" creada exitosamente',
            'category': {
                'id': category.id,
                'name': category.name,
                'workload': category.workload,
                'configurations_count': len(configurations)
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para crear configuracion (CRUD - JSON individual)
@app.route('/api/crearConfiguracion', methods=['POST'])
def create_single_configuration():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        if 'category_id' not in data:
            return jsonify({'error': 'Campo requerido: category_id'}), 400

        if 'configuration' not in data:
            return jsonify({'error': 'Campo requerido: configuration'}), 400

        config_data = data['configuration']
        required_config = ['id', 'name']
        for field in required_config:
            if field not in config_data:
                return jsonify({'error': f'Campo requerido en configuration: {field}'}), 400

        # Verificar que la categoria existe
        category = storage.get_category_by_id(str(data['category_id']))
        if not category:
            return jsonify({'error': f'Categoría con ID {data["category_id"]} no existe'}), 404

        # Crear recursos de la configuracion
        resources = []
        if 'resources' in config_data and config_data['resources']:
            for res in config_data['resources']:
                if 'resource_id' not in res or 'quantity' not in res:
                    return jsonify({'error': 'Cada recurso debe tener resource_id y quantity'}), 400

                # Verificar que el recurso existe
                resource = storage.get_resource_by_id(str(res['resource_id']))
                if not resource:
                    return jsonify({'error': f'Recurso con ID {res["resource_id"]} no existe'}), 404

                resources.append(ConfigurationResource(
                    resource_id=int(res['resource_id']),
                    quantity=float(res['quantity'])
                ))

        # Crear configuracion
        configuration = Configuration(
            id=int(config_data['id']),
            name=config_data['name'],
            description=config_data.get('description', ''),
            resources=resources
        )

        # Agregar configuracion a la categoria
        storage.add_configuration_to_category(
            int(data['category_id']),
            configuration
        )

        return jsonify({
            'status': 'ok',
            'message': f'Configuración "{configuration.name}" agregada a categoría exitosamente',
            'configuration': {
                'id': configuration.id,
                'name': configuration.name,
                'description': configuration.description,
                'category_id': data['category_id'],
                'resources_count': len(resources)
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para crear cliente (CRUD)
@app.route('/api/crearCliente', methods=['POST'])
def create_client():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        required = ['nit', 'name', 'username', 'password']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400

        # Validar NIT
        if not validate_nit(data['nit']):
            return jsonify({'error': f'NIT inválido: {data["nit"]}'}), 400

        # Crear cliente
        client = Client(
            nit=data['nit'],
            name=data['name'],
            username=data['username'],
            password=data['password'],
            address=data.get('address', ''),
            email=data.get('email', ''),
            instances=[]
        )

        storage.add_clients([client])

        return jsonify({
            'status': 'ok',
            'message': f'Cliente "{client.name}" creado exitosamente',
            'client': {
                'nit': client.nit,
                'name': client.name,
                'username': client.username
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para crear instancia (CRUD)
@app.route('/api/crearInstancia', methods=['POST'])
def create_instance():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        required = ['client_nit', 'id',
                    'configuration_id', 'name', 'start_date']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400

        # Validar NIT
        if not validate_nit(data['client_nit']):
            return jsonify({'error': f'NIT inválido: {data["client_nit"]}'}), 400

        # Extraer fecha si viene con texto adicional
        start_date = extract_first_date(data['start_date'])
        if not start_date:
            start_date = data['start_date']

        # Obtener cliente existente
        all_data = storage.get_all_data()
        client_data = None
        for client in all_data['clients']:
            if client['nit'] == data['client_nit']:
                client_data = client
                break

        if not client_data:
            return jsonify({'error': f'Cliente con NIT {data["client_nit"]} no encontrado'}), 404

        # Crear instancia
        instance = Instance(
            id=int(data['id']),
            configuration_id=int(data['configuration_id']),
            name=data['name'],
            start_date=start_date,
            status='Vigente',
            end_date=''
        )

        # Crear cliente completo con la nueva instancia
        instances = [Instance(**inst) for inst in client_data['instances']]
        instances.append(instance)

        client = Client(
            nit=client_data['nit'],
            name=client_data['name'],
            username=client_data['username'],
            password=client_data['password'],
            address=client_data['address'],
            email=client_data['email'],
            instances=instances
        )

        storage.add_clients([client])

        return jsonify({
            'status': 'ok',
            'message': f'Instancia "{instance.name}" creada exitosamente',
            'instance': {
                'id': instance.id,
                'name': instance.name,
                'configuration_id': instance.configuration_id,
                'status': instance.status
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para cancelar instancia
@app.route('/api/cancelarInstancia', methods=['POST'])
def cancel_instance():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        required = ['client_nit', 'instance_id', 'end_date']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400

        # Extraer fecha si viene con texto adicional
        end_date = extract_first_date(data['end_date'])
        if not end_date:
            end_date = data['end_date']

        # Cancelar instancia
        storage.cancel_instance(
            client_nit=data['client_nit'],
            instance_id=str(data['instance_id']),
            end_date=end_date
        )

        return jsonify({
            'status': 'ok',
            'message': f'Instancia {data["instance_id"]} cancelada exitosamente',
            'instance_id': data['instance_id'],
            'end_date': end_date
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para generar facturas
@app.route('/api/facturar', methods=['POST'])
@app.route('/facturar', methods=['POST'])
def generate_invoices():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        required = ['start_date', 'end_date']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400

        start_date = data['start_date']
        end_date = data['end_date']

        # Generar facturas
        invoices = billing_service.generate_invoices(start_date, end_date)

        if not invoices:
            return jsonify({
                'status': 'ok',
                'message': 'No hay consumos pendientes de facturar en el rango especificado',
                'invoices': [],
                'count': 0
            }), 200

        return jsonify({
            'status': 'ok',
            'message': f'{len(invoices)} facturas generadas exitosamente',
            'invoices': invoices,
            'count': len(invoices)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para consultar facturas
@app.route('/api/facturas', methods=['GET'])
@app.route('/facturas', methods=['GET'])
def get_invoices():

    try:
        invoices = storage.get_invoices()
        return jsonify({
            'status': 'ok',
            'invoices': invoices,
            'count': len(invoices)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para consultar consumos pendientes
@app.route('/api/consumosPendientes', methods=['GET'])
@app.route('/consumos/pendientes', methods=['GET'])
def get_unbilled_consumptions():

    try:
        consumptions = storage.get_unbilled_consumptions()
        return jsonify({
            'status': 'ok',
            'consumptions': consumptions,
            'count': len(consumptions)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint para obtener resumen/estadísticas del dashboard
@app.route('/api/summary', methods=['GET'])
@app.route('/summary', methods=['GET'])
def get_summary():

    try:
        resources = storage.get_resources()
        clients = storage.get_clients()
        invoices = storage.get_invoices()

        # Contar instancias totales
        total_instances = 0
        for client in clients:
            total_instances += len(client.get('instances', []))

        return jsonify({
            'status': 'ok',
            'summary': {
                'resources': len(resources),
                'clients': len(clients),
                'instances': total_instances,
                'invoices': len(invoices)
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reporte/factura/<invoice_id>', methods=['GET'])
def get_invoice_report(invoice_id):

    try:
        from services.reports import generate_invoice_detail_pdf

        # Obtener datos de la factura
        invoices = storage.get_invoices()
        invoice = None
        for inv in invoices:
            if inv.get('invoice_number') == invoice_id:
                invoice = inv
                break

        if not invoice:
            return jsonify({'error': 'Factura no encontrada'}), 404

        # Obtener datos del cliente
        clients = storage.get_all_data().get('clients', [])
        client = None
        for c in clients:
            if c.get('nit') == invoice.get('client_nit'):
                client = c
                break

        if not client:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        # Obtener todos los consumos del sistema
        all_data = storage.get_all_data()
        all_consumptions = all_data.get('consumptions', [])
        
        # Los consumption_ids de la factura son índices en el array de consumos
        invoice_consumptions = []
        for idx_str in invoice.get('consumption_ids', []):
            try:
                idx = int(idx_str)
                if 0 <= idx < len(all_consumptions):
                    consumption = all_consumptions[idx]
                    # Verificar que el consumo pertenece al cliente
                    if consumption.get('nit') == invoice.get('client_nit'):
                        invoice_consumptions.append(consumption)
            except (ValueError, IndexError):
                continue

        if not invoice_consumptions:
            return jsonify({'error': 'No se encontraron consumos para esta factura'}), 404

        # Obtener recursos
        resources = all_data.get('resources', [])

        # Construir datos para el reporte agrupados por instancia
        instances_data = {}
        
        for consumption in invoice_consumptions:
            instance_id = consumption.get('instance_id')
            time_hours = float(consumption.get('time_hours', 0))
            date_time = consumption.get('date_time', 'N/A')

            # Buscar instancia en el cliente
            instance = None
            for inst in client.get('instances', []):
                if str(inst.get('id')) == str(instance_id):
                    instance = inst
                    break

            if not instance:
                continue

            # Obtener configuración de la instancia
            config_id = instance.get('configuration_id')
            config = storage.get_configuration_by_id(int(config_id))

            if not config:
                continue

            # Si la instancia no está en el diccionario, agregarla
            if instance_id not in instances_data:
                instances_data[instance_id] = {
                    'instance_id': instance_id,
                    'instance_name': instance.get('name', f'Instancia {instance_id}'),
                    'config_id': config_id,
                    'config_name': config.get('name', 'N/A'),
                    'consumptions': [],
                    'resources': {},  # Diccionario para consolidar recursos
                    'subtotal': 0.0
                }

            # Agregar consumo individual con fecha/hora
            instances_data[instance_id]['consumptions'].append({
                'date_time': date_time,
                'time_hours': time_hours  # Asegurar que sea el nombre correcto
            })

            # Consolidar recursos por instancia
            for res_config in config.get('resources', []):
                resource_id = res_config.get('resource_id')
                quantity = float(res_config.get('quantity', 0))

                # Buscar recurso
                resource = None
                for r in resources:
                    if str(r.get('id')) == str(resource_id):
                        resource = r
                        break

                if resource:
                    cost_per_hour = float(resource.get('value_per_hour', 0))
                    amount = quantity * cost_per_hour * time_hours

                    # Consolidar recurso
                    res_key = resource_id
                    if res_key not in instances_data[instance_id]['resources']:
                        instances_data[instance_id]['resources'][res_key] = {
                            'name': resource.get('name', 'N/A'),
                            'abbreviation': resource.get('abbreviation', ''),
                            'quantity': quantity,
                            'cost_per_hour': cost_per_hour,
                            'hours': 0.0,
                            'amount': 0.0
                        }
                    
                    # Sumar horas y monto
                    instances_data[instance_id]['resources'][res_key]['hours'] += time_hours
                    instances_data[instance_id]['resources'][res_key]['amount'] += amount
                    instances_data[instance_id]['subtotal'] += amount

        # Convertir diccionario a lista y convertir recursos de dict a list
        instances_list = []
        for inst in instances_data.values():
            inst['resources'] = list(inst['resources'].values())
            instances_list.append(inst)

        # Preparar datos para el PDF
        invoice_data = {
            'invoice': {
                'number': invoice.get('invoice_number'),
                'nit': invoice.get('client_nit'),
                'date': invoice.get('issue_date'),
                'total': float(invoice.get('total_amount', 0))
            },
            'client': {
                'name': client.get('name', 'N/A'),
                'nit': client.get('nit', 'N/A'),
                'address': client.get('address', 'N/A'),
                'email': client.get('email', 'N/A')
            },
            'instances': instances_list
        }

        # Generar PDF
        pdf_buffer = generate_invoice_detail_pdf(invoice_data)

        # Retornar PDF
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'factura_{invoice_id}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reporte/ventas', methods=['POST'])
def get_sales_report():

    try:
        from services.reports import generate_sales_analysis_pdf
        from datetime import datetime

        data = request.json
        analysis_type = data.get('type', 'categories')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')

        if not start_date_str or not end_date_str:
            return jsonify({'error': 'Fechas requeridas'}), 400

        # Parsear fechas
        try:
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
        except ValueError:
            return jsonify({'error': 'Formato de fecha invalido. Use dd/mm/yyyy'}), 400

        # Obtener facturas en el rango
        invoices = storage.get_invoices()
        filtered_invoices = []

        for invoice in invoices:
            invoice_date_str = invoice.get('issue_date', '')
            try:
                invoice_date = datetime.strptime(invoice_date_str, '%d/%m/%Y')
                if start_date <= invoice_date <= end_date:
                    filtered_invoices.append(invoice)
            except ValueError:
                continue

        if not filtered_invoices:
            return jsonify({'error': 'No hay facturas en el rango de fechas seleccionado'}), 404

        # Analizar segun tipo
        if analysis_type == 'categories':
            # Analisis por categorias y configuraciones
            analysis_items = analyze_by_categories(filtered_invoices, storage)
        else:
            # Analisis por recursos
            analysis_items = analyze_by_resources(filtered_invoices, storage)

        # Calcular totales y porcentajes
        total_revenue = sum(item['revenue'] for item in analysis_items)
        for item in analysis_items:
            if total_revenue > 0:
                item['percentage'] = (item['revenue'] / total_revenue) * 100
            else:
                item['percentage'] = 0.0

        # Ordenar por ingresos descendente
        analysis_items.sort(key=lambda x: x['revenue'], reverse=True)

        # Preparar datos para el PDF
        analysis_data = {
            'date_range': {
                'start': start_date_str,
                'end': end_date_str
            },
            'items': analysis_items,
            'total_revenue': total_revenue
        }

        # Generar PDF
        pdf_buffer = generate_sales_analysis_pdf(analysis_data, analysis_type)

        # Retornar PDF
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'analisis_ventas_{analysis_type}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def analyze_by_categories(invoices, storage):
    """Analiza ventas por categorias y configuraciones"""
    category_revenue = {}

    # Obtener todos los datos necesarios
    all_data = storage.get_all_data()
    consumptions = all_data.get('consumptions', [])

    for invoice in invoices:
        # Obtener consumptions usando consumption_ids como indices
        consumption_ids = invoice.get('consumption_ids', [])
        
        for cons_id_str in consumption_ids:
            try:
                cons_idx = int(cons_id_str)
                if 0 <= cons_idx < len(consumptions):
                    consumption = consumptions[cons_idx]
                else:
                    continue
            except (ValueError, IndexError):
                continue

            instance_id = consumption.get('instance_id')

            # Buscar cliente e instancia
            client_nit = invoice.get('client_nit')
            clients = all_data.get('clients', [])
            client = None
            for c in clients:
                if c.get('nit') == client_nit:
                    client = c
                    break

            if not client:
                continue

            instance = None
            for inst in client.get('instances', []):
                if str(inst.get('id')) == str(instance_id):
                    instance = inst
                    break

            if not instance:
                continue

            # Obtener configuracion
            config_id = instance.get('configuration_id')
            config = storage.get_configuration_by_id(config_id)

            if not config:
                continue

            # Obtener categoria
            category_id = config.get('category_id')
            category = storage.get_category_by_id(category_id)

            if not category:
                continue

            # Calcular ingresos
            hours = float(consumption.get('time_hours', 0))
            resources = all_data.get('resources', [])
            revenue = 0.0

            for res_config in config.get('resources', []):
                resource_id = res_config.get('resource_id')
                quantity = float(res_config.get('quantity', 0))

                resource = None
                for r in resources:
                    if str(r.get('id')) == str(resource_id):
                        resource = r
                        break

                if resource:
                    value_per_hour = float(resource.get('value_per_hour', 0))
                    revenue += quantity * value_per_hour * hours

            # Agregar a estadisticas
            key = f"{category.get('name', 'N/A')} - {config.get('name', 'N/A')}"
            if key not in category_revenue:
                category_revenue[key] = {
                    'name': key,
                    'description': config.get('description', 'N/A'),
                    'revenue': 0.0
                }
            category_revenue[key]['revenue'] += revenue

    return list(category_revenue.values())


def analyze_by_resources(invoices, storage):
    """Analiza ventas por recursos"""
    resource_revenue = {}

    # Obtener todos los datos necesarios
    all_data = storage.get_all_data()
    consumptions = all_data.get('consumptions', [])
    resources = all_data.get('resources', [])

    for invoice in invoices:
        # Obtener consumptions usando consumption_ids como indices
        consumption_ids = invoice.get('consumption_ids', [])
        
        for cons_id_str in consumption_ids:
            try:
                cons_idx = int(cons_id_str)
                if 0 <= cons_idx < len(consumptions):
                    consumption = consumptions[cons_idx]
                else:
                    continue
            except (ValueError, IndexError):
                continue

            instance_id = consumption.get('instance_id')

            # Buscar cliente e instancia
            client_nit = invoice.get('client_nit')
            clients = all_data.get('clients', [])
            client = None
            for c in clients:
                if c.get('nit') == client_nit:
                    client = c
                    break

            if not client:
                continue

            instance = None
            for inst in client.get('instances', []):
                if str(inst.get('id')) == str(instance_id):
                    instance = inst
                    break

            if not instance:
                continue

            # Obtener configuracion
            config_id = instance.get('configuration_id')
            config = storage.get_configuration_by_id(config_id)

            if not config:
                continue

            # Calcular ingresos por recurso
            hours = float(consumption.get('time_hours', 0))

            for res_config in config.get('resources', []):
                resource_id = res_config.get('resource_id')
                quantity = float(res_config.get('quantity', 0))

                # Buscar recurso
                resource = None
                for r in resources:
                    if str(r.get('id')) == str(resource_id):
                        resource = r
                        break

                if resource:
                    value_per_hour = float(resource.get('value_per_hour', 0))
                    revenue = quantity * value_per_hour * hours

                    # Agregar a estadisticas
                    key = resource.get('name', 'N/A')
                    if key not in resource_revenue:
                        resource_revenue[key] = {
                            'name': key,
                            'description': resource.get('type', 'N/A'),
                            'revenue': 0.0
                        }
                    resource_revenue[key]['revenue'] += revenue

    return list(resource_revenue.values())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
