from sqlalchemy.orm import Session
from datetime import datetime
from src.db.modelos.auth import CuentaAuth
from src.db.modelos.usuarios import Usuarios
from src.domains.auth.schemas import CuentaAuthCreate
from src.core.security import generar_contrasena_hasheada, verificar_contrasena
from src.db.database import connection

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def obtener_cuenta_por_dni(self, dni: str) -> CuentaAuth | None:
        return self.db.query(CuentaAuth).filter(CuentaAuth.dni == dni).first()

    def crear_cuenta(self, datos: CuentaAuthCreate) -> Usuarios:
        existente = self.obtener_cuenta_por_dni(datos.dni)
        if existente:
            raise ValueError(f"Ya existe una cuenta registrada para el DNI '{datos.dni}'.")
    
        hashed_pw = generar_contrasena_hasheada(datos.password)
        nueva_cuenta = CuentaAuth(
            dni=datos.dni,
            password_hash=hashed_pw,
            activo=True
        )
        self.db.add(nueva_cuenta)
        self.db.flush()  # populate nueva_cuenta.id before using it as FK

        fecha_nac = datetime.strptime(datos.fecha_nac, "%d/%m/%Y").date()

        nuevo_usuario = Usuarios(
            nombre=datos.nombre,
            apellido=datos.apellido,
            dni=datos.dni,
            email=datos.email,
            telefono=datos.telefono,
            fecha_nac=fecha_nac,
            rol_id=datos.rol_id,
            cuenta_id=nueva_cuenta.id
        )
        self.db.add(nuevo_usuario)
        self.db.flush()
        self.db.commit()
        
        return nuevo_usuario
    
    def autenticar_usuario(self, dni: str, password: str) -> CuentaAuth:
        cuenta = self.obtener_cuenta_por_dni(dni)
        if not cuenta:
            raise ValueError("Credenciales inválidas (DNI o contraseña incorrecta).")
        
        if not cuenta.activo:
            raise ValueError("La cuenta de usuario se encuentra inactiva.")
    
        if not verificar_contrasena(password, str(cuenta.password_hash)):
            raise ValueError("Credenciales inválidas (DNI o contraseña incorrecta).")
    
        return cuenta
    