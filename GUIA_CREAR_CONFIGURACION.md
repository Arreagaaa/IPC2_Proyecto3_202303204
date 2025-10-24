# 📋 Guía Completa: Crear Configuración

## 🎯 Objetivo
Esta guía te llevará paso a paso para crear una **configuración** dentro de una **categoría** existente, agregando múltiples recursos con sus cantidades.

---

## 📦 Prerequisitos

### 1. Tener datos de prueba
Antes de crear una configuración, necesitas:
- ✅ Al menos **1 categoría** creada
- ✅ Al menos **2 recursos** creados (ej: RAM, CPU)

---

## 🚀 Paso 1: Iniciar los Servidores

### Backend (Puerto 5001)
```cmd
cd d:\Projects\USAC\IPC2\LAB\IPC2_Proyecto3_202303204\backend
python app.py
```

**Salida esperada:**
```
 * Running on http://127.0.0.1:5001
```

### Frontend (Puerto 8000)
```cmd
cd d:\Projects\USAC\IPC2\LAB\IPC2_Proyecto3_202303204\frontend
python manage.py runserver
```

**Salida esperada:**
```
Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 Paso 2: Acceder al Dashboard

1. Abre tu navegador
2. Ve a: **http://localhost:8000**
3. Verás el dashboard con estadísticas y opciones

---

## ➕ Paso 3: Crear Datos de Prueba (si no los tienes)

### 3.1 Crear Recursos

**Recurso 1: RAM**
1. Clic en **"Crear Recurso"** (card verde en columna CRUD)
2. Llenar formulario:
   - **ID:** `1`
   - **Nombre:** `RAM`
   - **Métrica:** `GiB`
   - **Costo por hora:** `0.05`
3. Clic en **"Crear Recurso"**
4. ✅ Mensaje: "Recurso creado exitosamente"

**Recurso 2: CPU**
1. Clic en **"Crear Recurso"**
2. Llenar formulario:
   - **ID:** `2`
   - **Nombre:** `CPU`
   - **Métrica:** `Núcleos`
   - **Costo por hora:** `0.10`
3. Clic en **"Crear Recurso"**
4. ✅ Mensaje: "Recurso creado exitosamente"

**Recurso 3: Almacenamiento (opcional)**
1. Clic en **"Crear Recurso"**
2. Llenar formulario:
   - **ID:** `3`
   - **Nombre:** `Almacenamiento SSD`
   - **Métrica:** `GB`
   - **Costo por hora:** `0.02`
3. Clic en **"Crear Recurso"**

### 3.2 Crear Categoría

**Categoría: Computing**
1. Clic en **"Crear Categoría"** (card verde en CRUD)
2. Llenar formulario:
   - **ID:** `1`
   - **Nombre:** `Computing`
   - **Descripción:** `Servicios de cómputo en la nube`
3. Clic en **"Crear Categoría"**
4. ✅ Mensaje: "Categoría creada exitosamente"

---

## 🎨 Paso 4: Crear Configuración (NUEVA FUNCIONALIDAD)

### 4.1 Acceder al Formulario
1. Desde el dashboard, busca la sección **"Crear Nuevos Datos"** (columna 3)
2. Localiza el card **"Crear Configuración"** (entre "Crear Categoría" y "Crear Cliente")
3. Clic en **"Crear Configuración"**

### 4.2 Llenar Información Básica

**Sección: Información Básica**

1. **Categoría:** 
   - Seleccionar del dropdown: `Computing`
   
2. **ID de Configuración:**
   - Ingresar: `1`
   
3. **Nombre de Configuración:**
   - Ingresar: `Dev Basic`
   
4. **Descripción:**
   - Ingresar: `Configuración básica para desarrollo con recursos moderados`

### 4.3 Agregar Recursos

**Primera fila de recurso (ya está visible):**

1. **Recurso:** Seleccionar del dropdown: `RAM (GiB)`
2. **Cantidad:** Ingresar: `4`

**Agregar segundo recurso:**

3. Clic en el botón azul **"Agregar Recurso"**
4. En la nueva fila:
   - **Recurso:** Seleccionar: `CPU (Núcleos)`
   - **Cantidad:** Ingresar: `2`

**Agregar tercer recurso (opcional):**

5. Clic en **"Agregar Recurso"**
6. En la nueva fila:
   - **Recurso:** Seleccionar: `Almacenamiento SSD (GB)`
   - **Cantidad:** Ingresar: `50`

### 4.4 Enviar Formulario

1. Revisar todos los datos ingresados
2. Clic en el botón verde **"Crear Configuración"**
3. ✅ Verás página de éxito con mensaje: **"Configuración creada exitosamente"**

---

## 🔍 Paso 5: Verificar la Configuración Creada

### 5.1 Verificar en Consulta

1. Volver al dashboard (botón "Volver al inicio")
2. Clic en **"Consultar Datos"** (card azul en columna 1)
3. Buscar en la sección **"Categorías"**
4. Expandir categoría `Computing`
5. Deberías ver:
   ```
   Configuraciones:
   - Dev Basic
     - RAM: 4 GiB
     - CPU: 2 Núcleos
     - Almacenamiento SSD: 50 GB
   ```

### 5.2 Verificar en XML

1. Abrir el archivo: `backend/instance/data/db.xml`
2. Buscar la categoría con ID `1`
3. Verificar estructura:

```xml
<category id="1">
  <name>Computing</name>
  <description>Servicios de cómputo en la nube</description>
  <configurations>
    <configuration id="1">
      <name>Dev Basic</name>
      <description>Configuración básica para desarrollo con recursos moderados</description>
      <resources>
        <resource id="1">4</resource>
        <resource id="2">2</resource>
        <resource id="3">50</resource>
      </resources>
    </configuration>
  </configurations>
</category>
```

---

## 📊 Paso 6: Crear Más Configuraciones (Práctica)

### Configuración 2: Production Standard

1. Clic en **"Crear Configuración"**
2. Datos:
   - **Categoría:** `Computing`
   - **ID:** `2`
   - **Nombre:** `Production Standard`
   - **Descripción:** `Configuración para producción con alta disponibilidad`
   - **Recursos:**
     - RAM: `16` GiB
     - CPU: `8` Núcleos
     - Almacenamiento SSD: `200` GB
3. Crear

### Configuración 3: Micro Instance

1. Clic en **"Crear Configuración"**
2. Datos:
   - **Categoría:** `Computing`
   - **ID:** `3`
   - **Nombre:** `Micro Instance`
   - **Descripción:** `Configuración mínima para pruebas`
   - **Recursos:**
     - RAM: `1` GiB
     - CPU: `1` Núcleo
     - Almacenamiento SSD: `10` GB
3. Crear

---

## 🎯 Paso 7: Usar las Configuraciones

Una vez creadas las configuraciones, los **clientes** podrán:

1. **Crear instancias** basadas en estas configuraciones
2. La instancia heredará todos los recursos de la configuración
3. El sistema calculará el costo: `(cantidad × costo_por_hora) × horas_uso`

**Ejemplo de cálculo para "Dev Basic" por 24 horas:**
```
RAM:   4 GiB  × $0.05/hora × 24h = $4.80
CPU:   2 Cores × $0.10/hora × 24h = $4.80
SSD:   50 GB  × $0.02/hora × 24h = $24.00
                            TOTAL = $33.60
```

---

## ⚠️ Manejo de Errores

### Error: "La categoría no existe"
- **Causa:** ID de categoría inválido
- **Solución:** Verificar que la categoría exista en "Consultar Datos"

### Error: "Ya existe una configuración con ese ID en esta categoría"
- **Causa:** ID duplicado dentro de la misma categoría
- **Solución:** Usar un ID diferente

### Error: "El recurso con ID X no existe"
- **Causa:** Recurso seleccionado no existe en el sistema
- **Solución:** Crear el recurso primero o seleccionar uno existente

### Error: "Debe haber al menos un recurso en la configuración"
- **Causa:** Intentaste eliminar la única fila de recurso
- **Solución:** Mantén al menos un recurso en la configuración

---

## 🧪 Casos de Prueba Recomendados

### ✅ Caso 1: Configuración Simple
- 1 categoría
- 1 configuración
- 2 recursos
- **Resultado esperado:** Creación exitosa

### ✅ Caso 2: Configuración Compleja
- 1 categoría
- 1 configuración
- 5+ recursos
- **Resultado esperado:** Creación exitosa con todos los recursos

### ✅ Caso 3: Múltiples Configuraciones
- 1 categoría
- 3 configuraciones diferentes
- **Resultado esperado:** Todas creadas sin conflictos

### ❌ Caso 4: ID Duplicado
- Crear configuración con ID `1`
- Intentar crear otra con ID `1` en la misma categoría
- **Resultado esperado:** Error de duplicado

### ❌ Caso 5: Categoría Inexistente
- Intentar crear configuración con category_id `999`
- **Resultado esperado:** Error "Categoría no existe"

---

## 🔧 Comandos de Diagnóstico

### Ver logs del backend
```cmd
cd backend
python app.py
# Observar consola para requests POST /api/crearConfiguracion
```

### Ver logs del frontend
```cmd
cd frontend
python manage.py runserver
# Observar consola para requests GET/POST /crear/configuracion/
```

### Verificar XML manualmente
```cmd
type backend\instance\data\db.xml
```

---

## 📁 Archivos Involucrados

```
backend/
├── app.py                    # Endpoint /api/crearConfiguracion (líneas ~220-300)
├── models/
│   └── storage.py           # Método add_configuration_to_category()
└── instance/
    └── data/
        └── db.xml           # Almacenamiento de datos

frontend/
├── app/
│   ├── views.py             # Vista create_configuration()
│   ├── urls.py              # Ruta 'crear/configuracion/'
│   └── templates/
│       ├── index.html       # Link "Crear Configuración"
│       ├── create_configuration.html  # Formulario
│       └── result.html      # Página de éxito
```

---

## 🎓 Conceptos Clave

### ¿Qué es una Configuración?
Una **plantilla de recursos** que agrupa varios recursos con cantidades específicas. Los clientes crean **instancias** basadas en estas configuraciones.

### Jerarquía de Datos
```
Recurso (RAM, CPU, SSD)
    ↓
Categoría (Computing, Storage)
    ↓
Configuración (Dev Basic, Production)
    ↓
Instancia (Creada por cliente)
    ↓
Factura (Costo calculado)
```

---

## ✨ Características del Formulario

- ✅ **Formulario dinámico**: Agrega/elimina recursos sin límite
- ✅ **Validación frontend**: Campos requeridos, cantidades positivas
- ✅ **Validación backend**: Categoría y recursos existen
- ✅ **Dark theme**: Diseño consistente con el resto del sistema
- ✅ **Responsive**: Funciona en móvil, tablet y desktop
- ✅ **Prevención de errores**: No permite eliminar el último recurso
- ✅ **Feedback claro**: Mensajes de error/éxito descriptivos

---

## 🎉 ¡Listo!

Ahora puedes crear configuraciones completas para tu sistema de facturación cloud. Las configuraciones permitirán a los clientes crear instancias de forma rápida y estandarizada.

**Próximos pasos sugeridos:**
1. Crear más recursos variados (Network, Database, etc.)
2. Crear más categorías (Storage, Networking, etc.)
3. Crear múltiples configuraciones por categoría
4. Probar creación de instancias basadas en estas configuraciones
5. Generar facturas para ver el cálculo de costos

---

**Fecha:** 23 de Octubre de 2025  
**Proyecto:** IPC2 Proyecto 3 - Sistema de Facturación Cloud  
**Estudiante:** 202303204
