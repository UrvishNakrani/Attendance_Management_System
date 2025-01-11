from sqlalchemy import Column, String, DateTime,ForeignKey,Boolean
from database.database import Base
from datetime import datetime
from src.models.user import User
from src.models.course import Course


class Attendance1(Base):
    __tablename__ = "attendance"

    id = Column(String(100),primary_key=True,nullable=False)
    Student_id = Column(String(100),ForeignKey(User.id),nullable=False)
    Course_id = Column(String(100),ForeignKey(Course.id),nullable=False)
    date = Column(DateTime,default=datetime.now,nullable=False)
    status = Column(Boolean,nullable=False)