from pydantic import BaseModel

from models.ranking import Ranking


class RankingHorse(BaseModel):
    horse_no: int
    rankings: list[Ranking]
