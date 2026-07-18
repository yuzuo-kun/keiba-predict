from typing import Optional

from pydantic import BaseModel

from models.race_history import RaceHistory


class DistanceData(BaseModel):
    race_place: str
    distance: int

    histories: list[RaceHistory]

    avg_time: Optional[str] = None
    avg_last3f: Optional[float] = None
    best_last3f: Optional[float] = None
    avg_first_corner_diff: Optional[float] = None
    avg_final_corner_diff: Optional[float] = None