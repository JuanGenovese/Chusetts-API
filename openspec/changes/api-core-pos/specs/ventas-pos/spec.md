# Capability: ventas-pos

## Requirements

### Requirement: Catálogo y Medios de Pago
El sistema debe proveer endpoints para obtener el catálogo de productos disponibles para la venta y los medios de pago configurados.

#### Scenario: Listar catálogo para el POS
- **WHEN** un cliente autenticado solicita `GET /api/v1/ventas/catalogo`
- **THEN** responde HTTP 200 con la lista de productos donde `activo == true`, incluyendo `id`, `nombre`, `precio_venta`, `stock_minimo`

#### Scenario: Listar medios de pago
- **WHEN** un cliente autenticado solicita `GET /api/v1/ventas/medios-pago`
- **THEN** responde HTTP 200 con la lista de medios de pago (`id`, `medio_pago`)

---

### Requirement: Emisión de Ticket de Venta
El sistema debe permitir emitir un ticket transaccional registrando el movimiento de venta, los productos vendidos y los medios de pago utilizados.

#### Scenario: Venta exitosa
- **GIVEN** un operador con turno de caja abierto
- **WHEN** envía `POST /api/v1/ventas/tickets` con:
  - `productos`: lista de `{ id_producto, cantidad_producto, precio }`
  - `pagos`: lista de `{ id_medio_pago, monto }`
  - La suma de los montos de pago coincide exactamente con el monto total de productos
- **THEN** el sistema:
  1. Crea un registro en `MOVIMIENTOS` (tipo Venta)
  2. Crea un registro en `MOVIMIENTOS_VENTAS` asociado al `turno_caja_id`
  3. Inserta los registros en `PRODUCTOS_X_MOVIMIENTOS`
  4. Inserta los registros en `MEDIOS_PAGO_X_MOVIMIENTOS`
  5. Responde HTTP 201 Created con el ID del ticket y detalle completo

#### Scenario: Venta rechazada por no tener turno abierto
- **GIVEN** un operador sin turno abierto
- **WHEN** intenta enviar `POST /api/v1/ventas/tickets`
- **THEN** responde HTTP 400 Bad Request indicando que se requiere un turno abierto

---

### Requirement: Anulación de Ticket
El sistema debe permitir anular un ticket previamente emitido, garantizando trazabilidad y auditoría.

#### Scenario: Anulación exitosa
- **GIVEN** un ticket de venta existente que no fue anulado previamente
- **WHEN** un usuario con permisos envía `POST /api/v1/ventas/tickets/{id}/anular` con motivo
- **THEN** el sistema marca o revierte el movimiento de venta y responde HTTP 200
