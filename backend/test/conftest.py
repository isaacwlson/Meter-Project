
# Import pytest and pytest-asyncio for async test support
import pytest_asyncio
import pytest
# Import AsyncClient and ASGITransport for HTTPX-based FastAPI testing
from httpx import AsyncClient, ASGITransport
# Import SQLAlchemy async engine/session for test DB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
# Import FastAPI app and DB dependencies
from app.main import app
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import get_db


# Use a PostgreSQL test database for integration tests
TEST_DATABASE_URL = "postgresql+asyncpg://sheepdog:sheepdogs123@db:5432/MeterDB"

# Create a separate async engine and sessionmaker for the test DB
engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

# Override the get_db dependency to use the test DB session
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

# Apply the override so all FastAPI endpoints use the test DB during tests
app.dependency_overrides[get_db] = override_get_db


# Automatically create and destroy the test DB schema for each test module
# Use @pytest_asyncio.fixture for async compatibility
@pytest_asyncio.fixture(scope="module", autouse=True)
async def create_test_db():
    # Create all tables at the start of the test module
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop/dispose the test DB after tests complete
    await engine_test.dispose()

# Provide an async HTTP client for making requests to the FastAPI app
# Depends on the test DB being set up first
@pytest_asyncio.fixture
async def async_client(create_test_db):
    # Use ASGITransport to run requests in-process against the app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac