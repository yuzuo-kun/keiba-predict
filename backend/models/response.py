from pydantic import BaseModel

from models.horse import Horse


class PredictResponse(BaseModel):
    horses: list[Horse]