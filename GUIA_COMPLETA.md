# 📘 GUÍA DE USO - Sistema de Facturación Cloud
## Tecnologías Chapinas S.A.

**Estudiante:** 202303204  
**Proyecto:** IPC2 Proyecto 3

---

## 🚀 INICIO RÁPIDO

### **Paso 1: Iniciar Servidores**

```bash
# Terminal 1 - Backend (Flask)
cd backend
python app.py
# ✓ Servidor corriendo en http://localhost:5001

# Terminal 2 - Frontend (Django)  
cd frontend
python manage.py runserver
# ✓ Servidor corriendo en http://localhost:8000
```

---

## 📝 FLUJO COMPLETO CON DATOS REALES

### **PASO 1: Cargar Configuración Inicial**

**¿Qué hace?** Carga recursos, categorías, configuraciones, clientes e instancias.

**Acción:**
1. Ir a: `http://localhost:8000/configuracion/`
2. Seleccionar archivo: `backend/instance/data/example_config.xml`
3. Click en "Cargar XML"

**Archivo XML usado:**
```xml
<?xml version="1.0"?>
<archivoConfiguraciones>
  <listaRecursos>
    <recurso id="1">
      <nombre>Memoria RAM</nombre>
      <abreviatura>GiB</abreviatura>
      <metrica>GiB</metrica>
      <tipo>Hardware</tipo>
      <valorXhora>0.75</valorXhora>
    </recurso>
    <recurso id="2">
      <nombre>Núcleos</nombre>
      <abreviatura>cores</abreviatura>
      <metrica>unidades</metrica>
      <tipo>Hardware</tipo>
      <valorXhora>1.2</valorXhora>
    </recurso>
  </listaRecursos>
  
  <listaCategorias>
    <categoria id="10">
      <nombre>VM Desarrollo</nombre>
      <descripcion>Para pruebas y desarrollo</descripcion>
      <cargaTrabajo>Desarrollo</cargaTrabajo>
      <listaConfiguraciones>
        <configuracion id="100">
          <nombre>Dev Basic</nombre>
          <descripcion>Configuración básica</descripcion>
          <recursosConfiguracion>
            <recurso id="1">4</recurso>  <!-- 4 GiB RAM -->
            <recurso id="2">2</recurso>  <!-- 2 cores -->
          </recursosConfiguracion>
        </configuracion>
      </listaConfiguraciones>
    </categoria>
  </listaCategorias>
  
  <listaClientes>
    <cliente nit="110339001-K">
      <nombre>ACME</nombre>
      <usuario>acme_user</usuario>
      <clave>pass</clave>
      <direccion>Ciudad</direccion>
      <correoElectronico>acme@example.com</correoElectronico>
      <listaInstancias>
        <instancia id="500">
          <idConfiguracion>100</idConfiguracion>
          <nombre>acme-dev-1</nombre>
          <fechaInicio>01/01/2025</fechaInicio>
          <estado>Vigente</estado>
        </instancia>
      </listaInstancias>
    </cliente>
    
    <cliente nit="85125-K">
      <nombre>JAKES Inc.</nombre>
      <usuario>jakes_user</usuario>
      <clave>pass123</clave>
      <direccion>Guatemala City</direccion>
      <correoElectronico>contact@jakes.com</correoElectronico>
      <listaInstancias>
        <instancia id="555">
          <idConfiguracion>100</idConfiguracion>
          <nombre>jakes-prod-1</nombre>
          <fechaInicio>01/01/2025</fechaInicio>
          <estado>Vigente</estado>
        </instancia>
      </listaInstancias>
    </cliente>
  </listaClientes>
</archivoConfiguraciones>
```

**Resultado esperado:**
```
✓ 2 recursos creados
✓ 1 categoría creada  
✓ 1 configuración creada
✓ 2 clientes creados
✓ 2 instancias creadas
```

**¿Qué se guardó en db.xml?**
- **2 Recursos:** RAM ($0.75/hora) y Núcleos ($1.20/hora)
- **1 Categoría:** VM Desarrollo con 1 configuración (Dev Basic: 4 GiB + 2 cores)
- **2 Clientes:**
  - ACME (110339001-K) con instancia 500 (acme-dev-1)
  - JAKES Inc. (85125-K) con instancia 555 (jakes-prod-1)

---

### **PASO 2: Cargar Consumos**

**¿Qué hace?** Registra el tiempo de uso de cada instancia.

**Acción:**
1. Ir a: `http://localhost:8000/consumo/`
2. Seleccionar archivo: `backend/instance/data/example_consumos.xml`
3. Click en "Cargar XML"

**Archivo XML usado:**
```xml
<?xml version="1.0"?>
<listadoConsumos>
    <!-- ACME: 2 consumos -->
    <consumo nitCliente="110339001-K" idInstancia="500">
        <tiempo>2.5</tiempo>
        <fechaHora>Guatemala, 15/01/2025 14:30</fechaHora>
    </consumo>
    <consumo nitCliente="110339001-K" idInstancia="500">
        <tiempo>3.75</tiempo>
        <fechaHora>en la ciudad de Guatemala, 16/01/2025 09:15 se registra el consumo</fechaHora>
    </consumo>
    
    <!-- JAKES Inc.: 3 consumos -->
    <consumo nitCliente="85125-K" idInstancia="555">
        <tiempo>4.0</tiempo>
        <fechaHora>10/01/2025 10:00</fechaHora>
    </consumo>
    <consumo nitCliente="85125-K" idInstancia="555">
        <tiempo>6.5</tiempo>
        <fechaHora>Guatemala, 11/01/2025 14:30</fechaHora>
    </consumo>
    <consumo nitCliente="85125-K" idInstancia="555">
        <tiempo>2.25</tiempo>
        <fechaHora>12/01/2025 09:00</fechaHora>
    </consumo>
</listadoConsumos>
```

**Resultado esperado:**
```
✓ 5 consumos registrados
```

**¿Qué se guardó?**
- ACME (110339001-K):
  - Instancia 500: 2.5 horas + 3.75 horas = 6.25 horas total
- JAKES Inc. (85125-K):
  - Instancia 555: 4.0 + 6.5 + 2.25 = 12.75 horas total

---

### **PASO 3: Verificar Dashboard**

**Acción:**
1. Ir a: `http://localhost:8000/`

**Deberías ver:**
```
┌─────────────┬──────────┬────────────┬───────────┐
│  Recursos   │ Clientes │ Instancias │ Facturas  │
│      2      │    2     │     2      │     0     │
└─────────────┴──────────┴────────────┴───────────┘
```

---

### **PASO 4: Consultar Consumos Pendientes**

**Acción:**
1. Ir a: `http://localhost:8000/consumos-pendientes/`

**Deberías ver tabla con 5 consumos:**
```
NIT Cliente     | ID Instancia | Horas | Fecha/Hora       | Estado
----------------+--------------+-------+------------------+-----------
110339001-K     | 500          | 2.5   | 15/01/2025 14:30 | Pendiente
110339001-K     | 500          | 3.75  | 16/01/2025 09:15 | Pendiente
85125-K         | 555          | 4.0   | 10/01/2025 10:00 | Pendiente
85125-K         | 555          | 6.5   | 11/01/2025 14:30 | Pendiente
85125-K         | 555          | 2.25  | 12/01/2025 09:00 | Pendiente
```

---

### **PASO 5: Generar Facturas**

**¿Qué hace?** Crea facturas por cliente calculando el costo de cada consumo.

**Acción:**
1. Ir a: `http://localhost:8000/facturar/`
2. Llenar formulario:
   - **Fecha Inicio:** 01/01/2025
   - **Fecha Fin:** 31/01/2025
3. Click "Generar Facturas"

**Cálculos realizados:**

**Cliente ACME (110339001-K):**
```
Instancia 500 usa configuración 100 (Dev Basic):
- 4 GiB RAM × $0.75/hora
- 2 cores × $1.20/hora

Consumo 1: 2.5 horas
- RAM:   4 × $0.75 × 2.5 = $7.50
- Cores: 2 × $1.20 × 2.5 = $6.00
- Subtotal: $13.50

Consumo 2: 3.75 horas
- RAM:   4 × $0.75 × 3.75 = $11.25
- Cores: 2 × $1.20 × 3.75 = $9.00
- Subtotal: $20.25

TOTAL ACME: $13.50 + $20.25 = $33.75
```

**Cliente JAKES Inc. (85125-K):**
```
Instancia 555 usa configuración 100 (Dev Basic):
- 4 GiB RAM × $0.75/hora
- 2 cores × $1.20/hora

Consumo 1: 4.0 horas
- RAM:   4 × $0.75 × 4.0 = $12.00
- Cores: 2 × $1.20 × 4.0 = $9.60
- Subtotal: $21.60

Consumo 2: 6.5 horas
- RAM:   4 × $0.75 × 6.5 = $19.50
- Cores: 2 × $1.20 × 6.5 = $15.60
- Subtotal: $35.10

Consumo 3: 2.25 horas
- RAM:   4 × $0.75 × 2.25 = $6.75
- Cores: 2 × $1.20 × 2.25 = $5.40
- Subtotal: $12.15

TOTAL JAKES: $21.60 + $35.10 + $12.15 = $68.85
```

**Resultado esperado:**
```
Facturas Generadas
------------------
FAC-000001 | NIT: 110339001-K | Fecha: 31/01/2025 | Monto: $33.75
FAC-000002 | NIT: 85125-K     | Fecha: 31/01/2025 | Monto: $68.85
```

---

### **PASO 6: Ver Facturas Generadas**

**Acción:**
1. Ir a: `http://localhost:8000/facturas/`

**Deberías ver:**
```
Total de facturas: 2

Número          | NIT Cliente  | Fecha Emisión | Monto Total
----------------+--------------+---------------+-------------
FAC-000001      | 110339001-K  | 31/01/2025    | $33.75
FAC-000002      | 85125-K      | 31/01/2025    | $68.85
```

---

### **PASO 7: Verificar Consumos Pendientes (de nuevo)**

**Acción:**
1. Ir a: `http://localhost:8000/consumos-pendientes/`

**Deberías ver:**
```
✓ ¡Éxito!
No hay consumos pendientes. Todos los consumos han sido facturados.
```

---

## 📊 CONSULTAR DATOS DEL SISTEMA

**Acción:**
1. Ir a: `http://localhost:8000/consultar/`

**Verás 6 tarjetas de estadísticas:**
```
Recursos: 2 | Categorías: 1 | Configuraciones: 1
Clientes: 2 | Instancias: 2 | Consumos: 5
```

**Tablas mostradas:**

**1. Recursos:**
```
ID | Nombre      | Abrev. | Métrica  | Tipo     | Valor/Hora
---+-------------+--------+----------+----------+-----------
1  | Memoria RAM | GiB    | GiB      | Hardware | $0.75
2  | Núcleos     | cores  | unidades | Hardware | $1.2
```

**2. Categorías y Configuraciones:**
```
VM Desarrollo (ID: 10)
Para pruebas y desarrollo
Carga de trabajo: Desarrollo

  ▸ Dev Basic (ID: 100)
    Configuración básica
    Recursos: Recurso 1: 4 | Recurso 2: 2
```

**3. Clientes e Instancias:**
```
ACME (NIT: 110339001-K)
Usuario: acme_user | Email: acme@example.com
Ciudad

  ▸ acme-dev-1 (ID: 500)
    Configuración ID: 100
    Inicio: 01/01/2025
    Estado: Vigente

JAKES Inc. (NIT: 85125-K)
Usuario: jakes_user | Email: contact@jakes.com
Guatemala City

  ▸ jakes-prod-1 (ID: 555)
    Configuración ID: 100
    Inicio: 01/01/2025
    Estado: Vigente
```

---

## ➕ CREAR NUEVOS DATOS MANUALMENTE

### **Crear Nuevo Recurso**

**Ruta:** `http://localhost:8000/crear/recurso/`

**Ejemplo:**
```
ID: 3
Nombre: Disco SSD
Abreviatura: SSD
Métrica: GB
Tipo: Hardware
Valor por Hora: 0.05
```

### **Crear Nueva Categoría**

**Ruta:** `http://localhost:8000/crear/categoria/`

**Ejemplo:**
```
ID: 20
Nombre: VM Producción
Descripción: Para aplicaciones en producción
Carga de Trabajo: Production
```

### **Crear Nuevo Cliente**

**Ruta:** `http://localhost:8000/crear/cliente/`

**Ejemplo:**
```
NIT: 999888-7
Nombre: TechCorp S.A.
Usuario: techcorp_admin
Clave: secure123
Dirección: Zona 10, Guatemala
Email: admin@techcorp.com
```

### **Crear Nueva Instancia**

**Ruta:** `http://localhost:8000/crear/instancia/`

**Ejemplo:**
```
ID: 600
NIT Cliente: 999888-7
ID Configuración: 100
Nombre: techcorp-web-1
Fecha Creación: 23/10/2025
```

### **Cancelar Instancia**

**Ruta:** `http://localhost:8000/cancelar/instancia/`

**Ejemplo:**
```
ID Instancia: 600
Fecha Cancelación: 30/10/2025
```

**Efecto:** La instancia cambia a estado "Cancelada" y no acepta más consumos.

---

## 🔄 REINICIAR SISTEMA

**¿Cuándo usar?** Para empezar de cero con datos limpios.

**Acción:**
1. Ir a: `http://localhost:8000/inicializar/`
2. Click "Confirmar Inicialización"

**Resultado:**
```
✓ Sistema inicializado correctamente
Todos los datos han sido eliminados
```

---

## ✅ CHECKLIST DE FUNCIONALIDADES

- ✅ Cargar XML de configuración (recursos, categorías, clientes, instancias)
- ✅ Cargar XML de consumos
- ✅ Generar facturas por rango de fechas
- ✅ Cálculo correcto: `quantity × cost_per_hour × time_hours`
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Consultar todos los datos del sistema
- ✅ Crear recursos, categorías, clientes, instancias manualmente
- ✅ Cancelar instancias
- ✅ Ver facturas generadas
- ✅ Ver consumos pendientes
- ✅ Inicializar sistema (borrar todo)

---

## 🎨 DISEÑO DEL SISTEMA

### **Colores Semánticos:**
- 🔵 **Azul:** Acciones normales (consultar, ver, navegar)
- 🟢 **Verde:** Crear/agregar datos nuevos
- 🟡 **Amarillo:** Advertencias (consumos pendientes)
- 🔴 **Rojo:** Acciones destructivas (cancelar, eliminar)

### **Tema Dark:**
- Fondo: `bg-slate-900`
- Tarjetas: `bg-slate-800`
- Bordes: `border-slate-700`
- 100% iconos SVG (sin emojis)

---

## 📁 ARCHIVOS IMPORTANTES

```
backend/
├── app.py                  (12 endpoints REST API)
├── models/
│   ├── storage.py         (XMLStorage - Leer/escribir db.xml)
│   ├── parser.py          (Parse XML de entrada)
│   └── domain.py          (Clases de datos)
├── services/
│   └── billing.py         (Lógica de facturación)
└── instance/data/
    ├── db.xml             (Base de datos XML persistente)
    ├── example_config.xml (Ejemplo de configuración)
    └── example_consumos.xml (Ejemplo de consumos)

frontend/
├── app/
│   ├── views.py           (13 vistas Django)
│   ├── urls.py            (Rutas)
│   └── templates/         (15 archivos HTML)
└── core/
    └── settings.py        (Configuración Django)
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

**Problema:** Dashboard muestra `--` en lugar de números
- **Solución:** Asegúrate de cargar primero el XML de configuración

**Problema:** Factura sale en $0.00
- **Solución:** Verifica que el cliente y la instancia existan en db.xml

**Problema:** 404 en `/cancelar-instancia/`
- **Solución:** La URL correcta es `/cancelar/instancia/` (con `/`)

**Problema:** Consumos no aparecen en "Pendientes"
- **Solución:** Ya fueron facturados. Verifica en `/facturas/`

---

**¡Sistema completo y listo para usar! 🎉**

Proyecto: IPC2 Proyecto 3 - Tecnologías Chapinas S.A.  
Estudiante: 202303204
