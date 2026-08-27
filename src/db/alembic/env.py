from logging.config import fileConfig
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import engine_from_config, pool, text
from alembic import context
from src.core.config import settings
from src.db.models import Base

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

db_url = settings.DATABASE_URL or ""
config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def drop_procedures(connection):
    """
    Elimina todos los stored procedures y funciones existentes (que comiencen con sp_ o trg_) antes de cargarlos.
    Esto evita conflictos y asegura que siempre se use la versión más reciente.
    """
    try:
        print("\n" + "=" * 80)
        print("🗑️  Eliminando stored procedures y funciones existentes...")
        
        # Obtener funciones y procedimientos con sus argumentos completos
        result = connection.execute(
            text("""
                SELECT 
                    n.nspname as schema_name,
                    p.proname as function_name,
                    pg_get_function_identity_arguments(p.oid) as args,
                    p.prokind
                FROM pg_proc p
                JOIN pg_namespace n ON p.pronamespace = n.oid
                WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
                AND (p.proname ILIKE 'sp_%' OR p.proname ILIKE 'trg_%')
                AND p.prokind IN ('f', 'p')
            """)
        ).fetchall()
        
        if not result:
            print("✓ No hay stored procedures/funciones para eliminar")
            print("=" * 80 + "\n")
            return
        
        iterator = tqdm(result, desc="Eliminando funciones", unit="función") if HAS_TQDM else result
        
        for rec in iterator:
            kind_str = "PROCEDURE" if rec.prokind == 'p' else "FUNCTION"
            drop_query = f'DROP {kind_str} IF EXISTS "{rec.schema_name}"."{rec.function_name}"({rec.args}) CASCADE'
            connection.execute(text(drop_query))
            if not HAS_TQDM:
                print(f"  ✓ Eliminada: {rec.function_name}({rec.args})")
        
        print("✅ Todas las funciones/procedimientos han sido eliminados correctamente")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"❌ Error eliminando funciones: {e}")
        raise


def load_stored_procedures(connection):
    """
    Carga todos los archivos .sql de stored procedures y triggers desde src/
    Se ejecuta automáticamente después de las migraciones de Alembic.
    """
    try:
        # Verificar si existen tablas de usuario en el esquema (evita crear triggers si fue un downgrade a base)
        from sqlalchemy import inspect
        inspector = inspect(connection)
        tables = [t for t in inspector.get_table_names() if t != "alembic_version"]
        if not tables:
            print("\n" + "=" * 80)
            print("ℹ️  No hay tablas de usuario en la base de datos (downgrade completado). Se omite la carga de procedimientos/triggers.")
            print("=" * 80 + "\n")
            return

        src_dir = Path(__file__).parent.parent.parent
        db_dir = src_dir / "db"
        target_dirs = [db_dir / "procedures", db_dir / "triggers"]
        
        print("\n" + "=" * 80)
        print("📂 Cargando stored procedures y triggers...")
        
        sql_files = []
        for target_dir in target_dirs:
            if target_dir.exists():
                sql_files.extend(sorted(target_dir.rglob("*.sql")))
        
        if not sql_files:
            print("⚠️  No se encontraron archivos SQL en procedures/ o triggers/ para ejecutar")
            print("=" * 80 + "\n")
            return
        
        print(f"📊 Encontrados {len(sql_files)} archivos SQL\n")
        
        iterator = (
            tqdm(enumerate(sql_files, 1), total=len(sql_files), desc="Cargando funciones", unit="archivo")
            if HAS_TQDM
            else enumerate(sql_files, 1)
        )
        
        for idx, sql_file in iterator:
            if not HAS_TQDM:
                print(f"[{idx}/{len(sql_files)}] Ejecutando: {sql_file.relative_to(src_dir)}")
            
            try:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                if not sql_content.strip():
                    print(f"⚠️  Archivo vacío: {sql_file.name}, se omite.")
                    continue
                
                connection.execute(text(sql_content))
                
                if not HAS_TQDM:
                    print(f"  ✓ {sql_file.name} ejecutado correctamente")
                
            except Exception as e:
                print(f"\n❌ Error ejecutando {sql_file.name}: {e}")
                raise
        
        print("\n✅ Se cargaron todos los stored procedures y triggers correctamente")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error cargando stored procedures: {e}")
        raise


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
            # Ejecutar eliminación y carga de stored procedures/triggers tras aplicar la migración
            drop_procedures(connection)
            load_stored_procedures(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
