from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class RegistreUserSchema(BaseModel):
    username : str
    email : EmailStr
    password : str 
   
class GetAllUserSchema(BaseModel):
    id: str
    username: str
    email:str
   
class UpdateUserSchema(BaseModel):
    username : Optional[str] = None
    email : Optional[EmailStr] = None
    password : Optional[str] = None


