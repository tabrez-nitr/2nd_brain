from fastapi import APIRouter , Depends , HTTPException , status, Response 
from app.schemas.user import UserSchema , LoginSchema 
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import hash_password , verify_password , create_token
from datetime import datetime , timedelta




router = APIRouter() # for the routes beloning to user 


@router.post("/register", status_code = status.HTTP_201_CREATED)
def register_user(data : UserSchema , db : Session = Depends(get_db)):
    # check if the user already exists 
    user_exists = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user_exists:
        raise HTTPException (
            status_code= 400,
            detail = "User already exists",
        )
    #hash password 
    hashed_password = hash_password(data.password)
    # create model of new user to pass values to database 
    new_user = UserModel(
        name = data.name,
        email = data.email,
        hashed_password = hashed_password, # will update it later
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )
    
    # add user to database 
    db.add(new_user)
    
    # commit the changes 
    db.commit()
    
    # refresh the model 
    db.refresh(new_user)
    
    return {
        "message" : "User created sucessfully",
        "new user " : new_user
    }




# login user 
@router.post("/login", status_code = status.HTTP_202_ACCEPTED)
def login_user(data : LoginSchema , response : Response , db : Session = Depends(get_db)):
    # check if the user exists 
    user_exists = db.query(UserModel).filter(UserModel.email == data.email).first()
    if not user_exists :
        raise HTTPException(
            status_code=400,
            detail = "User Doesn't Exists"
        )
    # verify with hashed password 
    correct_password = verify_password(data.password , user_exists.hashed_password)
    if not correct_password:
        raise HTTPException(
            status_code= 401,
            detail = "Invalid Password"
        )
    
    # set cookie for further session 

    # create payload 
    payload = {
        "user_id" : user_exists.id,
        "exp" : DateTime + timedelta(hours=24),
    }

    token = create_token(payload)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,
        expires=60 * 60 * 24,
        samesite="lax",
        secure=False,
        path="/"
    )
    return {
        "message" : "Login was successful"
    }


@router.post("/logout", status_code = status.HTTP_200_OK)
def logout_user(response : Response):
    response.delete_cookie(
        key="access_token",
        path="/",
    )
    return {
        "message" : "Logout was successful"
    }


