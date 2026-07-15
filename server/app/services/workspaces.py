from sqlalchemy.orm import Session 

from app.models.workspace import WorkSpaceModel
from app.schemas.workspace import WorkSpaceCreate
from app.models.user import UserModel


# class with all the workspace functions 
class WorkSpaceService:

     
    #create workspace 
    def create_workspace(self , data : WorkSpaceCreate , db : Session , current_user : UserModel ):
        # create workspace model 
        workspace = WorkSpaceModel(
            name = data.name,
            description = data.description,
            owner_id = current_user.id
        )
        db.add(workspace)
        db.commit()
        db.refresh(workspace)

        return workspace # return workspace 
    
    # returns all the workspaces 
    def get_all_workspaces( self , current_user : UserModel , db : Session):
        all_workspaces = db.query(WorkSpaceModel).filter(
            WorkSpaceModel.owner_id == current_user.id
        ).all() # return all workspaces that belong to the user 
    
        return all_workspaces # return all the  
    
    #return one workspace with id 
    def get_workspace(self , workspace_id : int , current_user : UserModel , db : Session):
        # get the workspace with the id and belongs to the user
        print(workspace_id)
       
        workspace = db.query(WorkSpaceModel).filter(
            WorkSpaceModel.id == workspace_id, 
            WorkSpaceModel.owner_id == current_user.id
        ).first()
        return workspace

    
     
    def delete_workspace(
        self , 
        workspace : WorkSpaceModel,
        db : Session,
    ):
      db.delete(workspace) #we got the workspace obj we directly delete it 
      db.commit()
      return {"message" : "Workspace deleted successfully"} # return message 
    

    
    
