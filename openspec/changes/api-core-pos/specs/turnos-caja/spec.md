# Capability: turnos-caja

## Requirements

### Requirement: Consulta de Turno Activo
El sistema debe proveer `GET /api/v1/caja/turno-actual` para determinar si el usuario autenticado tiene actualmente un turno abierto (`fecha_hasta IS NULL`).

#### Scenario: Usuario con turno abierto
- **GIVEN** un usuario autenticado con un registro en `TURNOS_CAJA` donde `fecha_hasta` es NULL
- **WHEN** el cliente solicita `GET /api/v1/caja/turno-actual`
- **THEN** responde HTTP 200 con los datos del turno (`id`, `fecha_desde`, `efectivo_inicial`, `observacion_apertura`)

#### Scenario: Usuario sin turno abierto
- **GIVEN** un usuario autenticado sin ningún turno abierto
- **WHEN** el cliente solicita `GET /api/v1/caja/turno-actual`
- **THEN** responde HTTP 200 con `null` o mensaje explícito indicando que no hay turno activo

---

### Requirement: Apertura de Turno
El sistema debe proveer `POST /api/v1/caja/abrir-turno` para iniciar un nuevo turno de caja con un monto inicial en efectivo.

#### Scenario: Apertura exitosa
- **GIVEN** un usuario autenticado sin turno activo
- **WHEN** envía `POST /api/v1/caja/abrir-turno` con `efectivo_inicial >= 0` y `observacion_apertura`
- **THEN** el sistema crea un nuevo registro en `TURNOS_CAJA`, establece `fecha_desde` al momento actual, y responde HTTP 201 con el turno creado

#### Scenario: Intento de apertura cuando ya existe un turno abierto
- **GIVEN** un usuario que ya posee un turno abierto
- **WHEN** intenta enviar `POST /api/v1/caja/abrir-turno`
- **THEN** el sistema rechaza la operación con HTTP 400 Bad Request indicando conflicto

---

### Requirement: Cierre de Turno
El sistema debe proveer `POST /api/v1/caja/cerrar-turno` para finalizar el turno activo, registrando los importes reales contados y la observación de cierre.

#### Scenario: Cierre exitoso de turno
- **GIVEN** un usuario con turno abierto
- **WHEN** envía `POST /api/v1/caja/cerrar-turno` con `observacion_cierre` y los montos reales por medio de pago
- **THEN** el sistema actualiza `fecha_hasta`, calcula totales esperados vs reales, y responde HTTP 200 con el resumen del arqueo
