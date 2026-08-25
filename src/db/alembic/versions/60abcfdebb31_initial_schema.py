"""Initial schema

Revision ID: 60abcfdebb31
Revises: 
Create Date: 2026-08-17 20:17:22.451599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60abcfdebb31'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. roles_adm
    op.create_table('ROLES_ADM',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('rol', sa.String(length=25), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ROLES_ADM_id'), 'ROLES_ADM', ['id'], unique=False)

    # 2. roles_cli
    op.create_table('ROLES_CLI',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('rol', sa.String(length=25), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ROLES_CLI_id'), 'ROLES_CLI', ['id'], unique=False)

    # 3. tipos_movimientos
    op.create_table('TIPOS_MOVIMIENTOS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('tipo', sa.String(length=25), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_TIPOS_MOVIMIENTOS_id'), 'TIPOS_MOVIMIENTOS', ['id'], unique=False)

    # 4. usuarios_adm
    op.create_table('USUARIOS_ADM',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.Column('apellido', sa.String(length=50), nullable=False),
        sa.Column('dni', sa.String(length=50), nullable=False, unique=True),
        sa.Column('rol_adm_id', sa.Integer(), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['rol_adm_id'], ['ROLES_ADM.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_USUARIOS_ADM_id'), 'USUARIOS_ADM', ['id'], unique=False)

    # 5. usuarios_cli
    op.create_table('USUARIOS_CLI',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('rol_cli_id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.Column('apellido', sa.String(length=50), nullable=False),
        sa.Column('dni', sa.String(length=50), nullable=False, unique=True),
        sa.Column('email', sa.String(length=150), nullable=False, unique=True),
        sa.Column('telefono', sa.String(length=50), nullable=True),
        sa.Column('fecha_nac', sa.Date(), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['rol_cli_id'], ['ROLES_CLI.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_USUARIOS_CLI_id'), 'USUARIOS_CLI', ['id'], unique=False)

    # 6. turnos_caja
    op.create_table('TURNOS_CAJA',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('usuario_adm_id', sa.Integer(), nullable=False),
        sa.Column('fecha_desde', sa.DateTime(), nullable=False),
        sa.Column('fecha_hasta', sa.DateTime(), nullable=True),
        sa.Column('efectivo_inicial', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('observacion_apertura', sa.String(length=500), nullable=True),
        sa.Column('observacion_cierre', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['usuario_adm_id'], ['USUARIOS_ADM.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_TURNOS_CAJA_id'), 'TURNOS_CAJA', ['id'], unique=False)

    # 7. cupones
    op.create_table('CUPONES',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.Column('codigo', sa.String(length=50), nullable=False, unique=True),
        sa.Column('valor', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CUPONES_id'), 'CUPONES', ['id'], unique=False)

    # 8. medios_pago
    op.create_table('MEDIOS_PAGO',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('medio_pago', sa.String(length=20), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_MEDIOS_PAGO_id'), 'MEDIOS_PAGO', ['id'], unique=False)

    # 9. productos
    op.create_table('PRODUCTOS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('valor_puntos', sa.Integer(), nullable=True),
        sa.Column('nombre', sa.String(length=100), nullable=False, unique=True),
        sa.Column('precio_venta', sa.Float(), nullable=False),
        sa.Column('stock_minimo', sa.Float(), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_PRODUCTOS_id'), 'PRODUCTOS', ['id'], unique=False)

    # 10. proveedores
    op.create_table('PROVEEDORES',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('nombre', sa.String(length=100), nullable=False, unique=True),
        sa.Column('telefono', sa.String(length=50), nullable=True),
        sa.Column('mail', sa.String(length=100), nullable=True),
        sa.Column('localidad', sa.String(length=50), nullable=True),
        sa.Column('barrio', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_PROVEEDORES_id'), 'PROVEEDORES', ['id'], unique=False)

    # 11. movimientos (tabla central)
    op.create_table('MOVIMIENTOS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('tipo_id', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['tipo_id'], ['TIPOS_MOVIMIENTOS.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_MOVIMIENTOS_id'), 'MOVIMIENTOS', ['id'], unique=False)

    # 12. movimientos_ventas
    op.create_table('MOVIMIENTOS_VENTAS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('movimiento_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('turno_caja_id', sa.Integer(), nullable=False),
        sa.Column('monto_total', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['movimiento_id'], ['MOVIMIENTOS.id'], ),
        sa.ForeignKeyConstraint(['turno_caja_id'], ['TURNOS_CAJA.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_MOVIMIENTOS_VENTAS_id'), 'MOVIMIENTOS_VENTAS', ['id'], unique=False)

    # 13. cupones_usuario (ahora se crea DESPUÉS de MOVIMIENTOS_VENTAS)
    op.create_table('CUPONES_USUARIO',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('usuario_cli_id', sa.Integer(), nullable=False),
        sa.Column('cupon_id', sa.Integer(), nullable=False),
        sa.Column('movimiento_venta_id', sa.Integer(), nullable=True),
        sa.Column('disponible', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['cupon_id'], ['CUPONES.id'], ),
        sa.ForeignKeyConstraint(['usuario_cli_id'], ['USUARIOS_CLI.id'], ),
        sa.ForeignKeyConstraint(['movimiento_venta_id'], ['MOVIMIENTOS_VENTAS.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CUPONES_USUARIO_id'), 'CUPONES_USUARIO', ['id'], unique=False)

    # 14. movimientos_compra
    op.create_table('MOVIMIENTOS_COMPRA',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('id_movimiento', sa.Integer(), nullable=False, unique=True),
        sa.Column('fecha', sa.DateTime(), nullable=False),
        sa.Column('costo_total', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('detalle', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['id_movimiento'], ['MOVIMIENTOS.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_MOVIMIENTOS_COMPRA_id'), 'MOVIMIENTOS_COMPRA', ['id'], unique=False)

    # 15. movimientos_gasto
    op.create_table('MOVIMIENTOS_GASTO',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('movimiento_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('concepto', sa.String(length=100), nullable=False),
        sa.Column('importe', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('detalle', sa.String(length=150), nullable=True),
        sa.ForeignKeyConstraint(['movimiento_id'], ['MOVIMIENTOS.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_MOVIMIENTOS_GASTO_id'), 'MOVIMIENTOS_GASTO', ['id'], unique=False)

    # 16. stock
    op.create_table('STOCK',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('nombre', sa.String(length=50), nullable=False, unique=True),
        sa.Column('cantidad', sa.Float(), nullable=False),
        sa.Column('fecha_vencimiento', sa.Date(), nullable=True),
        sa.Column('cantidad_minima', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_STOCK_id'), 'STOCK', ['id'], unique=False)

    # 17. stock_x_movimientos
    op.create_table('STOCK_X_MOVIMIENTOS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('id_mov_compra', sa.Integer(), nullable=False),
        sa.Column('id_stock', sa.Integer(), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column('costo_unitario', sa.DECIMAL(10, 2), nullable=False),
        sa.ForeignKeyConstraint(['id_mov_compra'], ['MOVIMIENTOS_COMPRA.id'], ),
        sa.ForeignKeyConstraint(['id_stock'], ['STOCK.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_STOCK_X_MOVIMIENTOS_id'), 'STOCK_X_MOVIMIENTOS', ['id'], unique=False)

    # 18. stock_x_proveedores
    op.create_table('STOCK_X_PROVEEDORES',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('id_proveedor', sa.Integer(), nullable=False),
        sa.Column('id_stock', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_proveedor'], ['PROVEEDORES.id'], ),
        sa.ForeignKeyConstraint(['id_stock'], ['STOCK.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_STOCK_X_PROVEEDORES_id'), 'STOCK_X_PROVEEDORES', ['id'], unique=False)

    # 19. producto_composicion
    op.create_table('PRODUCTO_COMPOSICION',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('id_producto', sa.Integer(), nullable=False),
        sa.Column('id_stock', sa.Integer(), nullable=False),
        sa.Column('cantidad_usada', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['id_producto'], ['PRODUCTOS.id'], ),
        sa.ForeignKeyConstraint(['id_stock'], ['STOCK.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_PRODUCTO_COMPOSICION_id'), 'PRODUCTO_COMPOSICION', ['id'], unique=False)

    # 20. puntos
    op.create_table('PUNTOS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('usuario_cli_id', sa.Integer(), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['usuario_cli_id'], ['USUARIOS_CLI.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_PUNTOS_id'), 'PUNTOS', ['id'], unique=False)

    # 21. medios_pago_x_movimientos
    op.create_table('MEDIOS_PAGO_X_MOVIMIENTOS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('id_movimiento', sa.Integer(), nullable=False),
        sa.Column('id_medio_pago', sa.Integer(), nullable=False),
        sa.Column('monto', sa.DECIMAL(10, 2), nullable=False),
        sa.ForeignKeyConstraint(['id_medio_pago'], ['MEDIOS_PAGO.id'], ),
        sa.ForeignKeyConstraint(['id_movimiento'], ['MOVIMIENTOS.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_MEDIOS_PAGO_X_MOVIMIENTOS_id'), 'MEDIOS_PAGO_X_MOVIMIENTOS', ['id'], unique=False)

    # 22. productos_x_movimientos
    op.create_table('PRODUCTOS_X_MOVIMIENTOS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, unique=True),
        sa.Column('id_movimiento_venta', sa.Integer(), nullable=False),
        sa.Column('id_producto', sa.Integer(), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column('precio', sa.DECIMAL(10, 2), nullable=False),
        sa.ForeignKeyConstraint(['id_movimiento_venta'], ['MOVIMIENTOS_VENTAS.id'], ),
        sa.ForeignKeyConstraint(['id_producto'], ['PRODUCTOS.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_PRODUCTOS_X_MOVIMIENTOS_id'), 'PRODUCTOS_X_MOVIMIENTOS', ['id'], unique=False)

    # Seed: ROLES_ADM
    roles_adm_table = sa.table('ROLES_ADM',
        sa.column('id', sa.Integer),
        sa.column('rol', sa.String)
    )
    op.bulk_insert(roles_adm_table, [
        {'id': 0, 'rol': 'DEV'},
        {'id': 1, 'rol': 'ADMIN'},
        {'id': 2, 'rol': 'CAJERO'}
    ])

    # Seed: ROLES_CLI
    roles_cli_table = sa.table('ROLES_CLI',
        sa.column('id', sa.Integer),
        sa.column('rol', sa.String)
    )
    op.bulk_insert(roles_cli_table, [
        {'id': 1, 'rol': 'CLIENTE'}
    ])

    # Seed: TIPOS_MOVIMIENTOS
    tipos_table = sa.table('TIPOS_MOVIMIENTOS',
        sa.column('id', sa.Integer),
        sa.column('tipo', sa.String)
    )
    op.bulk_insert(tipos_table, [
        {'id': 1, 'tipo': 'VENTA'},
        {'id': 2, 'tipo': 'COMPRA'},
        {'id': 3, 'tipo': 'GASTO'}
    ])

    # Seed: MEDIOS_PAGO
    medios_pago_table = sa.table('MEDIOS_PAGO',
        sa.column('id', sa.Integer),
        sa.column('medio_pago', sa.String)
    )
    op.bulk_insert(medios_pago_table, [
        {'id': 1, 'medio_pago': 'EFECTIVO'},
        {'id': 2, 'medio_pago': 'MERCADO_PAGO'},
        {'id': 3, 'medio_pago': 'TARJETA_DEBITO'},
        {'id': 4, 'medio_pago': 'TARJETA_CREDITO'}
    ])


def downgrade() -> None:
    # Limpieza de tablas legacy del esquema previo si existen
    op.execute('DROP TABLE IF EXISTS "MOVIMIENTOS_CAJA" CASCADE')
    op.execute('DROP TABLE IF EXISTS "ROLES" CASCADE')

    op.drop_index(op.f('ix_PRODUCTOS_X_MOVIMIENTOS_id'), table_name='PRODUCTOS_X_MOVIMIENTOS', if_exists=True)
    op.drop_table('PRODUCTOS_X_MOVIMIENTOS', if_exists=True)
    op.drop_index(op.f('ix_MEDIOS_PAGO_X_MOVIMIENTOS_id'), table_name='MEDIOS_PAGO_X_MOVIMIENTOS', if_exists=True)
    op.drop_table('MEDIOS_PAGO_X_MOVIMIENTOS', if_exists=True)
    op.drop_index(op.f('ix_PUNTOS_id'), table_name='PUNTOS', if_exists=True)
    op.drop_table('PUNTOS', if_exists=True)
    op.drop_index(op.f('ix_PRODUCTO_COMPOSICION_id'), table_name='PRODUCTO_COMPOSICION', if_exists=True)
    op.drop_table('PRODUCTO_COMPOSICION', if_exists=True)
    op.drop_index(op.f('ix_STOCK_X_PROVEEDORES_id'), table_name='STOCK_X_PROVEEDORES', if_exists=True)
    op.drop_table('STOCK_X_PROVEEDORES', if_exists=True)
    op.drop_index(op.f('ix_STOCK_X_MOVIMIENTOS_id'), table_name='STOCK_X_MOVIMIENTOS', if_exists=True)
    op.drop_table('STOCK_X_MOVIMIENTOS', if_exists=True)
    op.drop_index(op.f('ix_STOCK_id'), table_name='STOCK', if_exists=True)
    op.drop_table('STOCK', if_exists=True)
    op.drop_index(op.f('ix_MOVIMIENTOS_GASTO_id'), table_name='MOVIMIENTOS_GASTO', if_exists=True)
    op.drop_table('MOVIMIENTOS_GASTO', if_exists=True)
    op.drop_index(op.f('ix_MOVIMIENTOS_COMPRA_id'), table_name='MOVIMIENTOS_COMPRA', if_exists=True)
    op.drop_table('MOVIMIENTOS_COMPRA', if_exists=True)
    op.drop_index(op.f('ix_CUPONES_USUARIO_id'), table_name='CUPONES_USUARIO', if_exists=True)
    op.drop_table('CUPONES_USUARIO', if_exists=True)
    op.drop_index(op.f('ix_MOVIMIENTOS_VENTAS_id'), table_name='MOVIMIENTOS_VENTAS', if_exists=True)
    op.drop_table('MOVIMIENTOS_VENTAS', if_exists=True)
    op.drop_index(op.f('ix_MOVIMIENTOS_id'), table_name='MOVIMIENTOS', if_exists=True)
    op.drop_table('MOVIMIENTOS', if_exists=True)
    op.drop_index(op.f('ix_PROVEEDORES_id'), table_name='PROVEEDORES', if_exists=True)
    op.drop_table('PROVEEDORES', if_exists=True)
    op.drop_index(op.f('ix_PRODUCTOS_id'), table_name='PRODUCTOS', if_exists=True)
    op.drop_table('PRODUCTOS', if_exists=True)
    op.drop_index(op.f('ix_MEDIOS_PAGO_id'), table_name='MEDIOS_PAGO', if_exists=True)
    op.drop_table('MEDIOS_PAGO', if_exists=True)
    op.drop_index(op.f('ix_CUPONES_id'), table_name='CUPONES', if_exists=True)
    op.drop_table('CUPONES', if_exists=True)
    op.drop_index(op.f('ix_TURNOS_CAJA_id'), table_name='TURNOS_CAJA', if_exists=True)
    op.drop_table('TURNOS_CAJA', if_exists=True)
    op.drop_index(op.f('ix_USUARIOS_CLI_id'), table_name='USUARIOS_CLI', if_exists=True)
    op.drop_table('USUARIOS_CLI', if_exists=True)
    op.drop_index(op.f('ix_USUARIOS_ADM_id'), table_name='USUARIOS_ADM', if_exists=True)
    op.drop_table('USUARIOS_ADM', if_exists=True)
    op.drop_index(op.f('ix_TIPOS_MOVIMIENTOS_id'), table_name='TIPOS_MOVIMIENTOS', if_exists=True)
    op.drop_table('TIPOS_MOVIMIENTOS', if_exists=True)
    op.drop_index(op.f('ix_ROLES_CLI_id'), table_name='ROLES_CLI', if_exists=True)
    op.drop_table('ROLES_CLI', if_exists=True)
    op.drop_index(op.f('ix_ROLES_ADM_id'), table_name='ROLES_ADM', if_exists=True)
    op.drop_table('ROLES_ADM', if_exists=True)
