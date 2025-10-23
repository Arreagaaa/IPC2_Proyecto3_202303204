from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Resource:
    id: int
    name: str
    abbreviation: str
    metric: str
    type: str  # 'Hardware' o 'Software'
    value_per_hour: float


@dataclass
class ConfigurationResource:
    resource_id: int
    quantity: float


@dataclass
class Configuration:
    id: int
    name: str
    description: Optional[str] = None
    resources: List[ConfigurationResource] = field(default_factory=list)


@dataclass
class Category:
    id: int
    name: str
    description: Optional[str] = None
    workload: Optional[str] = None
    configurations: List[Configuration] = field(default_factory=list)


@dataclass
class Instance:
    id: int
    configuration_id: int
    name: str
    start_date: Optional[str] = None
    status: str = 'Vigente'  # o 'Cancelada'
    end_date: Optional[str] = None


@dataclass
class Client:
    nit: str
    name: str
    username: str
    password: str
    address: Optional[str] = None
    email: Optional[str] = None
    instances: List[Instance] = field(default_factory=list)


@dataclass
class Invoice:
    invoice_number: str  # Número único de factura
    client_nit: str
    issue_date: str  # Fecha de emisión (último día del rango)
    total_amount: float
    consumptions_ids: List[str] = field(
        default_factory=list)  # IDs de consumos facturados
