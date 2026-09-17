# Tasks: Endpoints Core POS y Caja

## Review Workload Forecast
| Field | Value |
|---|---|
| Estimated changed lines | ~450 |
| Total tasks | 6 |

---

## Task List

- [x] 1. Endpoint `GET /api/v1/auth/me`
  - [x] 1.1 Definir schema `UsuarioMeResponse` en `src/domains/auth/schemas.py`.
  - [x] 1.2 Implementar ruta `GET /me` en `src/domains/auth/routes.py` inyectando `obtener_usuario_actual`.

- [x] 2. Dominio y Endpoints de Turnos de Caja (`src/domains/caja/`)
  - [x] 2.1 Crear schemas de apertura, cierre y consulta en `src/domains/caja/schemas.py`.
  - [x] 2.2 Implementar `CajaService` en `src/domains/caja/services.py` con validación de turno único y cálculo de arqueo.
  - [x] 2.3 Implementar rutas `GET /turno-actual`, `POST /abrir-turno`, `POST /cerrar-turno` en `src/domains/caja/routes.py`.
  - [x] 2.4 Registrar router de `caja` en `src/main.py`.

- [x] 3. Catálogo y Medios de Pago en `src/domains/ventas/`
  - [x] 3.1 Definir schemas para productos de catálogo y medios de pago en `src/domains/ventas/schemas.py`.
  - [x] 3.2 Implementar queries en `VentasService` para listar productos vendibles activos y medios de pago.
  - [x] 3.3 Exponer rutas `GET /catalogo` y `GET /medios-pago` en `src/domains/ventas/routes.py`.

- [x] 4. Emisión y Consulta de Tickets en `src/domains/ventas/`
  - [x] 4.1 Definir schemas `TicketCreateRequest`, `TicketDetalleResponse` en `src/domains/ventas/schemas.py`.
  - [x] 4.2 Implementar lógica transaccional de emisión en `VentasService` (asociación con `MOVIMIENTOS`, `MOVIMIENTOS_VENTAS`, items y pagos).
  - [x] 4.3 Exponer `POST /tickets` y `GET /tickets` en `src/domains/ventas/routes.py`.

- [x] 5. Anulación de Tickets
  - [x] 5.1 Implementar método `anular_ticket` en `VentasService` con auditoría.
  - [x] 5.2 Exponer `POST /tickets/{id}/anular` en `src/domains/ventas/routes.py`.

- [x] 6. Tests automatizados de integración
  - [x] 6.1 Crear pruebas para `/auth/me`.
  - [x] 6.2 Crear pruebas para flujo de caja (abrir -> consultar -> cerrar).
  - [x] 6.3 Crear pruebas para emisión y anulación de ticket.
