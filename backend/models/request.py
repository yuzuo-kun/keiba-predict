from pydantic import BaseModel

class PredictRequest(BaseModel):
    url: str