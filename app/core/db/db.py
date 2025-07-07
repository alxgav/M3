from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from dotenv import load_dotenv
import os
from app.settings import logger as log

load_dotenv()

# Read individual PostgreSQL connection parameters
PGHOST = os.getenv("PGHOST", "localhost")
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGPORT = os.getenv("PGPORT", "5432")
PGSSLMODE = os.getenv("PGSSLMODE", "require")
PGCHANNELBINDING = os.getenv("PGCHANNELBINDING", "require")

# Validate required parameters
if not all([PGDATABASE, PGUSER, PGPASSWORD]):
    raise ValueError(log.error("Missing required PostgreSQL connection parameters in .env file"))

# Construct the connection URL with SSL parameters
DATABASE_URL = (
    f"postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
    f"?sslmode={PGSSLMODE}"
    f"&sslrootcert={os.getenv('PGSSLROOTCERT', '')}"
    f"&sslcert={os.getenv('PGSSLCERT', '')}"
    f"&sslkey={os.getenv('PGSSLKEY', '')}"
    f"&channel_binding={PGCHANNELBINDING}"
)

# Create async engine with connection pool settings
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

# Create a session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base class with automatic table name generation
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False
    )

    @classmethod
    def __tablename__(cls) -> str:
        """Automatically generate table name from class name."""
        name = cls.__name__
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')

# Dependency to get an async session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
# from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, Mapped
# from sqlalchemy.dialects.postgresql import UUID
# from uuid import uuid4
# from dotenv import load_dotenv
# import re
# import os
# from app.settings import logger as log
#
# load_dotenv()
#
# DATABASE_URL = os.getenv("DATABASE_URL")
# if not DATABASE_URL:
#     raise ValueError(log.error("DATABASE_URL not found in .env file"))
#
# # Create an async engine
# # engine = create_async_engine(DATABASE_URL, echo=True)
# engine = create_async_engine(re.sub(r'^postgresql:', 'postgresql+asyncpg:', DATABASE_URL), echo=True)
#
#
#
# # Create a session factory
# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )
#
# # Base class with automatic table name generation
# class Base(AsyncAttrs, DeclarativeBase):
#     __abstract__ = True
#
#     id: Mapped[UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid4,  # Use uuid4 directly
#         nullable=False
#     )
#
#     @classmethod
#     def __tablename__(cls) -> str:
#         """Automatically generate table name from class name."""
#         name = cls.__name__
#         snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
#         return snake_case
#
# # Dependency to get an async session
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session