from flask import Flask, request, jsonify, Response
from pathlib import Path
from models import parser
from models.storage import XMLStorage

app = Flask(__name__)

DATA_DIR = Path(__file__).resolve().parent / 'instance' / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = DATA_DIR / 'db.xml'

# Inicializar almacenamiento
storage = XMLStorage(DB_FILE)


@app.route('/api/crearConfiguracion', methods=['POST'])
def create_configuration():
    # Recibe XML de configuración, lo parsea y almacena en db.xml
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


@app.route('/api/consumos', methods=['POST'])
def create_consumptions():
    # Recibe XML de consumos, lo parsea y almacena en db.xml
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


@app.route('/api/consultarDatos', methods=['GET'])
def query_data():
    summary = storage.get_summary()
    return jsonify(summary)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
