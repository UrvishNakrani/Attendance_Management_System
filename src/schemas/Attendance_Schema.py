from pydantic import BaseModel
from datetime import datetime

class AttendanceSchema(BaseModel):
    date : datetime
    status : bool

    