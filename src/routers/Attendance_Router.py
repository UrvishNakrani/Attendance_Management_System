from fastapi import APIRouter,HTTPException
from database.database import SessionLocal
from src.models.Attendance import Attendance1
from src.schemas.Attendance_Schema import AttendanceSchema
import uuid

Attend = APIRouter()
db = SessionLocal()

@Attend.post("/Manage_Attendance")
def Attendance(attendnce:AttendanceSchema):

    Let_Attendance = Attendance1(
        id = str(uuid.uuid4()),
        Student_id =  str(uuid.uuid4()),
        Course_id =  str(uuid.uuid4()),
        date = attendnce.date,
        status = attendnce.status
    )

    db.add(Let_Attendance)
    db.commit()
    db.refresh(Let_Attendance)

    return{"Your Attandance Is Complate": Let_Attendance}
  

@Attend.get("/Get_Attendance_All_Student",response_model=list[AttendanceSchema])
def Get_All_St_Attend():
    
    Attendance = db.query(Attendance1).all()

    if not Attendance:
        raise HTTPException(status_code=400,detail="Studant is Absent")
    

    return Attendance

@Attend.get("/Get_Attendance/{id}",response_model=AttendanceSchema)
def Get(id:str):

    Specific_Student = db.query(Attendance1).filter(Attendance1.id == id).first()

    if not Specific_Student:
        raise HTTPException(status_code=400,detail="Student is not present")
    
    return Specific_Student


