# Design: Endpoints Core POS y Caja

## Context
El backend FastAPI cuenta con autenticación JWT global y modelos SQLAlchemy para `Usuarios`, `TurnosCaja`, `Movimientos`, `MovimientosVentas`, `Productos`, `ProductoXMovimiento` y `MediosPago`. Se deben exponer y conectar los endpoints requeridos por el frontend.

## Architecture & Domain Organization

```
backend/src/
├── core/
│   └── dependencies.py        # Reutilizar obtener_usuario_actual
├── domains/
│   ├── auth/
│   │   ├── routes.py          # Agregar GET /me
│   │   └── schemas.py         # Agregar UsuarioMeResponse
│   ├── caja/                  # Dominio modular de turnos de caja
│   │   ├── __init__.py
│   │   ├── routes.py          # GET /turno-actual, POST /abrir-turno, POST /cerrar-turno
│   │   ├── schemas.py         # TurnoApertura, TurnoCierre, TurnoResponse, ArqueoCierreResponse
│   │   └── services.py        # CajaService (lógica transaccional de turnos)
│   └── ventas/                # Dominio de catálogo y punto de venta
│       ├── routes.py          # GET /catalogo, GET /medios-pago, POST /tickets, GET /tickets, POST /tickets/{id}/anular
│       ├── schemas.py         # TicketCreateRequest, TicketResponse, CatalogoItemResponse, MedioPagoResponse
│       └── services.py        # VentasService (orquestación atómica de tickets y stock)
```

## Data Flow & Transaccionalidad

1. **GET `/api/v1/auth/me`**:
   - Resuelve el usuario actual mediante `obtener_usuario_actual` (ya inyectado con JWT).
   - Retorna proyección limpia con DNI, nombre, apellido, rol e ID.

2. **Apertura de Turno (`POST /api/v1/caja/abrir-turno`)**:
   - Valida que `TurnosCaja.filter(usuario_id == user.id, fecha_hasta == None)` no exista.
   - Crea `TurnosCaja` con `efectivo_inicial`, `observacion_apertura` y `fecha_desde = datetime.now()`.

3. **Cierre de Turno (`POST /api/v1/caja/cerrar-turno`)**:
   - Recupera el turno abierto del usuario.
   - Suma los importes esperados calculados a partir de `MOVIMIENTOS_VENTAS` asociados a dicho turno (desglosados por `MEDIOS_PAGO_X_MOVIMIENTOS`).
   - Setea `fecha_hasta = datetime.now()`, guarda `observacion_cierre` y devuelve la comparativa entre esperado y real.

4. **Emisión de Ticket (`POST /api/v1/ventas/tickets`)**:
   - **Transacción atómica**:
     1. Verifica que el cajero tenga turno activo (`turno_caja_id`).
     2. Inserta en `MOVIMIENTOS` con `tipo_id` correspondiente a "Venta".
     3. Inserta en `MOVIMIENTOS_VENTAS` vinculando `movimiento_id`, `turno_caja_id`, `monto_total`.
     4. Itera items e inserta en `PRODUCTOS_X_MOVIMIENTOS`.
     5. Itera pagos e inserta en `MEDIOS_PAGO_X_MOVIMIENTOS`.
     6. `db.commit()` y retorno del ticket completo.

## Error Handling
- Errores de validación de negocio disparan `ValueError` en services y se transforman en `HTTPException(400)` en routes.
- Intentos de venta sin turno activo retornan `HTTP 400` con mensaje claro.
- Anulaciones de tickets no encontrados retornan `HTTP 404`.
