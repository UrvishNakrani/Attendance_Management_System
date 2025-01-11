from database.database import SessionLocal
from src.models.Role import Roll
from fastapi import APIRouter,HTTPException
from src.schemas.Role_Schemas import RoleSchema
import uuid
from src.models.user import User

Role = APIRouter()
db = SessionLocal()

@Role.post("/Roll")
def Get_roll(roles:RoleSchema):

    Make_Role = Roll(
        id = str(uuid.uuid4()),
        Role_id = roles.Role_id,
        Roll_Name = roles.Roll_Name
    )

    db.add(Make_Role)
    db.commit()
    db.refresh(Make_Role)

    return Make_Role

@Role.get("/Get_All_Role",response_model=list[RoleSchema])
def all():

    All_Role = db.query(Roll).all()

    if not All_Role:
        raise HTTPException(status_code=400,detail="Roles Are Not Find")
    
    return All_Role


@Role.get("/Get_No.of_Role/{id}",response_model=RoleSchema)
def all(id:str):

    Specific_Role = db.query(Roll).filter(Roll.id == id).first()

    if not Specific_Role:
        raise HTTPException(status_code=400,detail="Roles Are Not Find")
    
    return Specific_Role
