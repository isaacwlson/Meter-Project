from pydantic import BaseModel, EmailStr

class AccountProfileCreate(BaseModel):
    OAuthID: str
    email: EmailStr
    name: str