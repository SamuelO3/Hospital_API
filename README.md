# Hospital_API
## API de sistema hospitalario

## **1. Información General**
- **Nombre del Proyecto**: Sistema Hospitalario.
- **Versión del Sistema**: 1.2.0
- **Fecha de Creación**: 08/2025
- **Autor(es)**: Emanuel Medina Arboleda, Samuel Ortiz Bermudez, Julián Garcia Guevara.
- **Propósito**: Proporcionar información técnica detallada sobre la instalación, configuración, funcionamiento y mantenimiento de la API REST desarrollada en FastAPI con integracaion con base de datos server less, para la gestión hospitalaria.

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
- Usuarios
- Tokens JWT

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
- Librerías: Pydantic, Typing, python-jose, SQLAlchemy, Alembic, bcrypt.
- Otros: Git (opcional).

---

## **4. Instalación**
### **4.1 Descarga de Archivos**
git clone https://github.com/SamuelO3/Hospital_API.git

### **4.2 Instalación Paso a Paso**
1. Instalar dependencias: pip install -r requirements.txt
2. Iniciar el entorno virtual .env/scripts/activate
3. Ejecutar servidor: uvicorn main:app --reload

### **4.3 Configuración Inicial**
- El sistema no requiere configuración adicional de base de datos.
- Acceder a la documentación interactiva en:
  - http://127.0.0.1:8000/docs (Swagger UI).
  - http://127.0.0.1:8000/redoc (Redoc).

---

## **5. Arquitectura del Sistema**
### **5.1 Diagrama de Arquitectura**
```plaintext
HOSPITAL_API/
├── alembic/
│   └── versions/
│
├── auth/
│   ├── dependencies.py
│   ├── JWTHandler.py
│   └── security.py
│
├── controllers/
│   ├── auth_controller.py
│   ├── bill_controller.py
│   ├── diagnosis_controller.py
│   ├── medical_appointment_controller.py
│   ├── medic_controller.py
│   ├── nurse_controller.py
│   ├── patient_controller.py
│   ├── user_controller.py
│   └── user_information_controller.py
│
├── database/
│   └── config.py
│
├── models/
│   ├── bill.py
│   ├── diagnosis.py
│   ├── medical_appointment.py
│   ├── medic.py
│   ├── nurse.py
│   ├── patient.py
│   ├── user.py
│   └── user_information.py
│
├── routes/
│   ├── authRouter.py
│   ├── billRouter.py
│   ├── diagnosisRouter.py
│   ├── medical_appointmentRouter.py
│   ├── medicRouter.py
│   ├── nurseRouter.py
│   ├── patientRouter.py
│   ├── userRouter.py
│   └── user_informationRouter.py
│
├── schemas/
│   ├── auth_schema.py
│   ├── bill_schema.py
│   ├── diagnosis_schema.py
│   ├── medical_appointment_schema.py
│   ├── medic_schema.py
│   ├── nurse_schema.py
│   ├── patient_schema.py
│   ├── user_schema.py
│   └── user_information_schema.py
│
├── utils/
│   └── role_utils.py
│
├── main.py
├── .env
└── requirements.txt
```                

### **5.2 Componentes Principales**
- **alembic/**: ubicacion de las migraciones de los modelos.
- **auth/**: Contiene las herramientas necesarias para la seguridad de la API.
- **controllers/**: Contiene los metodos necesarios para interactuar con la base de datos.
- **database/**: Contiene la confirguracion de la base de datos.
- **models/**: Define los modelos de datos (usando SQLAlchemy).
- **routers/**: Contiene los endpoints organizados por entidad.
- **schemas/**: Contiene los schemas de datos (usando pydantic).
- **utils/**: Cotiene herramientas para manejar los roles proteccion en los endpoints.
- **main.py**: Punto de entrada de la aplicación.
- **requirements.txt**: librerias y frameworks necesarios para la API.

---

## **6. Operación del Sistema**
### **6.1 Descripción General**
El sistema funciona como un servidor REST que permite realizar operaciones CRUD sobre entidades hospitalarias. Cada recurso tiene sus rutas específicas bajo el esquema:
-  /patient/ → Gestión de pacientes.
-  /medic/ → Gestión de médicos.
-  /nurse/ → Gestión de enfermeras.
-  /medical_appointment/ → Gestión de citas.
-  /bill/ → Gestión de facturas.
-  /diagnosis/ → Registro de diagnósticos.
-  /auth/ → Metodos de registro e inicio de sesion.

### **6.2 Flujos de Trabajo Principales**
1. **Gestión de Pacientes/Medicos/Enfermeras**:
-  Crear un patient/medic/nurse → POST (/patient),(/medic) o (/nurse)
-  Consultar pacientes/medic/nurse → GET (/patient),(/medic) o (/nurse)
-  Consultar parciente/medic/nurse por id → GET (/patient/{id_patient}),(/medic/{id_medic}) o (/nurse/{id_nurse})
-  Editar paciente/medic/nurse → PUT (/patient/update{id_patient}),(/medic/{id_medic}) o (/nurse/{id_nurse})
-  Eliminar paciente/medic/nurse → DELETE (/patient/delete{id_patient}),(/medic/{id_medic}) o (/nurse/{id_nurse})
  
2. **Gestión de Citas Médicas**:
-  Registrar cita → POST /appointment/
-  Consultar citas → GET /appointmen/
-  Consultar cita por id → GET /appointmen/{id_medical_appointmen}
-  Actualizar cita → PUT /appointmen/{id_medical_appointmen}
-  Cancelar cita → DELETE /appointmen/{id_medical_appointmen}

4. **Generación de Diagnosticos**:
-  Crear Diagnostico → POST /diagnostico/
-  Consultar diagnosticos → GET /diagnostico/
-  Consultar diagnostico por id → GET /diagnostico/{diagnostico_id}
-  Actualizar diagnostico → PUT /diagnostico/{diagnostico_id}
-  Eliminar diagnostico → DELETE /diagnostico/{diagnostico_id}

5. **Generación de Facturas**:
-  Crear factura → POST /bill/
-  Consultar facturas → GET /bill/
-  Consultar facturas por paciente → GET /bill/patient
-  Actualizar facturas → PUT /bill/{id_bill}
-  Eliminar facturas → DELETE /bill/{id_bill}
