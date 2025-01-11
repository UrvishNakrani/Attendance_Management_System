from fastapi import FastAPI
from src.routers.user import user
from src.routers.course_route import Course1
from src.routers.Student_En_Router import Enrolled
from src.routers.Attendance_Router import Attend
from src.routers.Rolll_Router import Role

app = FastAPI()

app.include_router(user)
app.include_router(Course1)
app.include_router(Enrolled)
app.include_router(Attend)
app.include_router(Role)


