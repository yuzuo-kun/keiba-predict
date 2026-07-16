from pydantic import BaseModel

from models.distance_data import distance_data


class distance_horse(BaseModel):
    horse_no: int

    distances: list[distance_data]