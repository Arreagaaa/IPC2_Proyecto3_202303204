from datetime import datetime
from typing import Dict, List, Tuple
from models.storage import XMLStorage


class BillingService:
    def __init__(self, storage: XMLStorage):
        self.storage = storage

    def parse_date(self, date_str: str) -> datetime:
        """
        Convierte string de fecha en formato dd/mm/yyyy a datetime
        """
        try:
            return datetime.strptime(date_str.strip(), '%d/%m/%Y')
        except ValueError:
            # Intentar con formato dd/mm/yyyy hh:mm
            try:
                parts = date_str.strip().split(' ')
                return datetime.strptime(parts[0], '%d/%m/%Y')
            except:
                raise ValueError(f"Formato de fecha inválido: {date_str}")

    def is_date_in_range(self, date_str: str, start_date: str, end_date: str) -> bool:
        """
        Verifica si una fecha está dentro de un rango
        """
        try:
            date = self.parse_date(date_str)
            start = self.parse_date(start_date)
            end = self.parse_date(end_date)
            return start <= date <= end
        except:
            return False

    def calculate_consumption_cost(self, consumption: Dict) -> Tuple[float, Dict]:
        """
        Calcula el costo de un consumo individual
        Retorna: (costo_total, detalle_por_recurso)
        """
        # Obtener instancia
        instance = self.storage.get_instance_by_id(
            consumption['nit'], consumption['instance_id'])
        if not instance:
            return 0.0, {}

        # Obtener configuración
        config = self.storage.get_configuration_by_id(
            instance['configuration_id'])
        if not config:
            return 0.0, {}

        # Calcular costo por recurso
        time_hours = float(consumption['time_hours'])
        total_cost = 0.0
        resource_details = {}

        for config_res in config['resources']:
            resource = self.storage.get_resource_by_id(
                config_res['resource_id'])
            if resource:
                quantity = config_res['quantity']
                cost_per_hour = resource['value_per_hour']
                resource_cost = quantity * cost_per_hour * time_hours

                total_cost += resource_cost
                resource_details[resource['id']] = {
                    'name': resource['name'],
                    'quantity': quantity,
                    'cost_per_hour': cost_per_hour,
                    'time_hours': time_hours,
                    'total_cost': resource_cost
                }

        return total_cost, resource_details

    def generate_invoices(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Genera facturas para todos los clientes según consumos en el rango de fechas
        Retorna lista de facturas generadas
        """
        # Obtener consumos no facturados
        unbilled = self.storage.get_unbilled_consumptions()

        # Filtrar por rango de fechas
        consumptions_in_range = []
        for cons in unbilled:
            if self.is_date_in_range(cons['date_time'], start_date, end_date):
                consumptions_in_range.append(cons)

        if not consumptions_in_range:
            return []

        # Agrupar por cliente
        clients_consumptions = {}
        for cons in consumptions_in_range:
            nit = cons['nit']
            if nit not in clients_consumptions:
                clients_consumptions[nit] = []
            clients_consumptions[nit].append(cons)

        # Generar facturas
        invoices = []
        existing_invoices = self.storage.get_invoices()
        next_invoice_number = len(existing_invoices) + 1

        for nit, consumptions in clients_consumptions.items():
            total_amount = 0.0
            consumption_ids = []
            details = []

            for cons in consumptions:
                cost, resource_details = self.calculate_consumption_cost(cons)
                total_amount += cost
                consumption_ids.append(cons['id'])
                details.append({
                    'consumption_id': cons['id'],
                    'instance_id': cons['instance_id'],
                    'time_hours': cons['time_hours'],
                    'date_time': cons['date_time'],
                    'cost': cost,
                    'resources': resource_details
                })

            # Crear factura
            invoice_number = f"FAC-{next_invoice_number:06d}"
            next_invoice_number += 1

            # Guardar en storage
            self.storage.add_invoice(
                invoice_number=invoice_number,
                client_nit=nit,
                issue_date=end_date,
                total_amount=total_amount,
                consumption_ids=consumption_ids
            )

            invoices.append({
                'invoice_number': invoice_number,
                'client_nit': nit,
                'issue_date': end_date,
                'total_amount': total_amount,
                'consumptions_count': len(consumptions),
                'details': details
            })

        return invoices

    def get_invoice_detail(self, invoice_number: str) -> Dict:
        """
        Obtiene el detalle completo de una factura
        """
        invoices = self.storage.get_invoices()

        for invoice in invoices:
            if invoice['invoice_number'] == invoice_number:
                # Reconstruir detalles desde consumos
                details = []
                total_by_instance = {}
                total_by_resource = {}

                for cons_id in invoice['consumption_ids']:
                    # Buscar consumo en storage (necesitamos implementar get_consumption_by_id)
                    # Por ahora retornamos la info básica
                    pass

                return {
                    **invoice,
                    'details': details,
                    'total_by_instance': total_by_instance,
                    'total_by_resource': total_by_resource
                }

        return None
