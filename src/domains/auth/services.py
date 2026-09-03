from sqlalchemy.orm import Session
from src.db.modelos.auth import CuentaAuth
from src.domains.auth.schemas import CuentaAuthCreate
from src.core.security import generar_contrasena_hasheada, verificar_contrasena

def obtener_cuenta_por_dni(db: Session, dni: str) -> CuentaAuth | None:
    """Busca una cuenta en el esquema auth por su DNI."""
    return db.query(CuentaAuth).filter(CuentaAuth.dni == dni).first()

def crear_cuenta_auth(db: Session, datos: CuentaAuthCreate) -> CuentaAuth:
    """Crea una nueva cuenta de acceso en el esquema auth vinculada al esquema public."""
    existente = obtener_cuenta_por_dni(db, datos.dni)
    if existente:
        raise ValueError(f"Ya existe una cuenta registrada para el DNI '{datos.dni}'.")

    hashed_pw = generar_contrasena_hasheada(datos.password)
    nueva_cuenta = CuentaAuth(
        dni=datos.dni,
        password_hash=hashed_pw,
        tipo_usuario=datos.tipo_usuario,
        usuario_adm_id=datos.usuario_adm_id,
        usuario_cli_id=datos.usuario_cli_id,
        activo=True
    )
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)
    return nueva_cuenta

def autenticar_usuario(db: Session, dni: str, password: str) -> CuentaAuth:
    """Valida las credenciales DNI y contraseña contra el esquema auth."""
    cuenta = obtener_cuenta_por_dni(db, dni)
    if not cuenta:
        raise ValueError("Credenciales inválidas (DNI o contraseña incorrecta).")
    
    if not cuenta.activo:
        raise ValueError("La cuenta de usuario se encuentra inactiva.")

    if not verificar_contrasena(password, str(cuenta.password_hash)):
        raise ValueError("Credenciales inválidas (DNI o contraseña incorrecta).")

    return cuenta
