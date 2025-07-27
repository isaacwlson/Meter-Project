
# Import FastAPI and dependencies for building the API and handling requests
from fastapi import FastAPI, Depends, HTTPException


# Import async session and select for database operations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Import asynccontextmanager for managing app lifespan events
from contextlib import asynccontextmanager

# Import database engine, session, and models
from app.infrastructure.db.session import engine, SessionLocal
from app.infrastructure.db.base import Base
from app.infrastructure.models.models import AccountProfile, MeterTable, VoteTable
# Import Pydantic schema for account creation
from app.interface.schemas import AccountProfileCreate

# Lifespan event handler: runs code at startup and shutdown
# Here, it creates all database tables at app startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# Create FastAPI app instance, using the lifespan handler
app = FastAPI(lifespan=lifespan)

# Root endpoint for testing the API
@app.get("/")
def read_root():
    """
    Simple test endpoint to verify the API is running.
    Returns a welcome message.
    """
    return {"message": "Hello world This is a test for the FastAPI application. I am also using copilot to write this code."}

# Dependency to provide a database session to endpoints
async def get_db():
    """
    Yields an async database session for use in endpoints.
    Ensures session is closed after use.
    """
    async with SessionLocal() as session:
        yield session

# Endpoint to add a new account to the database
@app.post("/accounts/", response_model=dict)
async def add_account(
    account: AccountProfileCreate, db: AsyncSession = Depends(get_db)
):
    """
    Creates a new account using the provided data.
    Returns the new account's ID and email on success.
    Raises HTTP 400 if creation fails (e.g., duplicate email).
    """
    new_account = AccountProfile(
        OAuthID=account.OAuthID, email=account.email, name=account.name
    )
    db.add(new_account)
    try:
        await db.commit()
        await db.refresh(new_account)
    except Exception as e:
        await db.rollback()
        print("Account creation error:", e)  # Print error for debugging
        raise HTTPException(status_code=400, detail="Account creation failed")
    return {"id": new_account.id, "email": new_account.email}

# Endpoint to delete an account by ID
@app.delete("/accounts/{account_id}", response_model=dict)
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deletes the account with the given ID.
    Returns a confirmation message on success.
    Raises HTTP 404 if the account does not exist.
    """
    result = await db.execute(select(AccountProfile).where(AccountProfile.id == account_id))
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    await db.delete(account)
    await db.commit()
    return {"detail": "Account deleted"}


# Endpoint to list all accounts in the database
@app.get("/accounts/", response_model=list)
async def list_accounts(db: AsyncSession = Depends(get_db)):
    """
    Returns a list of all account profiles in the database.
    Each account is represented as a dictionary with id, OAuthID, email, and name.
    """
    result = await db.execute(select(AccountProfile))
    accounts = result.scalars().all()
    return [{"id": acc.id, "OAuthID": acc.OAuthID, "email": acc.email, "name": acc.name} for acc in accounts]


# Endpoint to get details for a specific account by ID
@app.get("/accounts/{account_id}", response_model=dict)
async def get_account(account_id: int, db: AsyncSession = Depends(get_db)):
    """
    Returns account details for the given account ID.
    If the account does not exist, returns HTTP 404.
    """
    result = await db.execute(select(AccountProfile).where(AccountProfile.id == account_id))
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"id": account.id, "OAuthID": account.OAuthID, "email": account.email, "name": account.name}


# Endpoint for health check to verify the API is running
@app.get("/health")
def health_check():
    """
    Simple health check endpoint.
    Returns status 'ok' if the API is up.
    """
    return {"status": "ok"}