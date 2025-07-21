from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.infrastructure.db.base import Base

class AccountProfile(Base):
    __tablename__ = "AccountProfile"

    id = Column(Integer, primary_key=True, index=True)
    OAuthID = Column(String, unique= True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)

class MeterTable(Base):
    __tablename__ = "MeterTable"

    id = Column(Integer, primary_key=True, index=True)
    OAuthID = Column(String, ForeignKey("AccountProfile.OAuthID"), index=True)
    metername = Column(String, index=True)
    URL = Column(String, index=True)
    GUID = Column(String, index=True)
    datetime = Column(DateTime, index=True)

class VoteTable(Base):
    __tablename__ = "VoteTable"

    id = Column(Integer, primary_key=True, index=True)
    meterID = Column(Integer, ForeignKey("MeterTable.id"), index=True)
    Vote = Column(Integer, index=True)
    datetime = Column(DateTime, index=True)
