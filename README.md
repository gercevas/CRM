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

### Backend

The backend is responsible for:
- Business logic implementation.
- Data validation using custom validators.
- Persistence management via repositories.
- Interaction with SQLite database.

Key components:
- **Controllers**: Handle user and invoice operations.
- **Services**: Implement business logic.
- **Repositories**: Manage data storage and retrieval.
- **Models**: Represent entities like `User` and `Invoice`.

### Frontend

The frontend exposes the backend functionality via a FastAPI-based REST API. It includes:
- **Routers**: Define API endpoints for users and invoices.
- **Schemas**: Validate and structure API request/response data.
- **Services**: Bridge between frontend and backend logic.

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

### Detailed Class Diagram

![Detailed Class Diagram](imagenes/DetailedClassDiagram.png)

### Relational Database Model

![Relational Database Model](imagenes/RelationalDatabase.png)

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

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo