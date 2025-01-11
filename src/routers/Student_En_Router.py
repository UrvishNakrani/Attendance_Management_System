from database.database import SessionLocal
from fastapi import APIRouter,HTTPException
import uuid
from src.schemas.Enroll_Schema import EnrollSchema
from src.models.Student_Course_En import Student_Course_En

Enrolled = APIRouter()
db = SessionLocal()

@Enrolled.post("/Enroll")
def enroll(enroll:EnrollSchema):

    enroll_course = Student_Course_En(
        id = str(uuid.uuid4()),
        student_id = enroll.student_id,
        course_id = enroll.course_id
    )

    db.add(enroll_course)
    db.commit()
    db.refresh(enroll_course)


    return {"Course Enrolled Successfully": enroll_course}

@Enrolled.get("/Get_Enrolled_Student",response_model=list[EnrollSchema])
def Enrolle_All_Student():

    Get_Enroll = db.query(Student_Course_En).all()

    if not Get_Enroll:
        raise HTTPException(status_code=400,detail="Student Enroll Course Not Found")

    return Get_Enroll
        
@Enrolled.get("/Get_Enrolled_Student_Specific/{id}",response_model=EnrollSchema)
def get_data(id:str):
    
    Get_Enroll = db.query(Student_Course_En).filter(Student_Course_En.id == id).first()

    if not Get_Enroll:
        raise HTTPException(status_code=400,detail="Student_Course_En Not Found")
    return Get_Enroll

@Enrolled.delete("/Delete_Student_Enroll/{id}")
def Delete_Student_En(id:str):

    Delete_data = db.query(Student_Course_En).filter(Student_Course_En.id == id).first()

    if not Delete_data:
        raise HTTPException(status_code=400,detail="Student_Enroll_id Not Found")

    db.delete(Delete_data)
    db.refresh()
    
    return Delete_data