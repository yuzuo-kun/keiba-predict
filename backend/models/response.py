from pydantic import BaseModel
from models.info import Info

class PredictResponse(BaseModel):
    info: Info