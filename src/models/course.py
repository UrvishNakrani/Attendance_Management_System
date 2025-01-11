from database.database import Base
from sqlalchemy import String,ForeignKey,Column,DateTime
from datetime import datetime
from src.models.user import User

class Course(Base):
    __tablename__ = "courses"
    id = Column(String(100),primary_key=True,nullable=False)
    name = Column(String(100),nullable=False)
    teacher_id = Column(String(100),ForeignKey(User.id),nullable=False)
    created_at = Column(DateTime,default=datetime.now,nullable=False)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now,nullable=False)
    
