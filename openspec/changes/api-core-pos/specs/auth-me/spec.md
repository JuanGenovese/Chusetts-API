# Capability: auth-me

## Requirements

### Requirement: Perfil de usuario autenticado
El sistema debe proveer un endpoint `GET /api/v1/auth/me` protegido por autenticación Bearer JWT que retorne los datos esenciales del usuario actual para que el cliente (frontend) pueda resolver su identidad y permisos.

#### Scenario: Usuario autenticado consulta su perfil
- **GIVEN** un token JWT válido emitido para un usuario existente en la base de datos
- **WHEN** el cliente envía una solicitud `GET /api/v1/auth/me` con la cabecera `Authorization: Bearer <token>`
- **THEN** el sistema responde con HTTP 200 OK y el cuerpo contiene:
  - `id`: identificador único del usuario
  - `dni`: DNI del usuario
  - `nombre`: nombre de pila
  - `apellido`: apellido
  - `rol_id`: ID del rol asignado
  - `rol_nombre`: nombre del rol (e.g., 'administrador', 'cajero')
  - `activo`: booleano que indica si el usuario está habilitado

#### Scenario: Solicitud sin token o con token inválido
- **GIVEN** una solicitud sin cabecera `Authorization` o con un token expirado o corrupto
- **WHEN** el cliente envía `GET /api/v1/auth/me`
- **THEN** el sistema responde con HTTP 401 Unauthorized

#### Scenario: Usuario del token ya no existe o está inactivo
- **GIVEN** un token JWT válido para un usuario que fue dado de baja (`activo == false`)
- **WHEN** el cliente envía `GET /api/v1/auth/me`
- **THEN** el sistema responde con HTTP 403 Forbidden o 401 Unauthorized indicando que la cuenta no está activa
