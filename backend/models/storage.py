import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List
from .domain import Resource, Configuration, ConfigurationResource, Category, Instance, Client
from .validators import validate_nit, extract_first_date


class XMLStorage:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.ensure_db()

    def ensure_db(self):
        # Crear archivo si no existe
        if not self.db_path.exists():
            root = ET.Element('database')
            ET.SubElement(root, 'resources')
            ET.SubElement(root, 'categories')
            ET.SubElement(root, 'clients')
            ET.SubElement(root, 'consumptions')
            tree = ET.ElementTree(root)
            tree.write(self.db_path, encoding='utf-8', xml_declaration=True)

    def load_tree(self) -> ET.ElementTree:
        # Cargar XML desde archivo
        return ET.parse(self.db_path)

    def save_tree(self, tree: ET.ElementTree):
        # Guardar XML en archivo
        tree.write(self.db_path, encoding='utf-8', xml_declaration=True)

    def add_resources(self, resources: List[Resource]):
        # Agregar recursos a la base de datos
        tree = self.load_tree()
        root = tree.getroot()
        resources_node = root.find('resources')
        if resources_node is None:
            resources_node = ET.SubElement(root, 'resources')

        for res in resources:
            # Verificar si ya existe
            existing = resources_node.find(f".//resource[@id='{res.id}']")
            if existing is not None:
                resources_node.remove(existing)

            res_node = ET.SubElement(resources_node, 'resource')
            res_node.set('id', str(res.id))
            ET.SubElement(res_node, 'name').text = res.name
            ET.SubElement(res_node, 'abbreviation').text = res.abbreviation
            ET.SubElement(res_node, 'metric').text = res.metric
            ET.SubElement(res_node, 'type').text = res.type
            ET.SubElement(res_node, 'value_per_hour').text = str(
                res.value_per_hour)

        self.save_tree(tree)

    def add_categories(self, categories: List[Category]):
        # Agregar categorias con configuraciones a la base de datos
        tree = self.load_tree()
        root = tree.getroot()
        categories_node = root.find('categories')
        if categories_node is None:
            categories_node = ET.SubElement(root, 'categories')

        for cat in categories:
            # Verificar si ya existe
            existing = categories_node.find(f".//category[@id='{cat.id}']")
            if existing is not None:
                categories_node.remove(existing)

            cat_node = ET.SubElement(categories_node, 'category')
            cat_node.set('id', str(cat.id))
            ET.SubElement(cat_node, 'name').text = cat.name
            ET.SubElement(cat_node, 'description').text = cat.description or ''
            ET.SubElement(cat_node, 'workload').text = cat.workload or ''

            configs_node = ET.SubElement(cat_node, 'configurations')
            for config in cat.configurations:
                config_node = ET.SubElement(configs_node, 'configuration')
                config_node.set('id', str(config.id))
                ET.SubElement(config_node, 'name').text = config.name
                ET.SubElement(
                    config_node, 'description').text = config.description or ''

                resources_node = ET.SubElement(config_node, 'resources')
                for config_res in config.resources:
                    res_node = ET.SubElement(resources_node, 'resource')
                    res_node.set('id', str(config_res.resource_id))
                    res_node.text = str(config_res.quantity)

        self.save_tree(tree)

    def add_clients(self, clients: List[Client]):
        # Agregar clientes con instancias a la base de datos
        tree = self.load_tree()
        root = tree.getroot()
        clients_node = root.find('clients')
        if clients_node is None:
            clients_node = ET.SubElement(root, 'clients')

        for client in clients:
            # Verificar si ya existe
            existing = clients_node.find(f".//client[@nit='{client.nit}']")
            if existing is not None:
                clients_node.remove(existing)

            client_node = ET.SubElement(clients_node, 'client')
            client_node.set('nit', client.nit)
            ET.SubElement(client_node, 'name').text = client.name
            ET.SubElement(client_node, 'username').text = client.username
            ET.SubElement(client_node, 'password').text = client.password
            ET.SubElement(client_node, 'address').text = client.address or ''
            ET.SubElement(client_node, 'email').text = client.email or ''

            instances_node = ET.SubElement(client_node, 'instances')
            for instance in client.instances:
                inst_node = ET.SubElement(instances_node, 'instance')
                inst_node.set('id', str(instance.id))
                ET.SubElement(inst_node, 'configuration_id').text = str(
                    instance.configuration_id)
                ET.SubElement(inst_node, 'name').text = instance.name
                ET.SubElement(
                    inst_node, 'start_date').text = instance.start_date or ''
                ET.SubElement(inst_node, 'status').text = instance.status
                ET.SubElement(
                    inst_node, 'end_date').text = instance.end_date or ''

        self.save_tree(tree)

    def add_consumption(self, nit: str, instance_id: str, time_hours: str, date_time: str):
        # Agregar consumo a la base de datos
        tree = self.load_tree()
        root = tree.getroot()
        consumptions_node = root.find('consumptions')
        if consumptions_node is None:
            consumptions_node = ET.SubElement(root, 'consumptions')

        cons_node = ET.SubElement(consumptions_node, 'consumption')
        cons_node.set('nit', nit)
        cons_node.set('instance_id', instance_id)
        ET.SubElement(cons_node, 'time_hours').text = time_hours
        ET.SubElement(cons_node, 'date_time').text = date_time

        self.save_tree(tree)

    def get_summary(self) -> Dict[str, int]:
        # Obtener conteos de entidades
        tree = self.load_tree()
        root = tree.getroot()

        resources_count = len(root.findall('.//resources/resource'))
        categories_count = len(root.findall('.//categories/category'))
        configurations_count = len(root.findall(
            './/categories/category/configurations/configuration'))
        clients_count = len(root.findall('.//clients/client'))
        instances_count = len(root.findall(
            './/clients/client/instances/instance'))
        consumptions_count = len(root.findall('.//consumptions/consumption'))

        return {
            'resources': resources_count,
            'categories': categories_count,
            'configurations': configurations_count,
            'clients': clients_count,
            'instances': instances_count,
            'consumptions': consumptions_count
        }

    def clear_all(self):
        """
        Limpia todos los datos de la base de datos
        Reinicia la estructura XML a su estado inicial
        """
        root = ET.Element('database')
        ET.SubElement(root, 'resources')
        ET.SubElement(root, 'categories')
        ET.SubElement(root, 'clients')
        ET.SubElement(root, 'consumptions')
        tree = ET.ElementTree(root)
        tree.write(self.db_path, encoding='utf-8', xml_declaration=True)

    def get_all_data(self) -> Dict:
        """
        Obtiene todos los datos almacenados en formato estructurado
        Retorna diccionario con recursos, categorías, clientes, consumos
        """
        tree = self.load_tree()
        root = tree.getroot()

        # Obtener recursos
        resources = []
        for res_node in root.findall('.//resources/resource'):
            resources.append({
                'id': res_node.get('id'),
                'name': res_node.find('name').text if res_node.find('name') is not None else '',
                'abbreviation': res_node.find('abbreviation').text if res_node.find('abbreviation') is not None else '',
                'metric': res_node.find('metric').text if res_node.find('metric') is not None else '',
                'type': res_node.find('type').text if res_node.find('type') is not None else '',
                'value_per_hour': res_node.find('value_per_hour').text if res_node.find('value_per_hour') is not None else ''
            })

        # Obtener categorías con configuraciones
        categories = []
        for cat_node in root.findall('.//categories/category'):
            configurations = []
            for config_node in cat_node.findall('.//configurations/configuration'):
                config_resources = []
                for res_node in config_node.findall('.//resources/resource'):
                    config_resources.append({
                        'resource_id': res_node.get('id'),
                        'quantity': res_node.text
                    })

                configurations.append({
                    'id': config_node.get('id'),
                    'name': config_node.find('name').text if config_node.find('name') is not None else '',
                    'description': config_node.find('description').text if config_node.find('description') is not None else '',
                    'resources': config_resources
                })

            categories.append({
                'id': cat_node.get('id'),
                'name': cat_node.find('name').text if cat_node.find('name') is not None else '',
                'description': cat_node.find('description').text if cat_node.find('description') is not None else '',
                'workload': cat_node.find('workload').text if cat_node.find('workload') is not None else '',
                'configurations': configurations
            })

        # Obtener clientes con instancias
        clients = []
        for client_node in root.findall('.//clients/client'):
            instances = []
            for inst_node in client_node.findall('.//instances/instance'):
                instances.append({
                    'id': inst_node.get('id'),
                    'configuration_id': inst_node.find('configuration_id').text if inst_node.find('configuration_id') is not None else '',
                    'name': inst_node.find('name').text if inst_node.find('name') is not None else '',
                    'start_date': inst_node.find('start_date').text if inst_node.find('start_date') is not None else '',
                    'status': inst_node.find('status').text if inst_node.find('status') is not None else '',
                    'end_date': inst_node.find('end_date').text if inst_node.find('end_date') is not None else ''
                })

            clients.append({
                'nit': client_node.get('nit'),
                'name': client_node.find('name').text if client_node.find('name') is not None else '',
                'username': client_node.find('username').text if client_node.find('username') is not None else '',
                'password': client_node.find('password').text if client_node.find('password') is not None else '',
                'address': client_node.find('address').text if client_node.find('address') is not None else '',
                'email': client_node.find('email').text if client_node.find('email') is not None else '',
                'instances': instances
            })

        # Obtener consumos
        consumptions = []
        for cons_node in root.findall('.//consumptions/consumption'):
            consumptions.append({
                'nit': cons_node.get('nit'),
                'instance_id': cons_node.get('instance_id'),
                'time_hours': cons_node.find('time_hours').text if cons_node.find('time_hours') is not None else '',
                'date_time': cons_node.find('date_time').text if cons_node.find('date_time') is not None else ''
            })

        return {
            'resources': resources,
            'categories': categories,
            'clients': clients,
            'consumptions': consumptions,
            'summary': self.get_summary()
        }
