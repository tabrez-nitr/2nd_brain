from datetime import datetime 
from pydantic import BaseModel

class WorkSpaceCreate(BaseModel):
    name : str 
    description : str | None = None 


class WorkSpaceResponse(BaseModel):
    id : int
    name : str 
    description : str | None = None 
    owner_id : int 
    created_at : datetime

    class Config :
        from_attributes = True # This model can be created directly from an object's attributes, not just from a dictionary.
        # this helps to validate objects unlike we only do dictonary 
