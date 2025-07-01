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

The system follows a clean layered architecture that separates controllers, services, repositories, and schemas. This promotes maintainability, scalability, and decoupling between frontend and backend.

- Backend: Built with FastAPI and SQLite using a modular structure.
- Frontend: Implemented with Next.js (exported from v0.dev) as the graphical user interface.
- Infrastructure: Local development setup; Docker not yet configured.

### Backend
The backend is developed using FastAPI with a clean, professional layered architecture:

- routers/: Defines REST endpoints.
- schemas/: Validates input and output data.
- services/: Implements business logic.
- repositories/: Manages access to the database (SQLite).
- utils/database.py: Enables switching databases via .env.

### Frontend
The frontend interface is developed using Next.js (exported from v0.dev), and connects to the backend’s REST API. It allows user interaction with the CRM system (create users, retrieve invoices, etc.) directly from the browser.

- Runs locally at: http://localhost:8000 (configurable).
- Communicates with backend API on: http://localhost:3000.
- Decoupled from the backend, respecting the layered architecture.
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

- User and Invoice: Main data models
- Controllers: Handle HTTP requests
- Services: Contain business logic
- Repositories: Manage data access
- Relationships: Shows how classes interact

### Detailed Class Diagram

![Detailed Class Diagram](imagenes/DetailedClassDiagram.png)


Incluye:
- Domain entities
- Controller layer (FastAPI)
- Service layer
- Repository layer
- Main relationships
- Design patterns
- Validations
- ORM mapping


### Relational Database Model

![Relational Database Model](imagenes/RelationalDatabase.png)

Relationships:     

A user (users) can have multiple invoices
The relationship is established through the user_email field in the invoices table that references the email field in the users table

Primary Keys (PK)
users.id: Unique identifier for each user
invoices.id: Unique identifier for each invoice

Foreign Keys (FK)
invoices.user_email: References users.email (one-to-many relationship)

Indexes
users.email: For fast email lookups
invoices.user_email: To optimize invoice queries by user


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

2. Create a virtual environment and install it (optional)

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create the .env file with database configuration

In the root of the project, create a file called .env and add the following:

```bash
DB_TYPE=sqlite
SQLITE_PATH=crm.sqlite
```

5. Initialize the database
```bash
python -m backend.init_db
```

6. Run the backend (in the terminal)
```bash
python -m backend.main
```
This runs the CRM logic from the console and connects to the crm.sqlite database.

7. Run the frontend (API FastAPI for testing from Swagger UI)

```bash
uvicorn frontend.main_fastapi:app --reload --port 8000

```
This starts the API server in development mode on port 8000.

8. Access the API documentation:

Frontend (FastAPI docs): http://localhost:8000/docs

---

## API Endpoints

Below is a summary of the available API endpoints exposed by the FastAPI backend:

| Endpoint               | Method | Description                        |
|------------------------|--------|------------------------------------|
| `/users`              | GET    | Retrieve a list of all users       |
| `/users/{user_id}`    | GET    | Get details of a specific user     |
| `/users`              | POST   | Create a new user                  |
| `/users/{user_id}`    | PUT    | Update an existing user            |
| `/users/{user_id}`    | DELETE | Delete a user                      |
| `/invoices`           | GET    | Retrieve all invoices              |
| `/invoices/{id}`      | GET    | Get a specific invoice             |
| `/invoices`           | POST   | Create a new invoice               |
| `/invoices/{id}`      | PUT    | Update an existing invoice         |
| `/invoices/{id}`      | DELETE | Delete an invoice                  |
| `/invoices/user/{email}` | GET | Get all invoices by user email     |

These endpoints return JSON responses and follow RESTful principles.



