# 📊 SEMANA 3 - RELEASE 3: FACTURACIÓN Y CRUD COMPLETO
## Sistema de Facturación de Infraestructura en la Nube

**Carnet:** 202303204  
**Curso:** IPC2 - USAC  
**Empresa:** Tecnologías Chapinas S.A.

---

## 🎯 OBJETIVOS CUMPLIDOS

### ✅ Facturación Automática
- Generación de facturas por rango de fechas
- Cálculo de montos por cliente, configuración y recurso
- Registro de facturas en XML con números únicos
- Marcado de consumos como facturados

### ✅ CRUD Manual Completo
- Crear recursos individuales
- Crear categorías con configuraciones
- Registrar clientes nuevos
- Crear instancias para clientes
- Cancelar instancias existentes

### ✅ Interfaz Django Completa
- Selector de rango de fechas para facturación
- Formularios para CRUD de todos los elementos
- Vista de consulta mejorada con consumos pendientes
- Vista de facturas generadas

---

## 🔧 IMPLEMENTACIÓN BACKEND

### 1. Nuevos Modelos (`backend/models/domain.py`)

#### Modelo de Factura
```python
@dataclass
class Invoice:
    invoice_number: str  # FAC-000001
    client_nit: str
    issue_date: str  # dd/mm/yyyy
    total_amount: float
    consumptions_ids: List[str]  # Consumos facturados
```

### 2. Almacenamiento (`backend/models/storage.py`)

#### Métodos Nuevos:
- **`add_invoice()`** - Agregar factura y marcar consumos como facturados
- **`get_unbilled_consumptions()`** - Obtener consumos pendientes de facturar
- **`get_invoices()`** - Consultar todas las facturas
- **`cancel_instance()`** - Cambiar estado de instancia a "Cancelada"
- **`get_resource_by_id()`** - Obtener recurso específico
- **`get_configuration_by_id()`** - Obtener configuración específica
- **`get_instance_by_id()`** - Obtener instancia específica

### 3. Servicio de Facturación (`backend/services/billing.py`)

#### Clase BillingService:

**`generate_invoices(start_date, end_date)`**
- Obtiene consumos no facturados en el rango
- Agrupa por cliente
- Calcula costo por consumo:
  ```
  Costo = Σ (cantidad_recurso × costo_por_hora × horas_uso)
  ```
- Genera número de factura único (FAC-000001)
- Marca consumos como facturados
- Retorna facturas generadas

**`calculate_consumption_cost(consumption)`**
- Obtiene instancia del consumo
- Obtiene configuración de la instancia
- Para cada recurso en la configuración:
  - Calcula: `quantity × cost_per_hour × time_hours`
  - Suma al total
- Retorna costo total y detalle por recurso

### 4. Endpoints de API (`backend/app.py`)

#### CRUD Endpoints:

**POST `/api/crearRecurso`**
```json
{
  "id": 3,
  "name": "Disco SSD",
  "abbreviation": "SSD",
  "metric": "GB",
  "type": "Hardware",
  "value_per_hour": 0.10
}
```
Respuesta: `201 Created` con mensaje de éxito

**POST `/api/crearCategoria`**
```json
{
  "id": 2,
  "name": "Servidores de Producción",
  "description": "Servidores para aplicaciones en producción",
  "workload": "Alta",
  "configurations": []
}
```

**POST `/api/crearCliente`**
```json
{
  "nit": "12345678-9",
  "name": "Empresa XYZ",
  "username": "empresa_xyz",
  "password": "xyz123",
  "address": "Ciudad de Guatemala",
  "email": "contacto@xyz.com"
}
```
Validación automática de NIT con regex

**POST `/api/crearInstancia`**
```json
{
  "client_nit": "110339001-K",
  "id": 2,
  "configuration_id": 1,
  "name": "Servidor Producción",
  "start_date": "01/02/2025"
}
```
Extracción automática de fechas con regex

**POST `/api/cancelarInstancia`**
```json
{
  "client_nit": "110339001-K",
  "instance_id": 1,
  "end_date": "31/01/2025"
}
```
Cambia estado a "Cancelada" y establece fecha final

#### Facturación Endpoints:

**POST `/api/facturar`**
```json
{
  "start_date": "01/01/2025",
  "end_date": "31/01/2025"
}
```

Respuesta:
```json
{
  "status": "ok",
  "message": "3 facturas generadas exitosamente",
  "invoices": [
    {
      "invoice_number": "FAC-000001",
      "client_nit": "110339001-K",
      "issue_date": "31/01/2025",
      "total_amount": 156.25,
      "consumptions_count": 3,
      "details": [...]
    }
  ],
  "count": 3
}
```

**GET `/api/facturas`**
Retorna todas las facturas generadas

**GET `/api/consumosPendientes`**
Retorna consumos que NO han sido facturados

---

## 🎨 IMPLEMENTACIÓN FRONTEND

### 1. Nuevas Vistas Django (`frontend/app/views.py`)

#### `billing(request)` - Proceso de Facturación
- GET: Muestra formulario con selector de fechas
- POST: Envía rango al backend, muestra facturas generadas

#### `create_resource(request)` - Crear Recurso
- Formulario con campos: id, name, abbreviation, metric, type, value_per_hour
- POST a `/api/crearRecurso`

#### `create_category(request)` - Crear Categoría
- Formulario: id, name, description, workload
- POST a `/api/crearCategoria`

#### `create_client(request)` - Crear Cliente
- Formulario: nit, name, username, password, address, email
- Validación de NIT en frontend (pattern regex)

#### `create_instance(request)` - Crear Instancia
- Selectors dinámicos de clientes y configuraciones
- Carga datos desde `/consultar`
- POST a `/api/crearInstancia`

#### `cancel_instance_view(request)` - Cancelar Instancia
- Selector de cliente y sus instancias vigentes
- JavaScript para filtrar instancias por cliente
- POST a `/api/cancelarInstancia`

#### `view_invoices(request)` - Ver Facturas
- GET a `/api/facturas`
- Tabla con todas las facturas generadas

### 2. URLs Nuevas (`frontend/app/urls.py`)

```python
path('facturar/', views.billing, name='billing'),
path('crear/recurso/', views.create_resource, name='create_resource'),
path('crear/categoria/', views.create_category, name='create_category'),
path('crear/cliente/', views.create_client, name='create_client'),
path('crear/instancia/', views.create_instance, name='create_instance'),
path('cancelar/instancia/', views.cancel_instance_view, name='cancel_instance'),
path('facturas/', views.view_invoices, name='view_invoices'),
```

### 3. Index Actualizado (`frontend/app/templates/index.html`)

#### Nueva Sección: 💰 Facturación
- **Proceso de Facturación** → `/facturar/`
- **Consultar Facturas** → `/facturas/`

#### Nueva Sección: ➕ Creación de Nuevos Datos
- **Crear Recurso** → `/crear/recurso/`
- **Crear Categoría** → `/crear/categoria/`
- **Crear Cliente** → `/crear/cliente/`
- **Crear Instancia** → `/crear/instancia/`
- **Cancelar Instancia** → `/cancelar/instancia/`

### 4. Templates Nuevos (8 archivos)

#### `billing.html` - Selector de Fechas
- Inputs tipo `date` con conversión a dd/mm/yyyy
- JavaScript para transformar formato antes de enviar
- Información sobre el proceso de facturación

#### `billing_result.html` - Resultados
- Tabla de facturas generadas
- Monto total por factura
- Resumen de consumos facturados

#### `create_resource.html` - Formulario de Recurso
- Campos: ID, Nombre, Abreviatura, Métrica
- Selector de tipo: Hardware/Software
- Costo por hora (USD)

#### `create_category.html` - Formulario de Categoría
- Campos: ID, Nombre, Descripción
- Selector de carga: Ligera/Media/Alta/Crítica

#### `create_client.html` - Formulario de Cliente
- NIT con validación pattern
- Campos opcionales: dirección, email
- Username y password obligatorios

#### `create_instance.html` - Formulario de Instancia
- Selector de cliente (carga desde backend)
- Selector de configuración por categoría (optgroups)
- Fecha de inicio con extracción automática

#### `cancel_instance.html` - Cancelar Instancia
- Selector de cliente
- Filtrado dinámico de instancias vigentes con JavaScript
- Advertencia sobre la cancelación

#### `invoices.html` - Lista de Facturas
- Tabla responsive con todas las facturas
- Número, NIT, Fecha, Monto
- Botón para generar nuevas facturas

---

## 📂 ESTRUCTURA DE XML ACTUALIZADA

### Nodo de Facturas en `db.xml`

```xml
<database>
  <resources>...</resources>
  <categories>...</categories>
  <clients>...</clients>
  
  <consumptions>
    <consumption nit="110339001-K" instance_id="1" invoiced="true">
      <time_hours>2.5</time_hours>
      <date_time>15/01/2025 14:30</date_time>
    </consumption>
  </consumptions>
  
  <invoices>
    <invoice number="FAC-000001" nit="110339001-K">
      <issue_date>31/01/2025</issue_date>
      <total_amount>156.25</total_amount>
      <consumptions>
        <consumption_ref>0</consumption_ref>
        <consumption_ref>1</consumption_ref>
        <consumption_ref>2</consumption_ref>
      </consumptions>
    </invoice>
  </invoices>
</database>
```

---

## 🧮 EJEMPLO DE CÁLCULO DE FACTURACIÓN

### Datos de Ejemplo:

**Cliente:** ACME Corporation (NIT: 110339001-K)  
**Instancia:** "Instancia Desarrollo" (Config Básica)

**Configuración Básica incluye:**
- 2 GB Memoria RAM @ $0.75/hora = $1.50/hora
- 2 Núcleos vCPU @ $1.20/hora = $2.40/hora
- **Total por hora:** $3.90/hora

**Consumos en Enero 2025:**
1. 2.5 horas el 15/01/2025 14:30
2. 3.75 horas el 16/01/2025 09:15
3. 1.0 horas el 17/01/2025 18:00
**Total horas:** 7.25 horas

### Cálculo de Factura:

```
Consumo 1: 2.5 horas × $3.90 = $9.75
Consumo 2: 3.75 horas × $3.90 = $14.62
Consumo 3: 1.0 horas × $3.90 = $3.90
-------------------------------------------
TOTAL FACTURA: $28.27
```

**Factura Generada:**
- Número: FAC-000001
- NIT: 110339001-K
- Fecha: 31/01/2025
- Monto: $28.27

---

## 🚀 CÓMO USAR LAS NUEVAS FUNCIONALIDADES

### 1. Crear Datos Manualmente

#### Crear un Recurso:
1. Ir a `/crear/recurso/`
2. Completar formulario:
   - ID: 3
   - Nombre: Disco SSD
   - Abreviatura: SSD
   - Métrica: GB
   - Tipo: Hardware
   - Costo/hora: 0.10
3. Click en "Crear Recurso"

#### Crear una Categoría:
1. Ir a `/crear/categoria/`
2. Completar:
   - ID: 2
   - Nombre: Servidores de Producción
   - Carga: Alta
3. Click en "Crear Categoría"

#### Crear un Cliente:
1. Ir a `/crear/cliente/`
2. Completar:
   - NIT: 12345678-9 (formato validado)
   - Nombre: Empresa XYZ
   - Usuario: empresa_xyz
   - Contraseña: ****
3. Click en "Registrar Cliente"

#### Crear una Instancia:
1. Ir a `/crear/instancia/`
2. Seleccionar cliente del dropdown
3. Seleccionar configuración (agrupada por categoría)
4. Ingresar nombre: "Servidor Web"
5. Fecha de inicio: 01/02/2025
6. Click en "Crear Instancia"

### 2. Proceso de Facturación

#### Paso a Paso:
1. Ir a `/facturar/`
2. Ingresar rango de fechas:
   - Fecha inicio: 01/01/2025
   - Fecha fin: 31/01/2025
3. Click en "Generar Facturas"
4. Sistema automáticamente:
   - Busca consumos NO facturados en el rango
   - Agrupa por cliente
   - Calcula costo total por recurso
   - Genera número único de factura
   - Marca consumos como facturados
5. Muestra resultado con tabla de facturas

#### Ver Facturas Generadas:
1. Ir a `/facturas/`
2. Ver tabla con todas las facturas
3. Información: Número, NIT, Fecha, Monto

### 3. Cancelar una Instancia

1. Ir a `/cancelar/instancia/`
2. Seleccionar cliente
3. Automáticamente filtra instancias vigentes
4. Seleccionar instancia a cancelar
5. Ingresar fecha de cancelación
6. Confirmar

---

## 🔍 VALIDACIONES IMPLEMENTADAS

### Backend:
- ✅ NIT válido con regex: `^\d+-[0-9K]$`
- ✅ Extracción automática de fechas de texto
- ✅ Verificación de cliente existente antes de crear instancia
- ✅ Solo consumos NO facturados se incluyen en facturación
- ✅ Números de factura únicos secuenciales

### Frontend:
- ✅ Campos requeridos marcados con *
- ✅ Pattern validation en NIT
- ✅ Conversión de fechas (yyyy-mm-dd → dd/mm/yyyy)
- ✅ Selectores dinámicos con JavaScript
- ✅ Mensajes de error claros
- ✅ Advertencias antes de acciones destructivas

---

## 📊 ENDPOINTS COMPLETOS DISPONIBLES

### Configuración y Consumos (Semana 2):
- `POST /configuracion` - Cargar XML de configuraciones
- `POST /consumo` - Cargar XML de consumos
- `GET /consultar` - Consultar todos los datos
- `POST /inicializar` - Limpiar sistema

### CRUD Manual (Semana 3):
- `POST /api/crearRecurso` - Crear recurso individual
- `POST /api/crearCategoria` - Crear categoría
- `POST /api/crearCliente` - Registrar cliente
- `POST /api/crearInstancia` - Crear instancia
- `POST /api/cancelarInstancia` - Cancelar instancia

### Facturación (Semana 3):
- `POST /api/facturar` - Generar facturas por rango de fechas
- `GET /api/facturas` - Consultar todas las facturas
- `GET /api/consumosPendientes` - Ver consumos sin facturar

**Total:** 12 endpoints funcionales

---

## 🎨 INTERFAZ COMPLETA

### Páginas Disponibles:
1. `/` - Dashboard principal con todas las opciones
2. `/configuracion/` - Cargar XML de configuraciones
3. `/consumo/` - Cargar XML de consumos
4. `/consultar/` - Ver todos los datos del sistema
5. `/inicializar/` - Limpiar sistema
6. `/facturar/` - Proceso de facturación
7. `/facturas/` - Ver facturas generadas
8. `/crear/recurso/` - Crear recurso
9. `/crear/categoria/` - Crear categoría
10. `/crear/cliente/` - Registrar cliente
11. `/crear/instancia/` - Crear instancia
12. `/cancelar/instancia/` - Cancelar instancia
13. `/estudiante/` - Información del proyecto

**Total:** 13 páginas funcionales con Tailwind CSS

---

## ✅ CHECKLIST SEMANA 3

### Facturación:
- [x] Endpoint `/facturar` implementado
- [x] Cálculo de montos por cliente
- [x] Cálculo de montos por configuración
- [x] Cálculo de montos por recurso
- [x] Registro de facturas en XML
- [x] Números de factura únicos
- [x] Interfaz de selector de fechas
- [x] Vista de resultados de facturación

### CRUD Manual:
- [x] Crear recursos individuales
- [x] Crear categorías
- [x] Registrar clientes con validación de NIT
- [x] Crear instancias
- [x] Cancelar instancias con fecha final

### Consultas:
- [x] Consultar datos (categorías, recursos, clientes)
- [x] Ver instancias vigentes y canceladas
- [x] Consultar consumos pendientes de facturar
- [x] Ver facturas generadas

### Interfaz:
- [x] Dashboard actualizado con nuevas secciones
- [x] 8 templates nuevos con Tailwind CSS
- [x] Formularios responsivos
- [x] Validaciones en frontend
- [x] Mensajes de éxito y error

---

## 🎯 PENDIENTE PARA SEMANAS FUTURAS

### Reportes en PDF:
- [ ] Detalle de factura con desglose completo
- [ ] Gráficas de consumo
- [ ] Análisis de ventas por categoría
- [ ] Análisis de ventas por recurso

### Mejoras Potenciales:
- [ ] Autenticación de clientes
- [ ] Panel de cliente para ver sus consumos
- [ ] Notificaciones por email
- [ ] Histórico de facturación
- [ ] Estadísticas y dashboards

---

## 🚀 COMANDOS PARA INICIAR

### Con run.py (Recomendado):
```cmd
# Iniciar todo
python run.py start

# Solo backend
python run.py backend

# Solo frontend
python run.py frontend
```

### Manual:
```cmd
# Terminal 1 - Backend
cd backend
.venv\Scripts\activate
python app.py

# Terminal 2 - Frontend
cd frontend
.venv\Scripts\activate
python manage.py runserver
```

**URLs:**
- Backend: http://127.0.0.1:5001
- Frontend: http://127.0.0.1:8000

---

## 📝 NOTAS IMPORTANTES

1. **Facturación solo incluye consumos NO facturados previamente**
2. **Números de factura son únicos y secuenciales** (FAC-000001, FAC-000002, ...)
3. **Instancias canceladas ya NO pueden generar consumos facturables** después de su fecha final
4. **Todos los endpoints son compatibles con Postman** para pruebas
5. **Validación de NIT en backend y frontend** para consistencia
6. **Extracción automática de fechas** permite flexibilidad en formatos de entrada

---

**¡Semana 3 completada exitosamente!** 🎉

**Siguiente paso:** Implementar reportes en PDF y análisis de ventas
