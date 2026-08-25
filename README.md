# Chusetts Backend API

Backend refactorizado para el sistema de gestión de cervecería Chusetts, desarrollado en Python con **FastAPI** y estructurado mediante una arquitectura guiada por dominios (**Domain-Driven / Feature-First**) con 3 capas estrictas por módulo.

---

## 🏛️ Arquitectura del Sistema

El proyecto sigue una arquitectura en 3 capas desacopladas dentro de cada dominio:

```text
src/domains/<domain_name>/
├── routes.py      # Capa 1: Definición de endpoints HTTP, controladores y esquemas Pydantic.
├── service.py     # Capa 2: Lógica de negocio pura, orquestación y validaciones de dominio.
├── repository.py  # Capa 3: Persistencia, consultas SQL / llamadas a Stored Procedures.
└── schemas.py     # Esquemas de entrada y salida (Pydantic DTOs).
```

### Dominios Principales

- **`auth`**: Gestión de usuarios, autenticación Bearer JWT, roles (`admin`, `cajero`).
- **`caja`**: Apertura/cierre de turnos, arqueo de caja (esperado vs. real), registro de movimientos.
- **`inventario`**: Control de stock de productos, categorías, productos compuestos y recetas.
- **`ventas`**: Procesamiento de ventas, carritos, generación de tickets y medios de pago.

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.10 o superior
- Virtualenv

### Instalación

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar Servidor en Desarrollo

```bash
uvicorn src.main:app --reload --port 8000
```

La documentación interactiva OpenAPI (Swagger UI) estará disponible en:
- `http://localhost:8000/docs`


    # Comandos base de datos

- **Crear migración:**

```bash
alembic revision --autogenerate -m "<mensaje_migracion>"
```

- **Correr una migración:**

```bash
alembic upgrade heads
```

- **Volver atrás una migración:**

```bash
alembic downgrade -1
```

- **Revertir todas las migraciones:**

```bash
alembic downgrade base
```

- **Mostrar el historial de migraciones:**

```bash
alembic history
```

- **Ver el estado actual de las migraciones:**

```bash
alembic current
```

- **Revisar diferencias entre los modelos y la base de datos:**

```bash
alembic check --autogenerate
```

- **Crear una migración vacía:**

```bash
alembic revision -m "<mensaje_migracion>"
```

- **Listar los encabezados de las migraciones actuales:**

```bash
alembic heads
```

- **Realizar el merge entre las migraciones para resolver inconsistencias:**

```bash
alembic merge -m "<mensaje_migracion>" <id_encabezado_1> <id_encabezado_2>
```

Con los comandos mencionados anteriormente se pueden realizar las totalidad de las acciones necesarias en la base de datos propiamente dicha.

# Comando para actualizar requirement.txt

cada vez que instalen dependencias nuevas ejecutar:

```bash
   pip freeze > requirements.txt
```



# 1. Revertir todas las tablas
docker compose exec backend alembic downgrade base
# 2. Volver a aplicar la migración actualizada
docker compose exec backend alembic upgrade head




el calculo del cierre de caja tiene que ser en base al calculo de todos los movimientos 
una vista  contable que junte todos los movimientos y me retorne el saldo final de la caja
