from dotenv import load_dotenv
from sqlalchemy import create_engine 
from sqlalchemy.orm import DeclarativeBase , sessionmaker
import os 
load_dotenv()


DATABASE_URL=os.getenv("DATABASE_URL")

# create engine to connect to database 
engine = create_engine(
    DATABASE_URL,
)


# create local session for each call
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine,
)

class Base(DeclarativeBase):
    pass


# funtion to get db and session local 
def get_db():
    db= SessionLocal()  #create local session 
    try: # try block to counter any error 
        yield db  #return the db 
    finally:
        db.close() # after the work is done close the connection 

