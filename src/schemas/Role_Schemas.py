from pydantic import BaseModel

class RoleSchema(BaseModel):
    Roll_Name : str
    Role_id :str