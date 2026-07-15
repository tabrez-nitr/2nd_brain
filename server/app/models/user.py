from app.db.database import Base
from sqlalchemy import Column , String , Integer , DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer , primary_key = True , index = True)
    name = Column(String)
    email = Column(String , index = True , unique = True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True),
                         server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
        server_default=func.now())

    workspaces = relationship(
        "WorkSpaceModel",
        back_populates="owner",
        cascade="all, delete-orphan",  # this helps to get access of all the children suppose user delete his id than all the workspaces will be deleted  
    )