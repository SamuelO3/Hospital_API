# Hospital_API
API de sistema hospitalario

## **1. Información General**
- **Nombre del Proyecto**: Sistema Hospitalario
- **Versión del Sistema**: 1.1.0
- **Fecha de Creación**: 08/2025
- **Autor(es)**: Emanuel Medina Arboleda, Samuel Ortiz Bermudez, Julián Garcia Guevara
- **Propósito**: Proporcionar información técnica detallada sobre la instalación, configuración, funcionamiento y mantenimiento de la API REST desarrollada en FastAPI para la gestión hospitalaria.

---

## **2. Introducción**
### **2.1 Descripción del Sistema**
El sistema es una API RESTful desarrollada en FastAPI que permite la gestión de información hospitalaria. Maneja recursos como:
- Pacientes
- Médicos
- Enfermeras
- Citas médicas
- Facturas
- Registros de diagnósticos
Su propósito es centralizar y simplificar las operaciones del hospital, facilitando el acceso y administración de datos médicos.

### **2.2 Alcance**
El manual cubre:
- Instalación y configuración del sistema.
- Requisitos de hardware y software.
- Arquitectura y componentes principales.
- Operación del sistema y flujos de trabajo.
 
---

## **3. Requisitos del Sistema**
### **3.1 Requisitos de Hardware**
- Procesador: 2 núcleos mínimos.
- Memoria RAM: 2 GB mínimo.
- Espacio en Disco: 200 MB.
- Otros: Conexión a internet para instalar dependencias.

### **3.2 Requisitos de Software**
- Sistema Operativo: Windows, Linux o macOS.
- Lenguaje: Python 3.9 o superior.
- Frameworks: FastAPI, Uvicorn.
- Librerías: Pydantic, Typing.
- Otros: Git (opcional).

---

## **4. Instalación**
### **4.1 Descarga de Archivos**
git clone <URL_DEL_REPOSITORIO>

### **4.2 Instalación Paso a Paso**
1. Instalar dependencias: pip install -r requirements.txt
2. Ejecutar servidor: uvicorn main:app --reload

### **4.3 Configuración Inicial**
- El sistema no requiere configuración adicional de base de datos.
- Acceder a la documentación interactiva en:
  http://127.0.0.1:8000/docs (Swagger UI).
  http://127.0.0.1:8000/redoc (Redoc).

---

## **5. Arquitectura del Sistema**
### **5.1 Diagrama de Arquitectura**
 main.py ───► routers/
                ├── pacienteRouter.py
                ├── medicoRouter.py
                ├── enfermeraRouter.py
                ├── citaRouter.py
                ├── facturaRouter.py
                └── registroDiagnosticoRouter.py
           └── models/
                └── models.py
                

### **5.2 Componentes Principales**
- **main.py**: Punto de entrada de la aplicación.
- **routers/**: Contiene los endpoints organizados por entidad.
- **models/**: Define los modelos de datos (usando Pydantic).

---

## **6. Operación del Sistema**
### **6.1 Descripción General**
El sistema funciona como un servidor REST que permite realizar operaciones CRUD sobre entidades hospitalarias. Cada recurso tiene sus rutas específicas bajo el esquema:
-  /pacientes/ → Gestión de pacientes.
-  /medicos/ → Gestión de médicos.
-  /enfermeras/ → Gestión de enfermeras.
-  /citas/ → Gestión de citas.
-  /facturas/ → Gestión de facturas.
-  /diagnosticos/ → Registro de diagnósticos.

### **6.2 Flujos de Trabajo Principales**
1. **Gestión de Pacientes/Medicos/Enfermeras**:
-  Crear un paciente/medicos/enfermeras → POST (/patient),(/medicos) o (/enfermeras)
-  Consultar pacientes → GET (/patient),(/medicos) o (/enfermeras)
-  Editar paciente → PUT (/patient/{patient_id}),(/medicos/{id}) o (/enfermeras/{id})
-  Eliminar paciente → DELETE (/patient/{patient_id}),(/medicos/{id}) o (/enfermeras/{id})
  
2. **Gestión de Citas Médicas**:
-  Registrar cita → POST /citas/
-  Consultar citas → GET /citas/
-  Actualizar cita → PUT /citas/{id}
-  Cancelar cita → DELETE /citas/{id}

4. **Generación de Diagnosticos**:
-  Crear Diagnostico → POST /diagnostico/
-  Consultar diagnosticos → GET /diagnostico/
-  Consultar diagnosticos por tipo de diagnostico → GET /diagnostico/tipo
-  Consultar diagnostico por id → GET /diagnostico/{diagnostico_id}
-  Actualizar diagnostico → PUT /diagnostico/{diagnostico_id}
-  Eliminar diagnostico → DELETE /diagnostico/{diagnostico_id}

5. **Generación de Facturas**:
-  Crear factura → POST /Factura/
-  Consultar facturas → GET /Factura/
-  Consultar facturas por paciente → GET /Factura/patient
-  Actualizar facturas → PUT /Factura/{factura_id}
-  Eliminar facturas → DELETE /Factura/{factura_id}



