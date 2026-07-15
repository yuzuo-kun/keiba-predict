from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.predict import router as predict_router

app = FastAPI(title="Keiba Predict API")

# CSS・JavaScript配信用
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

origins = [
    "https://keiba-predict-frontend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(predict_router)


@app.get("/")
def root():
    return FileResponse("../frontend/index.html")