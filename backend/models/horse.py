from pydantic import BaseModel

from models.race_history import RaceHistory


class Horse(BaseModel):
    horse_no: int              # 馬番
    history: list[RaceHistory] # 過去成績