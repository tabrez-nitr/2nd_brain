from fastapi import APIRouter , Depends , HTTPException , status, Response 
from app.schemas.user import UserSchema , LoginSchema 
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import hash_password , verify_password , create_token
from datetime import datetime , timedelta 
from app.services.auth import AuthService




router = APIRouter() # for the routes beloning to user 


# create obj of auth class 
auth_service = AuthService()


@router.post("/register", status_code = status.HTTP_201_CREATED)
def register_user(data : UserSchema , db : Session = Depends(get_db)):
    
    user = auth_service.register(data , db)
    return {
        "message" : "User Created Successfully",
        "user" : user 
    }




# login user 
@router.post("/login", status_code = status.HTTP_202_ACCEPTED)
def login_user(data : LoginSchema , response : Response , db : Session = Depends(get_db)):
   
   return auth_service.login(data=data,db=db,response=response)
    


@router.post("/logout", status_code = status.HTTP_200_OK)
def logout_user(response : Response):
   return auth_service.logout(response=response)


