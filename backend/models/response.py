from pydantic import BaseModel

from models.distance_horse import DistanceHorse
from models.info import Info


class PredictResponse(BaseModel):
    info: Info
    distance: list[DistanceHorse]