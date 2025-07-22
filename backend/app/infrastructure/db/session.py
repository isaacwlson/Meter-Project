
# Import necessary SQLAlchemy async components
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an async SQLAlchemy engine using the database URL
# echo=True enables SQL logging for debugging
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker factory for async sessions
# - bind: the engine to use
# - class_: use AsyncSession for async DB operations
# - expire_on_commit: keeps objects 'live' after commit
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency function to provide a database session
# Used with FastAPI's Depends to inject a session into endpoints
async def get_db() -> AsyncSession:
    """
    Yields an async database session for use in endpoints.
    Ensures the session is closed after use.
    """
    async with SessionLocal() as session:
        yield session