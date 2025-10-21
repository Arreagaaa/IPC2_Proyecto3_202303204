"""
Script de pruebas para los endpoints del backend
Semana 2 - Release 2
"""
import requests
import json
from pathlib import Path

BACKEND_URL = 'http://127.0.0.1:5001'
DATA_DIR = Path(__file__).parent / 'backend' / 'instance' / 'data'

def print_separator(title):
    """Imprime un separador visual con título"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def test_initialize():
    """Prueba 1: Inicializar el sistema"""
    print_separator("PRUEBA 1: Inicializar Sistema")
    
    try:
        response = requests.post(f'{BACKEND_URL}/inicializar')
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_upload_configuration():
    """Prueba 2: Cargar configuraciones"""
    print_separator("PRUEBA 2: Cargar XML de Configuración")
    
    xml_file = DATA_DIR / 'example_config.xml'
    if not xml_file.exists():
        print(f"ERROR: No se encontró el archivo {xml_file}")
        return False
    
    try:
        with open(xml_file, 'rb') as f:
            content = f.read()
        
        response = requests.post(
            f'{BACKEND_URL}/configuracion',
            data=content,
            headers={'Content-Type': 'application/xml'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_upload_consumptions():
    """Prueba 3: Cargar consumos"""
    print_separator("PRUEBA 3: Cargar XML de Consumos")
    
    xml_file = DATA_DIR / 'example_consumos.xml'
    if not xml_file.exists():
        print(f"ERROR: No se encontró el archivo {xml_file}")
        return False
    
    try:
        with open(xml_file, 'rb') as f:
            content = f.read()
        
        response = requests.post(
            f'{BACKEND_URL}/consumo',
            data=content,
            headers={'Content-Type': 'application/xml'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_query_data():
    """Prueba 4: Consultar datos"""
    print_separator("PRUEBA 4: Consultar Datos del Sistema")
    
    try:
        response = requests.get(f'{BACKEND_URL}/consultar')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Mostrar resumen
            if 'summary' in data:
                print("\nRESUMEN DEL SISTEMA:")
                for key, value in data['summary'].items():
                    print(f"  {key}: {value}")
            
            # Mostrar recursos
            if 'resources' in data and data['resources']:
                print(f"\nRECURSOS ({len(data['resources'])}):")
                for res in data['resources']:
                    print(f"  - ID {res['id']}: {res['name']} ({res['type']}) - ${res['value_per_hour']}/hora")
            
            # Mostrar categorías
            if 'categories' in data and data['categories']:
                print(f"\nCATEGORÍAS ({len(data['categories'])}):")
                for cat in data['categories']:
                    print(f"  - ID {cat['id']}: {cat['name']}")
                    if cat['configurations']:
                        for config in cat['configurations']:
                            print(f"    * Configuración {config['id']}: {config['name']}")
            
            # Mostrar clientes
            if 'clients' in data and data['clients']:
                print(f"\nCLIENTES ({len(data['clients'])}):")
                for client in data['clients']:
                    print(f"  - NIT {client['nit']}: {client['name']}")
                    if client['instances']:
                        for inst in client['instances']:
                            print(f"    * Instancia {inst['id']}: {inst['name']} ({inst['status']})")
            
            # Mostrar consumos
            if 'consumptions' in data and data['consumptions']:
                print(f"\nCONSUMOS ({len(data['consumptions'])}):")
                for cons in data['consumptions']:
                    print(f"  - NIT {cons['nit']}, Instancia {cons['instance_id']}: {cons['time_hours']} horas ({cons['date_time']})")
        
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "*"*70)
    print("  SCRIPT DE PRUEBAS - BACKEND API")
    print("  Semana 2 - Release 2")
    print("*"*70)
    
    print("\nAsegúrese de que el backend esté corriendo en http://127.0.0.1:5001")
    input("Presione Enter para continuar...")
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Inicializar Sistema", test_initialize()))
    results.append(("Cargar Configuración", test_upload_configuration()))
    results.append(("Cargar Consumos", test_upload_consumptions()))
    results.append(("Consultar Datos", test_query_data()))
    
    # Mostrar resumen de resultados
    print_separator("RESUMEN DE PRUEBAS")
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "OK" if result else "FALLO"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed} exitosas, {failed} fallidas de {len(results)} pruebas")
    
    if failed == 0:
        print("\n¡Todas las pruebas pasaron exitosamente!")
    else:
        print(f"\n{failed} prueba(s) fallaron. Revise los errores arriba.")

if __name__ == '__main__':
    main()
