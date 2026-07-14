from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def check_server():
    return "server is live and running ."