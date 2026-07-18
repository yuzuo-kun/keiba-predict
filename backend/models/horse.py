from typing import List

from pydantic import BaseModel

from models.race_history import RaceHistory


class Horse(BaseModel):
    horse_no: int              # 馬番
    history: List[RaceHistory] # 過去成績