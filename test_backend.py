#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar los endpoints del backend
"""

import requests
import json

BACKEND_URL = 'http://127.0.0.1:5001'

def test_endpoint(name, url):
    """Prueba un endpoint del backend"""
    print(f"\n{'='*60}")
    print(f"Probando: {name}")
    print(f"URL: {url}")
    print('='*60)
    
    try:
        response = requests.get(url, timeout=2)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Respuesta:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar al backend")
        print("¿Está corriendo Flask en el puerto 5001?")
        print("\nPara iniciar el backend:")
        print("  cd backend")
        print("  python app.py")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║         TEST DEL BACKEND - IPC2 PROYECTO 3            ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Test 1: Summary
    test_endpoint("RESUMEN (Summary)", f"{BACKEND_URL}/summary")
    
    # Test 2: Consultar Datos
    test_endpoint("CONSULTAR DATOS COMPLETOS", f"{BACKEND_URL}/consultar")
    
    print(f"\n{'='*60}")
    print("Tests completados")
    print('='*60)

if __name__ == '__main__':
    main()
