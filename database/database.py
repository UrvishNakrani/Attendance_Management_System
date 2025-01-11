from config import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
