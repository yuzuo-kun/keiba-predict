from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Keiba Predict API")

# CSS・JavaScript配信用
app.mount("/static", StaticFiles(directory="../frontend"), name="static")


@app.get("/")
def root():
    return FileResponse("../frontend/index.html")


@app.get("/hello")
def hello():
    return {"message": "Hello FastAPI!"}