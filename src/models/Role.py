from database.database import Base
from sqlalchemy import Column,String,ForeignKey
from src.models.user import User

class Roll(Base):
    __tablename__ = "roles"

    id = Column(String(100),primary_key=True,nullable=False)
    Role_id = Column(String(100),ForeignKey(User.id),nullable=False)
    Roll_Name = Column(String(100),nullable=False)