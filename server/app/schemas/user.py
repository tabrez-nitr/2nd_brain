from pydantic import BaseModel 


# to validate user form 
class UserSchema(BaseModel):
    name : str 
    email : str 
    password : str 

class LoginSchema(BaseModel):
    email : str 
    password : str




    