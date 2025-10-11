import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple
from .domain import Resource, Configuration, ConfigurationResource, Category, Instance, Client
from .validators import extract_first_date, extract_first_datetime, validate_nit


def parse_configurations_xml(xml_text: str) -> Tuple[List[Resource], List[Category], List[Client], Dict[str, int]]:
    # Parsea el XML de configuraciones y retorna listas de recursos, categorias y clientes junto con conteos
    root = ET.fromstring(xml_text)

    resources = []
    categories = []
    clients = []

    counts = {
        'resources': 0,
        'categories': 0,
        'configurations': 0,
        'clients': 0,
        'instances': 0,
    }

    # Parsear recursos
    resource_list_node = root.find('listaRecursos')
    if resource_list_node is not None:
        for res_node in resource_list_node.findall('recurso'):
            res_id = int(res_node.get('id', '0'))
            name = res_node.findtext('nombre', '')
            abbr = res_node.findtext('abreviatura', '')
            metric = res_node.findtext('metrica', '')
            res_type = res_node.findtext('tipo', 'Hardware')
            value_per_hour = float(res_node.findtext('valorXhora', '0'))

            resources.append(Resource(
                id=res_id,
                name=name,
                abbreviation=abbr,
                metric=metric,
                type=res_type,
                value_per_hour=value_per_hour
            ))
        counts['resources'] = len(resources)

    # Parsear categorias con configuraciones
    category_list_node = root.find('listaCategorias')
    if category_list_node is not None:
        for cat_node in category_list_node.findall('categoria'):
            cat_id = int(cat_node.get('id', '0'))
            cat_name = cat_node.findtext('nombre', '')
            cat_desc = cat_node.findtext('descripcion', '')
            cat_workload = cat_node.findtext('cargaTrabajo', '')

            configurations = []
            config_list_node = cat_node.find('listaConfiguraciones')
            if config_list_node is not None:
                for config_node in config_list_node.findall('configuracion'):
                    config_id = int(config_node.get('id', '0'))
                    config_name = config_node.findtext('nombre', '')
                    config_desc = config_node.findtext('descripcion', '')

                    config_resources = []
                    resources_node = config_node.find('recursosConfiguracion')
                    if resources_node is not None:
                        for res_node in resources_node.findall('recurso'):
                            res_id = int(res_node.get('id', '0'))
                            quantity = float(res_node.text or '0')
                            config_resources.append(ConfigurationResource(
                                resource_id=res_id,
                                quantity=quantity
                            ))

                    configurations.append(Configuration(
                        id=config_id,
                        name=config_name,
                        description=config_desc,
                        resources=config_resources
                    ))

            categories.append(Category(
                id=cat_id,
                name=cat_name,
                description=cat_desc,
                workload=cat_workload,
                configurations=configurations
            ))
        counts['categories'] = len(categories)
        counts['configurations'] = sum(
            len(c.configurations) for c in categories)

    # Parsear clientes con instancias
    client_list_node = root.find('listaClientes')
    if client_list_node is not None:
        for client_node in client_list_node.findall('cliente'):
            nit = client_node.get('nit', '')
            if not validate_nit(nit):
                continue  # Saltar NIT invalido

            name = client_node.findtext('nombre', '')
            username = client_node.findtext('usuario', '')
            password = client_node.findtext('clave', '')
            address = client_node.findtext('direccion', '')
            email = client_node.findtext('correoElectronico', '')

            instances = []
            instance_list_node = client_node.find('listaInstancias')
            if instance_list_node is not None:
                for inst_node in instance_list_node.findall('instancia'):
                    inst_id = int(inst_node.get('id', '0'))
                    config_id = int(inst_node.findtext('idConfiguracion', '0'))
                    inst_name = inst_node.findtext('nombre', '')
                    start_date_text = inst_node.findtext('fechaInicio', '')
                    start_date = extract_first_date(start_date_text)
                    status = inst_node.findtext('estado', 'Vigente')
                    end_date_text = inst_node.findtext('fechaFinal', '')
                    end_date = extract_first_date(
                        end_date_text) if end_date_text else None

                    instances.append(Instance(
                        id=inst_id,
                        configuration_id=config_id,
                        name=inst_name,
                        start_date=start_date,
                        status=status,
                        end_date=end_date
                    ))

            clients.append(Client(
                nit=nit,
                name=name,
                username=username,
                password=password,
                address=address,
                email=email,
                instances=instances
            ))
        counts['clients'] = len(clients)
        counts['instances'] = sum(len(c.instances) for c in clients)

    return resources, categories, clients, counts


def parse_consumptions_xml(xml_text: str) -> List[Dict[str, str]]:
    # Parsea el XML de consumos y retorna una lista de diccionarios con datos validados
    root = ET.fromstring(xml_text)
    result = []
    for consumption in root.findall('consumo'):
        nit = consumption.get('nitCliente') or consumption.get('nit') or ''
        if not validate_nit(nit):
            continue  # Saltar NIT invalido

        instance_id = consumption.get(
            'idInstancia') or consumption.get('id') or ''
        time_value = None
        date_time_str = None

        time_node = consumption.find('tiempo')
        if time_node is not None:
            time_value = time_node.text

        datetime_node = consumption.find('fechaHora')
        if datetime_node is not None:
            dt_text = datetime_node.text
            dt_extracted = extract_first_datetime(dt_text)
            if dt_extracted:
                date_part, time_part = dt_extracted
                date_time_str = f"{date_part} {time_part}"
            else:
                date_time_str = dt_text

        result.append({
            'nit': nit,
            'instance_id': instance_id,
            'time': time_value or '0',
            'date_time': date_time_str or ''
        })
    return result
