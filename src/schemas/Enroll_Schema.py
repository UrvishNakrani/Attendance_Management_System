from pydantic import BaseModel
from datetime import datetime

class EnrollSchema(BaseModel):
    student_id: str
    course_id: str
    enrolled_at: datetime
   
