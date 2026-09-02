"""create auth schema and cuentas table

Revision ID: 20260901_auth
Revises: f59eb8292c7e
Create Date: 2026-09-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260901_auth'
down_revision = 'f59eb8292c7e'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Crear esquema auth si no existe
    op.execute("CREATE SCHEMA IF NOT EXISTS auth;")

    # 2. Crear tabla CUENTAS en el esquema auth
    op.create_table(
        'CUENTAS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('dni', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('tipo_usuario', sa.String(length=25), nullable=False),
        sa.Column('usuario_adm_id', sa.Integer(), nullable=True),
        sa.Column('usuario_cli_id', sa.Integer(), nullable=True),
        sa.Column('activo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('create_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['usuario_adm_id'], ['USUARIOS_ADM.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['usuario_cli_id'], ['USUARIOS_CLI.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema='auth'
    )
    op.create_index(op.f('ix_auth_CUENTAS_id'), 'CUENTAS', ['id'], unique=False, schema='auth')
    op.create_index(op.f('ix_auth_CUENTAS_dni'), 'CUENTAS', ['dni'], unique=True, schema='auth')
    op.create_index(op.f('ix_auth_CUENTAS_create_at'), 'CUENTAS', ['create_at'], unique=False, schema='auth')
    op.create_index(op.f('ix_auth_CUENTAS_update_at'), 'CUENTAS', ['update_at'], unique=False, schema='auth')

def downgrade() -> None:
    op.drop_index(op.f('ix_auth_CUENTAS_update_at'), table_name='CUENTAS', schema='auth')
    op.drop_index(op.f('ix_auth_CUENTAS_create_at'), table_name='CUENTAS', schema='auth')
    op.drop_index(op.f('ix_auth_CUENTAS_dni'), table_name='CUENTAS', schema='auth')
    op.drop_index(op.f('ix_auth_CUENTAS_id'), table_name='CUENTAS', schema='auth')
    op.drop_table('CUENTAS', schema='auth')
    op.execute("DROP SCHEMA IF EXISTS auth CASCADE;")
