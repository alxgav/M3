import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker

# load_dotenv()
#
# DATABASE_URL = os.getenv('DATABASE_URL')
from app.settings import config

# Ensure the DATABASE_URL is set in the environment
DB = config.DATABASE_URL
if not  DB:
    raise RuntimeError("DATABASE_URL is not set in .env file")



engine: AsyncEngine = create_async_engine(DB, echo=True)
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

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