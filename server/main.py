from fastapi import FastAPI
from app.routes.user import router as user_router 
from app.db.database import Base , engine 
from app.routes.workspace import router as workspace_router


app = FastAPI()

#create tables if not exists
Base.metadata.create_all(bind = engine)

# incldue all the routes 
app.include_router(user_router , prefix = "/user" , tags=["User"])
app.include_router(workspace_router ,  prefix="/workspace" , tags=["workspace"])

@app.get("/")
def check_server():
    return "server is live and running ."