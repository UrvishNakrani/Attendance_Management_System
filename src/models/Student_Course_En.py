from sqlalchemy import String,ForeignKey,Column,DateTime
from database.database import Base
from datetime import datetime
from src.models.user import User
from src.models.course import Course


class Student_Course_En(Base):

    __tablename__ = "student_course_enrollments"

    id = Column(String(100),primary_key=True,nullable=False)

    student_id = Column(String(100),ForeignKey(User.id),nullable=False)

    course_id = Column(String(100),ForeignKey(Course.id),nullable=False)
    
    enrolled_at = Column(DateTime,default=datetime.now,nullable=False)