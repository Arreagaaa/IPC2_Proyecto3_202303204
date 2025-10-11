"""
Manual test for validation and parsing (TEST B and C)
This test validates NIT, date extraction, and full entity parsing without needing backend running
"""

from backend.models.validators import validate_nit, extract_first_date, extract_first_datetime
from backend.models.parser import parse_configurations_xml

print("=" * 60)
print("TEST B: Validacion de NIT y extraccion de fechas")
print("=" * 60)

# Test NIT validation
test_nits = [
    ("34300-4", True),
    ("110339001-K", True),
    ("123-X", False),
    ("123", False),
    ("abc-4", False)
]

print("\nValidacion de NITs:")
for nit, expected in test_nits:
    result = validate_nit(nit)
    status = "PASS" if result == expected else "FAIL"
    print(f"  {nit}: {result} [{status}]")

# Test date extraction
test_dates = [
    "01/01/2025",
    "Guatemala, 15/03/2024",
    "en la ciudad de Guatemala, 20/12/2023 se brinda el servicio",
    "No hay fecha aqui"
]

print("\nExtraccion de fechas:")
for text in test_dates:
    date = extract_first_date(text)
    print(f"  '{text[:50]}...' -> {date}")

# Test datetime extraction
test_datetimes = [
    "01/01/2025 14:30",
    "Inicio: 15/03/2024 08:45 fin",
    "Solo fecha 20/12/2023"
]

print("\nExtraccion de fecha y hora:")
for text in test_datetimes:
    result = extract_first_datetime(text)
    print(f"  '{text}' -> {result}")

print("\n" + "=" * 60)
print("TEST C: Parseo completo de entidades")
print("=" * 60)

# Read and parse example XML
with open('backend/instance/data/example_config.xml', 'r', encoding='utf-8') as f:
    xml_content = f.read()

resources, categories, clients, counts = parse_configurations_xml(xml_content)

print(f"\nResultados del parseo:")
print(f"  Recursos: {len(resources)}")
for res in resources:
    print(f"    - {res.name} ({res.abbreviation}): ${res.value_per_hour}/hora")

print(f"\n  Categorias: {len(categories)}")
for cat in categories:
    print(f"    - {cat.name}: {len(cat.configurations)} configuraciones")
    for config in cat.configurations:
        print(f"      * {config.name}: {len(config.resources)} recursos")

print(f"\n  Clientes: {len(clients)}")
for client in clients:
    print(f"    - {client.name} (NIT: {client.nit}): {len(client.instances)} instancias")
    for inst in client.instances:
        print(f"      * {inst.name} (Config ID: {inst.configuration_id}, Estado: {inst.status})")

print(f"\nConteos totales: {counts}")

print("\n" + "=" * 60)
print("TESTS B y C: COMPLETADOS")
print("=" * 60)
