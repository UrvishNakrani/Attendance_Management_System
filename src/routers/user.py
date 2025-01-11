from fastapi import APIRouter,HTTPException
from database.database import SessionLocal
from src.models.user import User,OTP
from src.schemas.user import RegistreUserSchema,GetAllUserSchema,UpdateUserSchema
import uuid,random
from src.utils.user import pwd_context,find_same_email,find_same_username,send_email,pass_checker,get_token
from logs.log_config import logger



user = APIRouter()
db = SessionLocal()

    
@user.post("/Registration_User")
def registre_user(user:RegistreUserSchema):

    logger.info("Getting all the users")

    new_user = User(
        id = str(uuid.uuid4()),
        username = user.username,
        email = user.email,
        password = pwd_context.hash(user.password)
        )


    find_minimum_one_entry = db.query(User).first()
    if find_minimum_one_entry:
        find_same_email(user.email)
        find_same_username(user.username)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    logger.success("Users retrieved successfully")
    return "User Register Successfully now go for the verification"



@user.get("/Get_User_Profile/{user_id}",response_model=GetAllUserSchema)
def get_single_user_profile(user_id:str):

    single_user = db.query(User).filter(User.id == user_id).first()
    
    if not single_user:
        raise HTTPException(status_code=400,detail="User Not Found")
    return single_user

@user.patch("/update_user/{user_id}")
def update_user(user_id:str,user:UpdateUserSchema):

    update_user_with_condition = db.query(User).filter(User.id == user_id,User.is_active == True,User.is_verified == True,User.is_delete == False).first()
    if not update_user_with_condition:
        raise HTTPException(status_code=400,detail="User did not found")

    new_userschema_without_none = user.model_dump(exclude_none=True)

    for key,value in new_userschema_without_none.items():
        if key == "password":
            setattr(update_user_with_condition,pwd_context.hash(value))
        else:
            find_same_email(value)
            find_same_username(value)
            setattr(update_user_with_condition,key,value)

    db.commit()
    db.refresh(update_user_with_condition)

    return {"Message":"User Updated Succesfully","Data":update_user_with_condition} 



@user.put("/update_user/{id}", response_model=UpdateUserSchema)
def update_user(id: str, user: UpdateUserSchema):
    find_user = db.query(User).filter(User.id == id,User.is_active == True,User.is_verified == True,User.is_delete == False).first()
    if not find_user:
        raise HTTPException(status_code=404, detail="user id not found")
    find_user.username = user.username
    find_user.email = user.email
    find_user.password = pwd_context.hash(user.password)
    db.commit()
    return find_user


@user.get("/Get_All_User_Profile",response_model=list[GetAllUserSchema])
def get_all_user():

    all_user_with_condition = db.query(User).all()

    if not all_user_with_condition:
        raise HTTPException(status_code=400,detail="User is not found")
    return all_user_with_condition

@user.delete("/delete_user/{id}",response_model=GetAllUserSchema)
def delete_user(id:str):
    
    find_user = db.query(User).filter(User.id == id,User.is_active == True,User.is_verified == True).first()

    if not find_user:
        raise HTTPException(status_code=400, detail="User not found")

    if find_user.is_delete == True:
        raise HTTPException(status_code=400, detail="User already deleted")
    

    find_user.is_delete = True
    find_user.is_active = False
    find_user.is_verified = False

    db.delete(find_user)
    db.commit()
    db.refresh(find_user)
    
    return {"message":"user deleted successfully","data":find_user}


@user.post("/generate_otp")
def generate_otp(email:str):
    find_user_with_email = db.query(User).filter(User.email == email,User.is_active == True,User.is_verified == False , User.is_delete == False).first()

    if not find_user_with_email:
        raise HTTPException(status_code=400, detail="User not found")
    
    random_otp = random.randint(1000,9999)
    print("---------------------------------------")
    print(random_otp)
    print("---------------------------------------")

    new_otp = OTP(
        id = str(uuid.uuid4()),
        user_id = find_user_with_email.id,
        email = find_user_with_email.email,
        otp = random_otp
    )

    send_email(find_user_with_email.email, "Test Email", f"Otp is {random_otp}")

    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return "OTP generated successfully"



@user.get("/verify_otp")
def verify_otp(email:str, otp:str):
    find_user_with_email = db.query(User).filter(User.email == email, User.is_active == True, User.is_verified == False, User.is_delete == False).first()

    # if not find_user_with_email:
    #     raise HTTPException(status_code=400, detail="User not found")

    find_otp = db.query(OTP).filter(OTP.email == email, OTP.otp == otp).first()

    if not find_otp:
        raise HTTPException(status_code=400, detail="OTP not found")

    find_user_with_email.is_verified = True
    db.delete(find_otp)
    db.commit()
    db.refresh(find_user_with_email)

    return "OTP verified successfully"



@user.get("/login_user")
def login_user(email:str, password:str):
    find_user_with_email = db.query(User).filter(User.email == email, User.is_active == True, User.is_verified == True, User.is_delete == False).first()

    if not find_user_with_email:
        raise HTTPException(status_code=400, detail="User not found")

    pass_checker(password, find_user_with_email.password)
      
    access_token = get_token(find_user_with_email.id, find_user_with_email.username, find_user_with_email.email)

    return access_token



