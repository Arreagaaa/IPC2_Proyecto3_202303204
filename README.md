# IPC2 Proyecto 3 - Sistema de Facturación de Infraestructura en la Nube

**Carnet:** 202303204  
**Curso:** Introducción a la Programación y Computación 2  
**Universidad de San Carlos de Guatemala**

## Descripción del Proyecto

Sistema de facturación para Tecnologías Chapinas S.A. que permite gestionar servicios de infraestructura en la nube, incluyendo recursos, categorías, configuraciones, clientes, instancias y consumos.

## Arquitectura del Sistema

El proyecto implementa una arquitectura de microservicios con dos componentes principales:

- **Programa 1 (Frontend):** Aplicación web Django para interfaz de usuario
- **Servicio 2 (Backend):** API REST Flask para procesamiento y almacenamiento de datos

## Tecnologías Utilizadas

- **Backend:** Flask 2.2.5, Python 3.x
- **Frontend:** Django 4.2.10, Tailwind CSS (CDN)
- **Base de Datos:** XML Persistente
- **Comunicación:** REST API (HTTP/JSON)

## Estructura del Proyecto

```
IPC2_Proyecto3_202303204/
├── backend/
│   ├── app.py                      # Aplicación Flask principal
│   ├── requirements.txt            # Dependencias del backend
│   ├── models/
│   │   ├── domain.py              # Modelos de dominio
│   │   ├── parser.py              # Parseo de XML
│   │   ├── storage.py             # Almacenamiento XML
│   │   └── validators.py          # Validaciones (NIT, fechas)
│   └── instance/
│       └── data/
│           ├── db.xml             # Base de datos XML
│           ├── example_config.xml # XML de ejemplo (configuración)
│           └── example_consumos.xml # XML de ejemplo (consumos)
├── frontend/
│   ├── manage.py                   # Django management
│   ├── requirements.txt            # Dependencias del frontend
│   ├── app/
│   │   ├── views.py               # Vistas Django
│   │   ├── urls.py                # URLs de la aplicación
│   │   └── templates/             # Plantillas HTML
│   └── core/
│       ├── settings.py            # Configuración Django
│       └── urls.py                # URLs principales
└── test_backend_complete.py       # Script de pruebas

```

## Endpoints del Backend

### POST /configuracion
Recibe XML con recursos, categorías, configuraciones, clientes e instancias.

**Request:** XML con estructura de configuración  
**Response:** JSON con conteo de elementos creados

### POST /consumo
Recibe XML con consumos de recursos (NIT, instancia, tiempo, fecha/hora).

**Request:** XML con listado de consumos  
**Response:** JSON con número de consumos procesados

### GET /consultar
Obtiene todos los datos almacenados en el sistema.

**Response:** JSON con recursos, categorías, clientes, consumos y resumen

### POST /inicializar
Limpia todos los datos del sistema.

**Response:** JSON confirmando inicialización

## Instalación y Configuración

### 1. Configurar Backend

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar Frontend

```cmd
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución del Sistema

### Iniciar Backend (Terminal 1)

```cmd
cd backend
.venv\Scripts\activate
python app.py
```

El backend se ejecutará en: http://127.0.0.1:5001

### Iniciar Frontend (Terminal 2)

```cmd
cd frontend
.venv\Scripts\activate
python manage.py runserver
```

El frontend se ejecutará en: http://127.0.0.1:8000

## Uso del Sistema

### Interfaz Web

1. **Página Principal:** http://127.0.0.1:8000/
   - Tarjetas de navegación para todas las funcionalidades

2. **Enviar Mensaje de Configuración:** http://127.0.0.1:8000/configuracion/
   - Cargar XML con recursos, categorías, clientes e instancias
   - Ejemplo: `backend/instance/data/example_config.xml`

3. **Enviar Mensaje de Consumo:** http://127.0.0.1:8000/consumo/
   - Cargar XML con registro de consumos
   - Ejemplo: `backend/instance/data/example_consumos.xml`

4. **Consultar Datos:** http://127.0.0.1:8000/consultar/
   - Visualizar todos los datos del sistema
   - Muestra recursos, categorías, clientes, instancias y consumos

5. **Inicializar Sistema:** http://127.0.0.1:8000/inicializar/
   - Eliminar todos los datos (requiere confirmación)

6. **Información del Estudiante:** http://127.0.0.1:8000/estudiante/
   - Ver información del proyecto y documentación

## Pruebas del Sistema

### Usando el Script de Pruebas

```cmd
# Asegurarse de que el backend esté corriendo
python test_backend_complete.py
```

El script ejecuta:
1. Inicialización del sistema
2. Carga de configuraciones
3. Carga de consumos
4. Consulta de datos

### Pruebas Manuales

Ver archivo `PRUEBAS_SEMANA2.md` para pruebas detalladas con curl y navegador.

## Validaciones Implementadas

### Validación de NIT
- Formato: `números-dígito` (ej: 110339001-K, 34300-4)
- Dígito verificador: 0-9 o K

### Extracción de Fechas
- Formato: `dd/mm/yyyy` o `dd/mm/yyyy hh:mm`
- Extrae la primera fecha válida encontrada en cualquier texto
- Ejemplos válidos:
  - "01/01/2025"
  - "Guatemala, 15/03/2024"
  - "en la ciudad de Guatemala, 16/01/2025 09:15 se registra"

## Formato de Archivos XML

### XML de Configuración
Estructura:
- `<listaRecursos>` - Recursos disponibles (Hardware/Software)
- `<listaCategorias>` - Categorías con configuraciones
- `<listaClientes>` - Clientes con instancias

### XML de Consumos
Estructura:
- `<listadoConsumos>` - Consumos con NIT, instancia, tiempo y fecha/hora

Ver archivos de ejemplo en `backend/instance/data/`

## Notas Importantes

1. **Orden de inicio:** Siempre iniciar backend antes que frontend
2. **Persistencia:** Datos almacenados en `backend/instance/data/db.xml`
3. **CORS:** Habilitado para comunicación frontend-backend
4. **Código:** Variables y funciones en inglés, UI y comentarios en español
5. **Sin emojis:** Proyecto libre de emojis

## Solución de Problemas

### Backend no responde
- Verificar que el backend esté corriendo en puerto 5001
- Revisar logs en la terminal del backend

### Error al cargar XML
- Verificar formato del XML
- Asegurar que NITs sean válidos
- Confirmar que fechas tengan formato correcto

### Error de conexión en frontend
- Verificar que backend esté corriendo
- Revisar URL del backend en `frontend/app/views.py`

## Autor

Estudiante USAC - Carnet 202303204  
Proyecto IPC2 - 2024