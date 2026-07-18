from typing import List

from pydantic import BaseModel

from models.horse import Horse


class Info(BaseModel):
    place: str  # 場所
    race_no: str  # レース番号
    race_name: str  # レース名
    race_distance: int # 距離
    horses: List[Horse]  # 馬一覧