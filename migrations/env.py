import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from app.core.models import Base  # Ensure this path is correct

# Alembic config
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata correctly
target_metadata = Base.metadata

# Define async engine globally
async_engine = create_async_engine(
    "sqlite+aiosqlite:///app_db.db",
    poolclass=pool.NullPool,
)

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

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using async SQLAlchemy."""
    async with async_engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(sync_conn):
    """Helper function to configure and run migrations in a sync context."""
    context.configure(connection=sync_conn, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

# Handle sync/async properly
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())  # Ensure proper async execution
