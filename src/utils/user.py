
from database.database import SessionLocal
from src.models.user import User
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from config import SENDER_EMAIL,EMAIL_PASS


db = SessionLocal()

def find_same_email(email:str):
    find_same_email = db.query(User).filter(User.email == email).first()

    if find_same_email:
        if find_same_email.is_active == True:
            raise HTTPException(status_code=400,default="User Email Id is Alredy Exist Try With Another Email Id")
        if find_same_email.is_active == False:
            raise HTTPException(status_code=400,details="User email are alredy exist but account are deleted try with another Emai")
        
def find_same_username(username:str):
  find_same_username = db.query(User).filter(User.username == username).first()

  if find_same_username:
    if find_same_username.is_active == True:
      raise HTTPException(status_code=400,detail="Username are alresy exist")
    if find_same_username.is_active == False:
      raise HTTPException(status_code=400,detail="Username are alredy exist but this account is deleted try with another Username ")
      


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def pass_checker(user_pass, hash_pass):
    if pwd_context.verify(user_pass, hash_pass):
        return True
    else:
        raise HTTPException(status_code=401, detail="Password is incorrect")



from config import SECRET_KEY,ALGORITHM
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status


def get_token(id:str,username:str,email:str):
    payload = {
        "id" : id,
        "username" : username,
        "email" : email,
        "exp" : datetime.now(timezone.utc) + timedelta(days=10),
    }


    access_token =  jwt.encode(payload,SECRET_KEY,ALGORITHM)

    return {"access_token":access_token}

def decode_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        id = payload.get("id")
        email = payload.get("email")
        username = payload.get("username")
        if not id or not username or not email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return id , username , email 
    
    except jwt.ExpiredSignatureError:
       
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
      
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )





import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import SENDER_EMAIL,EMAIL_PASS

def send_email(receiver, subject, body):

    # SMTP Configuration (for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = SENDER_EMAIL
    smtp_pass = EMAIL_PASS

    #build the mail system to send someone
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    #now try to send the mail to receiver 

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(SENDER_EMAIL,receiver, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
