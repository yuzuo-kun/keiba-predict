from fastapi import FastAPI
from api.predict import router as predict_router

app = FastAPI(title="Keiba Predict API")

app.include_router(predict_router)


@app.get("/")
def root():
    return {
        "message": "Keiba Predict API is running!"
    }