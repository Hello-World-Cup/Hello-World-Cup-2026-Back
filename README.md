# HWC Server

Backend API desarrollada en **Python** con **FastAPI**, estructurada bajo **Arquitectura Hexagonal (Ports & Adapters)**.  
El objetivo principal del proyecto es **aislar completamente el dominio** de los frameworks y detalles de infraestructura, permitiendo que el núcleo de negocio evolucione de forma independiente y mantenible.

Este repositorio representa una **base sólida para servicios backend modernos**, preparada para escalar, testear y adaptarse a cambios tecnológicos (DB, frameworks web, integraciones externas).

---

## 📌 Descripción del proyecto

**HWC Server** implementa una API HTTP con FastAPI y persistencia en **PostgreSQL** usando **SQLAlchemy**.  
La arquitectura está organizada en **capas concéntricas**, donde:

- El **dominio** contiene la lógica de negocio pura.
- Los **puertos** definen contratos (interfaces).
- Los **adaptadores** implementan dichos contratos para tecnologías concretas (FastAPI, PostgreSQL, etc.).

Incluye además:
- Configuración por variables de entorno.
- Inicialización automática de base de datos.
- Seeders para entorno de desarrollo.
- Contenedores Docker listos para desarrollo local.

---

## 🚀 Funcionalidades principales

- ✅ API HTTP con FastAPI
- ✅ Documentación automática con Swagger (`/docs`)
- ✅ Healthcheck (`GET /health`)
- ✅ Ejemplo de endpoints (`/test`)
- ✅ Respuestas HTTP con formato unificado
- ✅ Persistencia en PostgreSQL con SQLAlchemy
- ✅ Inicialización automática de tablas
- ✅ Seeder automático en entorno **development**
- ✅ Dockerfile + Docker Compose

---

## 🛠️ Tecnologías utilizadas

- **Python 3.11**
- **FastAPI**
- **Uvicorn**
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic v2**
- **pydantic-settings**
- **Docker / Docker Compose**

Dependencias definidas en `requirements.txt`.

---

## ⚙️ Requisitos previos

- Docker
- Docker Compose

---

## 📂 Estructura del proyecto

```text
app/
├── adapters/                 # Infraestructura (adaptadores)
│   ├── database/             # Persistencia
│   │   └── postgres/
│   │       ├── connection.py # Engine + Session
│   │       ├── models/       # Modelos SQLAlchemy
│   │       ├── repositories/ # Implementaciones concretas
│   │       └── seeders/      # Datos iniciales (dev)
│   └── routing/              # Adaptador web (FastAPI)
│       ├── main.py           # Punto de entrada ASGI
│       ├── config.py         # Configuración FastAPI (CORS, routers)
│       └── routers/          # Endpoints
│
├── domain/                   # Núcleo del negocio
│   ├── core/
│   │   ├── config.py
│   │   ├── enums.py
│   │   └── exceptions/
│   ├── dtos/                 # Data Transfer Objects
│   └── services/             # Servicios de dominio
│
└── ports/                    # Puertos (interfaces)
    ├── driven/               # Hacia infraestructura (DB, APIs externas)
    └── driving/              # Hacia el dominio (casos de uso)
```

---


## 📈Flujo
<img width="796" height="597" alt="WHC SERVER ARCHITECTURE drawio" src="https://github.com/user-attachments/assets/1b2f5ea8-bb01-479f-8485-0a30fc330cca" />

---
## 📦Instalacion/Ejecucion

### Docker Compose 

```bash
cp .env.development.example .env
docker compose up --build
```


### API disponible en

```bash 
http://localhost:8000
```

### Swagger
```bash
http://localhost:8000/docs
```

---

