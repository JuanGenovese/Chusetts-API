# Proposal: Endpoints Core POS y Caja (Fase 1 Frontend)

## Intent
Implementar en la API FastAPI (`backend/`) los endpoints indispensables del camino crítico para permitir la construcción inmediata de un frontend (autenticación de sesión, apertura/cierre de turnos de caja, catálogo de venta y emisión de tickets).

## Scope

### In Scope
1. **Auth / Sesión:**
   - `GET /api/v1/auth/me`: Retorna los datos del usuario autenticado (ID, nombre, apellido, DNI, rol_id, rol_nombre) a partir del token JWT.
2. **Turnos de Caja (`TURNOS_CAJA`):**
   - `GET /api/v1/caja/turno-actual`: Consulta si el usuario actual tiene un turno abierto.
   - `POST /api/v1/caja/abrir-turno`: Apertura de turno con monto inicial en efectivo y observación.
   - `POST /api/v1/caja/cerrar-turno`: Cierre de turno y arqueo de caja con desglose de montos reales y observación.
3. **Catálogo y Medios de Pago:**
   - `GET /api/v1/ventas/catalogo`: Listado de productos activos vendibles con precio, categoría y disponibilidad.
   - `GET /api/v1/ventas/medios-pago`: Listado de medios de pago disponibles (`MEDIOS_PAGO`).
4. **Ventas y Tickets (`MOVIMIENTOS_VENTAS`, `PRODUCTOS_X_MOVIMIENTOS`):**
   - `POST /api/v1/ventas/tickets`: Registro transaccional de venta con desglose por medio de pago y descuento de stock.
   - `GET /api/v1/ventas/tickets`: Consulta de tickets asociados al turno actual o filtros básicos.
   - `POST /api/v1/ventas/tickets/{id}/anular`: Anulación auditada de un ticket con reversión de movimientos.

### Out of Scope
- Gestión profunda de compras de insumos a proveedores.
- Recetas complejas y producción multinivel (Fase 3).
- Pantallas administrativas avanzadas de configuración y reportes de rentabilidad.
- Migración del frontend Streamlit (se ejecuta en un cambio posterior).

## Capabilities

### New Capabilities
- `auth-me`: Obtención de perfil y rol del usuario autenticado.
- `turnos-caja`: Ciclo de vida completo del turno de caja para el operador.
- `ventas-pos`: Emisión y consulta de tickets transaccionales contra la base PostgreSQL.

## Approach
- Utilizar los modelos SQLAlchemy ya mapeados en `src/db/modelos/` (`Usuarios`, `TurnosCaja`, `Productos`, `MovimientosVentas`, `ProductoXMovimiento`, `MediosPago`, `MediosPagoxMovimientos`).
- Implementar schemas Pydantic de entrada/salida en cada dominio.
- Crear la capa de servicios (`src/domains/caja/services.py`, `src/domains/ventas/services.py`) manteniendo la lógica de negocio y transacciones fuera de los routers.
- Integrar las rutas en `src/main.py`.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Inconsistencia de stock al anular tickets | Medium | Ejecutar la anulación dentro de una transacción DB atómica revirtiendo stock. |
| Múltiples turnos abiertos simultáneos para un mismo usuario | Low | Validación de unicidad de turno activo antes de permitir la apertura. |
| Incompatibilidad de tipos en importes flotantes | Low | Validaciones estrictas en schemas Pydantic (decimal/float validado). |

## Success Criteria
- [ ] `GET /api/v1/auth/me` responde los datos del usuario logueado con JWT válido.
- [ ] Se puede abrir y cerrar un turno de caja vía API registrando los movimientos correspondientes.
- [ ] Se puede listar el catálogo vendible y los medios de pago.
- [ ] Se puede emitir un ticket de venta completo con sus productos y medios de pago, persistiendo en DB.
- [ ] Se puede anular un ticket revirtiendo sus efectos.
- [ ] Tests automáticos cubren los nuevos endpoints.
