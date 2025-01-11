
from fastapi import APIRouter,HTTPException
from database.database import SessionLocal
from src.schemas.course_schema import CourseBase
from src.models.course import Course
import uuid


Course1 = APIRouter()
db = SessionLocal()

@Course1.post("/Make_Course")
def Create_Course(course:CourseBase):

    Make_Course = Course(
        id = str(uuid.uuid4()),
        name = course.name,
        teacher_id = course.teacher_id
    )

    db.add(Make_Course)
    db.commit()
    db.refresh(Make_Course)


    return {"Course Created Successfully": Make_Course}


@Course1.get("/Retrives_all_Course",response_model=list[CourseBase])
def get_all_Course():
    Get_all = db.query(Course).all()

    if not Get_all:
        raise HTTPException(status=400,detail="Course Not Found")
    return Get_all


@Course1.get("/Get_Specific_Course/{id}",response_model=CourseBase)
def get(id:str):

    get_course = db.query(Course).filter(Course.id == id).first()

    if not get_course:
        raise HTTPException(status_code=400,detail="Course Not Found")
    return get_course


@Course1.put("/Update_Course/{id}",response_model=CourseBase)
def update_user(id:str,course: CourseBase):
    find_Course = db.query(Course).filter(Course.id == id).first()
    if not find_Course:
        raise HTTPException(status_code=404,detail="Course id not found")
    find_Course.name = course.name
    find_Course.teacher_id = course.teacher_id
  
    db.commit()
    return find_Course


@Course1.delete("/Delete_Course/{id}")
def delete_course(id:str):
    find_Course = db.query(Course).filter(Course.id == id).first()
    if not find_Course:
        raise HTTPException(status_code=404,detail="Course id not found")
    db.delete(find_Course)
    db.commit()
    return {"Course Deleted Successfully": find_Course}
