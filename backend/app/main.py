from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager

from app.infrastructure.db.session import engine, SessionLocal
from app.infrastructure.db.base import Base
from app.infrastructure.models.models import AccountProfile, MeterTable, VoteTable
from app.interface.schemas import AccountProfileCreate


#The lifespan event handler in FastAPI (and Starlette) is a way to manage application startup and shutdown events. 
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")

#TEST: to get comfortable with using fastapi and copilot
def read_root():
    return {"message": "Hello world This is a test for the FastAPI application. I am also using copilot to write this code."}


# Dependency for DB session
async def get_db():
    async with SessionLocal() as session:
        yield session


@app.post("/accounts/", response_model=dict)
async def add_account(
    account: AccountProfileCreate, db: AsyncSession = Depends(get_db)
):
    new_account = AccountProfile(
        OAuthID=account.OAuthID, email=account.email, name=account.name
    )
    db.add(new_account)
    try:
        await db.commit()
        await db.refresh(new_account)
    except Exception as e:
        await db.rollback()
        print("Account creation error:", e)
        raise HTTPException(status_code=400, detail="Account creation failed")
    return {"id": new_account.id, "email": new_account.email}

@app.delete("/accounts/{account_id}", response_model=dict)
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AccountProfile).where(AccountProfile.id == account_id))
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    await db.delete(account)
    await db.commit()
    return {"detail": "Account deleted"}
