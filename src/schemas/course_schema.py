from pydantic import BaseModel
from datetime import datetime

class CourseBase(BaseModel):
    name : str
    teacher_id : str
            