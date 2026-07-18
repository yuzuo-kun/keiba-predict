from pydantic import BaseModel

from models.distance_horse import DistanceHorse
from models.info import Info
from models.ranking_horse import RankingHorse


class PredictResponse(BaseModel):
    info: Info
    distance: list[DistanceHorse]
    ranking: list[RankingHorse]