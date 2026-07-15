from fastapi import APIRouter , Depends , HTTPException , status 
from sqlalchemy.orm import Session 

from app.db.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import UserModel 
from app.schemas.workspace import WorkSpaceCreate , WorkSpaceResponse
from app.services.workspaces import WorkSpaceService 

router = APIRouter()

workspace_service = WorkSpaceService() # obj of workspace Service that has all the fucntion 

@router.post("/create" , status_code = status.HTTP_201_CREATED)
def create_workspace(data : WorkSpaceCreate , db : Session = Depends(get_db) , current_user : UserModel =   Depends(get_current_user)):

    return workspace_service.create_workspace(data = data , current_user=current_user ,db =  db)

# get all workspaces 
@router.get("/all", status_code = status.HTTP_200_OK)
def get_workspaces(current_user : UserModel = Depends(get_current_user) , db : Session = Depends(get_db)):
    return workspace_service.get_all_workspaces(current_user = current_user , db = db)



#get single workspace 
@router.get("/one/{workspace_id}", status_code=status.HTTP_200_OK)
def get_one_workspace(
    workspace_id : int , current_user : UserModel = Depends(get_current_user) , db : Session = Depends(get_db)
):
 #serch for the workspace and does it belong to the current user 
 workspace = workspace_service.get_workspace(
    workspace_id,
    current_user,
    db
 )
 if not workspace :
    raise HTTPException(
        status_code = 404 ,
        detail = "workspace not found",
    )

 return workspace

@router.delete("/delete/{workspace_id}", status_code = status.HTTP_202_ACCEPTED)
def delete_workspace(workspace_id : int , current_user : UserModel = Depends(get_current_user) , db : Session = Depends(get_db)):
    # find the workspace 
    workspace = workspace_service.get_workspace(
        workspace_id , 
        current_user,
        db
    )

    if not workspace:
        raise HTTPException(
            status_code = 404,
            detail = "Workspace not found"
        )
    #delete workspace by passing model obj 
    return workspace_service.delete_workspace(
        workspace,
        db
    )

