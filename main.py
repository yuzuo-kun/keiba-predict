from fastapi import FastAPI

app = FastAPI(title="Keiba Predict API")


@app.get("/")
def root():
    return {
        "message": "Keiba Predict API is running!"
    }


@app.get("/hello")
def hello():
    return {
        "message": "Hello FastAPI!"
    }


@app.get("/predict")
def predict():
    return {
        "status": "success",
        "race": "Kasamatsu 5R",
        "prediction": [
            {
                "horse_no": 5,
                "score": 95
            },
            {
                "horse_no": 6,
                "score": 90
            },
            {
                "horse_no": 7,
                "score": 88
            }
        ]
    }