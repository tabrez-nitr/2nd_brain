from app.db.database import Base
from sqlalchemy import Column , String , Integer , Date

class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer , primary_key = True , index = True)
    name = Column(String)
    email = Column(String , index = True , unique = True)
    hashed_password = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)