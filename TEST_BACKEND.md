# 🧪 INSTRUCCIONES DE PRUEBA

## ✅ ERRORES CORREGIDOS

### 1. Tabla de recursos duplicada ✅
**Problema:** En `/consultar/` salían filas extra con solo ID y $

**Causa:** El XPath `.//resources/resource` buscaba recursivamente y encontraba tanto los recursos del sistema como los recursos dentro de las configuraciones.

**Solución:** Cambiado a `./resources/resource` (sin la doble barra) para buscar solo en el nivel inmediato.

**Archivo:** `backend/models/storage.py` línea 210

### 2. Dashboard muestra 0 ✅
**Problema:** Las tarjetas del dashboard siempre mostraban 0

**Causa:** El template no tenía valores por defecto cuando `summary` está vacío o no se carga

**Solución:** Agregado filtro `|default:0` en todas las tarjetas

**Archivos modificados:**
- `backend/app.py` - Endpoint `/summary` ya existía (línea 477-505)
- `frontend/app/views.py` - Vista `index()` ya llamaba al endpoint (línea 10-23)
- `frontend/app/templates/index.html` - Agregados filtros `|default:0` (líneas 71, 97, 122, 147)

---

## 🔧 PARA PROBAR LOS CAMBIOS:

### **1. Reiniciar Backend Flask**
```bash
# Si está corriendo, presiona Ctrl+C
cd backend
python app.py
```

### **2. Reiniciar Frontend Django**
```bash
# Si está corriendo, presiona Ctrl+C  
cd frontend
python manage.py runserver
```

### **3. Prueba Completa**

**a) Cargar Configuración**
1. Ir a `http://localhost:8000/configuracion/`
2. Cargar `backend/instance/data/example_config.xml`
3. Debería decir: ✓ 2 recursos, 1 categoría, 2 clientes, 2 instancias

**b) Verificar Dashboard**
1. Ir a `http://localhost:8000/`
2. Debería mostrar:
   ```
   Recursos: 2
   Clientes: 2
   Instancias: 2
   Facturas: 0
   ```

**c) Verificar Tabla de Recursos**
1. Ir a `http://localhost:8000/consultar/`
2. En la tabla de "Recursos" deberías ver SOLO 2 filas:
   ```
   ID | Nombre      | Abrev | Métrica  | Tipo     | Valor/Hora
   1  | Memoria RAM | GiB   | GiB      | Hardware | $0.75
   2  | Núcleos     | cores | unidades | Hardware | $1.2
   ```
3. **NO** deberían aparecer filas extra con solo "1" y "2" vacías

**d) Cargar Consumos**
1. Ir a `http://localhost:8000/consumo/`
2. Cargar `backend/instance/data/example_consumos.xml`
3. Debería decir: ✓ 5 consumos registrados

**e) Facturar**
1. Ir a `http://localhost:8000/facturar/`
2. Fechas: 01/01/2025 a 31/01/2025
3. Debería generar:
   ```
   FAC-000001 | 110339001-K | $33.75
   FAC-000002 | 85125-K     | $68.85
   ```

**f) Verificar Dashboard Final**
1. Ir a `http://localhost:8000/`
2. Debería mostrar:
   ```
   Recursos: 2
   Clientes: 2
   Instancias: 2
   Facturas: 2   <-- ¡Actualizado!
   ```

---

## 🐛 SI TODAVÍA SALE MAL:

### Dashboard sigue en 0:
```python
# Verificar en backend/app.py que existe el endpoint /summary (línea 477)
# Verificar en frontend/app/views.py que la función index() llame al backend (línea 14)
# Asegurarse de que ambos servidores estén corriendo
```

### Tabla de recursos duplicada:
```python
# Verificar en backend/models/storage.py línea 210:
# Debe decir: config_node.findall('./resources/resource')
# NO debe decir: config_node.findall('.//resources/resource')
```

---

## 📊 DATOS ESPERADOS DESPUÉS DE FACTURAR:

```
RESUMEN DEL SISTEMA:
- Recursos: 2
- Categorías: 1  
- Configuraciones: 1
- Clientes: 2
- Instancias: 2
- Consumos: 5

RECURSOS:
1. Memoria RAM - GiB - $0.75/hora
2. Núcleos - cores - $1.20/hora

CATEGORÍAS:
- VM Desarrollo (ID: 10)
  └─ Dev Basic (ID: 100)
     ├─ Recurso 1 (RAM): 4.0 GiB
     └─ Recurso 2 (Núcleos): 2.0 unidades

CLIENTES:
1. ACME (110339001-K)
   └─ acme-dev-1 (ID: 500) - Vigente

2. JAKES Inc. (85125-K)
   └─ jakes-prod-1 (ID: 555) - Vigente

FACTURAS:
1. FAC-000001 - ACME - $33.75
2. FAC-000002 - JAKES Inc. - $68.85
```

---

**¡Con esto ya debería funcionar todo correctamente! 🚀**
