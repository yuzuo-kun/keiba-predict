from pydantic import BaseModel

from models.distance_horse import distance_horse
from models.info import Info


class PredictResponse(BaseModel):
    info: info
    distance: list[distance_horse]