from flask import Flask, request, jsonify, Response
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


# Endpoint para configuraciones (version completa)
@app.route('/configuracion', methods=['POST'])
@app.route('/api/crearConfiguracion', methods=['POST'])
def create_configuration():
    """
    Recibe XML de configuración, lo parsea y almacena en db.xml
    XML debe contener: recursos, categorías, configuraciones, clientes, instancias
    """
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
    """
    Recibe XML de consumos, lo parsea y almacena en db.xml
    XML debe contener: consumos con NIT, idInstancia, tiempo, fechaHora
    """
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
    """
    Limpia todos los datos de la base de datos XML
    Reinicia el sistema a estado inicial
    """
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
    """
    Devuelve todos los datos actuales del sistema en formato JSON
    Incluye: recursos, categorías, configuraciones, clientes, instancias, consumos
    """
    try:
        data = storage.get_all_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========== NUEVOS ENDPOINTS SEMANA 3 ==========

# Endpoint para crear recurso individual (CRUD)
@app.route('/api/crearRecurso', methods=['POST'])
def create_resource():
    """
    Crea un recurso individual
    Body JSON: {id, name, abbreviation, metric, type, value_per_hour}
    """
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
    """
    Crea una categoría con sus configuraciones
    Body JSON: {id, name, description, workload, configurations: [{...}]}
    """
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


# Endpoint para crear cliente (CRUD)
@app.route('/api/crearCliente', methods=['POST'])
def create_client():
    """
    Crea un cliente individual
    Body JSON: {nit, name, username, password, address, email}
    """
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
    """
    Crea una instancia para un cliente existente
    Body JSON: {client_nit, id, configuration_id, name, start_date}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        required = ['client_nit', 'id', 'configuration_id', 'name', 'start_date']
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
    """
    Cancela una instancia existente
    Body JSON: {client_nit, instance_id, end_date}
    """
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
    """
    Genera facturas para un rango de fechas
    Body JSON: {start_date, end_date}
    Formato de fechas: dd/mm/yyyy
    """
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
    """
    Obtiene todas las facturas generadas
    """
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
def get_unbilled_consumptions():
    """
    Obtiene todos los consumos que no han sido facturados
    """
    try:
        consumptions = storage.get_unbilled_consumptions()
        return jsonify({
            'status': 'ok',
            'consumptions': consumptions,
            'count': len(consumptions)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
