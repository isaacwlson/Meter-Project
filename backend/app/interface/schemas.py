
# Import Pydantic's BaseModel and EmailStr for data validation
from pydantic import BaseModel, EmailStr

# Schema for creating a new account profile
# Used to validate incoming request data for account creation endpoints
class AccountProfileCreate(BaseModel):
    OAuthID: str         # OAuth identifier for the user (string)
    email: EmailStr      # User's email address (validated as a proper email)
    name: str            # User's name (string)