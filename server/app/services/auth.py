from datetime import datetime , timedelta 

from fastapi import HTTPException , Response , status 
from sqlalchemy.orm import Session

from app.models.user import UserModel
from app.schemas.user import UserSchema , LoginSchema
from app.core.security import create_token , hash_password , verify_password




# auth class with all auth related fucntion in ones 
class AuthService:

    #register function 
    def register(self , data : UserSchema , db : Session)->UserModel:
        # Check if user already exists
        user = (
            db.query(UserModel)
            .filter(UserModel.email == data.email)
            .first()
        )
        # user already exists 
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        # Hash password
        hashed_password = hash_password(data.password)

        # Create user
        new_user = UserModel(
            name=data.name,
            email=data.email,
            hashed_password=hashed_password,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        #commit to db 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        #return user 
        return new_user

    #login user 
    def login(
        self,
        data: LoginSchema,
        db: Session,
        response: Response,
    ):
        #check if the user exists 
        user = (
            db.query(UserModel)
            .filter(UserModel.email == data.email)
            .first()
        )
        #if no user is found return exception 
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist",
            )
        #check if the password matches 
        if not verify_password(
            data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        
        #payload to generate JWT token 
        payload = {
            "user_id": user.id,
            "exp": datetime.now() + timedelta(hours=24),
        }

        token = create_token(payload)
         
         # set cookie for further session 
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 60 * 24,
            expires=60 * 60 * 24,
            path="/",
        )
        return {
            "message": "Login successful"
        }





    # logout , remove cookie 
    def logout(
        self,
        response: Response,
    ):
        
        response.delete_cookie(
            key="access_token",
            path="/",
        )

        return {
            "message": "Logout successful"
        }



    
