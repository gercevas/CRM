# CRM System
Customer Relationship Management system in Python with scalable architecture.

# CRM System

Customer Relationship Management (CRM) system built in Python with a scalable architecture. This project includes a backend and frontend implementation, leveraging SQLite as the database.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
   - [Backend](#backend)
   - [Frontend](#frontend)
3. [Diagrams](#diagrams)
   - [Class Diagram](#class-diagram)
   - [Detailed Class Diagram](#detailed-class-diagram)
   - [Relational Database Model](#relational-database-model)
   - [Use Cases and Sequence Diagrams](#use-cases-and-sequence-diagrams)
4. [Installation](#installation)
5. [Running Locally](#running-locally)
6. [API Documentation](#api-documentation)

---

## Overview

This CRM system allows users to manage customer data and invoices efficiently. It is designed with a modular architecture to ensure scalability and maintainability. The backend handles business logic and persistence, while the frontend exposes an API for interaction.

---

## Architecture


El sistema sigue una arquitectura limpia por capas, que separa controladores, servicios, repositorios y esquemas. Esto facilita el mantenimiento, escalabilidad y desacoplamiento entre frontend y backend.

- Backend: FastAPI con SQLite y estructura modular.
- Frontend: Next.js (exportado desde v0.dev) para la interfaz gráfica.
- Infraestructura: Uso local, sin Docker por el momento.

### Backend
El backend está desarrollado en FastAPI, con una estructura profesional por capas:

routers/: define los endpoints REST.
schemas/: valida los datos de entrada y salida.
services/: implementa la lógica de negocio.
repositories/: gestiona el acceso a la base de datos (SQLite).
utils/database.py: permite alternar entre bases de datos según .env.

### Frontend
La interfaz de usuario está desarrollada en Next.js, exportada desde v0.dev, y conectada a la API REST del backend. Permite interactuar con el sistema CRM (crear usuarios, consultar facturas, etc.) desde el navegador.

Corre localmente en http://localhost:8000 (según configuración del frontend).
Se comunica con la API del backend en http://localhost:3000.
Está desacoplado del backend, respetando la arquitectura por capas.

---

## Diagrams

### Class Diagram

```mermaid
classDiagram
    %% Entidades principales
    class User {
        +str id
        +str first_name
        +str last_name
        +str email
        +str phone
        +str address
        +str registration_date
        +full_name() str
        +to_dict() dict
    }

    class Invoice {
        +str id
        +str user_email
        +str description
        +float amount
        +str status_code
        +str created_at
        +STATUS_OPTIONS dict
        +status_text() str
        +to_dict() dict
    }

    %% Controladores
    class UserController {
        +create_user(data: dict) User
        +get_user(user_id: str) User
        +update_user(user_id: str, data: dict) User
        +delete_user(user_id: str) bool
    }

    class InvoiceController {
        +create_invoice(data: dict) Invoice
        +get_invoice(invoice_id: str) Invoice
        +get_user_invoices(user_email: str) list[Invoice]
        +update_invoice(invoice_id: str, data: dict) Invoice
        +delete_invoice(invoice_id: str) bool
    }

    %% Repositorios
    class UserRepository {
        +save(user: User) bool
        +find_by_id(user_id: str) User
        +find_by_email(email: str) User
        +find_all() list[User]
        +delete(user_id: str) bool
    }

    class InvoiceRepository {
        +save(invoice: Invoice) bool
        +find_by_id(invoice_id: str) Invoice
        +find_by_user(user_email: str) list[Invoice]
        +find_all() list[Invoice]
        +delete(invoice_id: str) bool
    }

    %% Servicios
    class UserService {
        +user_repository: UserRepository
        +create_user(data: dict) User
        +get_user(user_id: str) User
        +update_user(user_id: str, data: dict) User
        +delete_user(user_id: str) bool
    }

    class InvoiceService {
        +invoice_repository: InvoiceRepository
        +user_service: UserService
        +create_invoice(data: dict) Invoice
        +get_invoice(invoice_id: str) Invoice
        +get_user_invoices(user_email: str) list[Invoice]
        +update_invoice(invoice_id: str, data: dict) Invoice
        +delete_invoice(invoice_id: str) bool
    }

    %% Relaciones
    User "1" -- "*" Invoice : tiene
    UserController --> UserService : usa
    InvoiceController --> InvoiceService : usa
    UserService --> UserRepository : usa
    InvoiceService --> InvoiceRepository : usa
    InvoiceService --> UserService : usa
```

- User e Invoice: Modelos de datos principales.
- Controllers: Manejan las solicitudes HTTP.
- Services: Contienen la lógica de negocio.
- Repositories: Gestionan el acceso a datos.
- Relaciones: Muestra cómo interactúan las clases.

### Detailed Class Diagram

![Detailed Class Diagram](imagenes/DetailedClassDiagram.png)


Incluye:
- Entidades de Dominio
- Capa de Controladores (FastAPI)
- Capa de Servicios
- Capa de Repositorios
- Relaciones Principales
- Patrones de Diseño
- Validaciones
- Mapeo ORM


### Relational Database Model

![Relational Database Model](imagenes/RelationalDatabase.png)

Relaciones:

Un usuario (users) puede tener múltiples facturas (invoices)
La relación se establece a través del campo user_email en la tabla invoices que referencia el campo email en la tabla users

Claves Principales (PK)
users.id: Identificador único de cada usuario
invoices.id: Identificador único de cada factura
Claves Foráneas (FK)
invoices.user_email: Referencia a users.email (relación uno a muchos)
Índices
users.email: Para búsquedas rápidas por correo
invoices.user_email: Para optimizar consultas de facturas por usuario
Feedback submitted




### Use Cases and Sequence Diagrams

#### Create User
```mermaid
sequenceDiagram
    participant Cliente as HTTP Client
    participant Controlador as FastAPI Controller
    participant Servicio as UserService
    participant Repositorio as UserRepository
    participant DB as Database

    Cliente->>Controlador: POST /users (UserCreate)
    activate Controlador
    
    Controlador->>Servicio: create_user(user_data)
    activate Servicio
    
    Servicio->>Servicio: Validar datos
    Servicio->>Repositorio: save(user_data)
    activate Repositorio
    
    Repositorio->>DB: INSERT INTO users (...)
    DB-->>Repositorio: ID del usuario creado
    Repositorio-->>Servicio: User
    
    deactivate Repositorio
    
    Servicio-->>Controlador: UserResponse
    deactivate Servicio
    
    Controlador-->>Cliente: 201 Created (UserResponse)
    deactivate Controlador
```

#### Create Invoice
```mermaid
sequenceDiagram
    participant Cliente as HTTP Client
    participant Controlador as FastAPI Controller
    participant Servicio as InvoiceService
    participant Repositorio as InvoiceRepository
    participant UserService as UserService
    participant DB as Database

    Cliente->>Controlador: POST /invoices (InvoiceCreate)
    activate Controlador
    
    Controlador->>Servicio: create_invoice(invoice_data)
    activate Servicio
    
    Servicio->>UserService: user_exists(email)
    activate UserService
    UserService-->>Servicio: True/False
    deactivate UserService
    
    alt Usuario no existe
        Servicio-->>Controlador: Error 404 Usuario no encontrado
    else Usuario existe
        Servicio->>Servicio: Validar datos de factura
        Servicio->>Repositorio: save(invoice_data)
        activate Repositorio
        
        Repositorio->>DB: INSERT INTO invoices (...)
        DB-->>Repositorio: ID de la factura creada
        Repositorio-->>Servicio: Invoice
        
        deactivate Repositorio
        Servicio-->>Controlador: InvoiceResponse
    end
    
    deactivate Servicio
    Controlador-->>Cliente: 201 Created (InvoiceResponse)
    deactivate Controlador
```

#### List Users

```mermaid
sequenceDiagram
    participant Cliente as HTTP Client
    participant Controlador as FastAPI Controller
    participant Servicio as UserService
    participant Repositorio as UserRepository
    participant DB as Database

    Cliente->>Controlador: GET /users
    activate Controlador
    
    Controlador->>Servicio: get_all_users()
    activate Servicio
    
    Servicio->>Repositorio: find_all()
    activate Repositorio
    
    Repositorio->>DB: SELECT * FROM users
    DB-->>Repositorio: Lista de usuarios
    Repositorio-->>Servicio: List[User]
    
    deactivate Repositorio
    
    Servicio->>Servicio: Convertir a UserResponse
    Servicio-->>Controlador: List[UserResponse]
    deactivate Servicio
    
    Controlador-->>Cliente: 200 OK (List[UserResponse])
    deactivate Controlador
```

---


## Deployment

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo

2. Crea un entorno virtual e instalalo (opcional)

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
```

3. Instala las dependencias
```bash
pip install -r requirements.txt
```

4. Crea el archivo .env con la configuración de base de datos

En la raíz del proyecto, crea un archivo llamado .env y agrega lo siguiente:

```bash
DATABASE_URL=sqlite:///./crm.sqlite
```

5. Inicializa la base de datos
```bash
python -m backend.init_db
```

6. Ejecuta el backend (en la terminal)
```bash
python -m backend.main
```
Esto ejecuta la lógica del CRM desde consola y conecta con la base de datos crm.sqlite.

7. Ejecuta el frontend (API FastAPI para probar desde Swagger UI)

```bash
uvicorn frontend.main_fastapi:app --reload --port 8000

```
Esto levanta el servidor de la API en modo desarrollo en el puerto 8000.

8. Accede a la documentación de la API:

Frontend (FastAPI docs): http://localhost:8000/docs


## Requisitos

