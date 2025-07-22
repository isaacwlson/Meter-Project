
# Import SQLAlchemy column types and base class
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.infrastructure.db.base import Base

# Model for user account profiles
class AccountProfile(Base):
    __tablename__ = "AccountProfile"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique user ID (primary key)
    OAuthID = Column(String, unique=True, index=True)   # OAuth identifier, must be unique
    email = Column(String, unique=True, index=True)     # User's email, must be unique
    name = Column(String, index=True)                   # User's name

# Model for meters (e.g., devices/resources linked to users)
class MeterTable(Base):
    __tablename__ = "MeterTable"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique meter ID (primary key)
    OAuthID = Column(String, ForeignKey("AccountProfile.OAuthID"), index=True)  # Link to AccountProfile via OAuthID
    metername = Column(String, index=True)              # Name of the meter
    URL = Column(String, index=True)                    # Associated URL for the meter
    GUID = Column(String, index=True)                   # Globally unique identifier for the meter
    datetime = Column(DateTime, index=True)             # Timestamp for the meter (e.g., creation or update time)

# Model for votes on meters
class VoteTable(Base):
    __tablename__ = "VoteTable"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique vote ID (primary key)
    meterID = Column(Integer, ForeignKey("MeterTable.id"), index=True)  # Link to MeterTable via meter ID
    Vote = Column(Integer, index=True)                  # Vote value (e.g., upvote/downvote)
    datetime = Column(DateTime, index=True)             # Timestamp for when the vote was cast
