from fastapi import Depends , HTTPException , status , Cookie
from sqlalchemy.orm import Session 
from app.db.database import get_db
from app.models.user import UserModel
from app.core.security import decode_token
from jose import JWTError

"""This Dependecy helps to get the user from cookie """

def get_current_user(access_token : str = Cookie(default=None) , db : Session = Depends(get_db)):
    print(access_token)
    # if cookie doesnot exists 
    if not access_token:
      raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "You are not authorized to perform this action"
      )
    
    try:
        payload = decode_token(access_token)
        # get the payload 
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    #get all information about the user 
    #cookie only has user_id as payload 
    user_info = (
        db.query(UserModel).filter(UserModel.id == payload["user_id"]).first()
    )
    
    if not user_info:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "You are not authorized to perform this action"
        )
    
    # return the user info from this Dependecy
    return user_info
    
