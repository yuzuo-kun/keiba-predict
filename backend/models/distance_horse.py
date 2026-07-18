from pydantic import BaseModel

from models.distance_data import DistanceData


class DistanceHorse(BaseModel):
    horse_no: int

    distances: list[DistanceData]