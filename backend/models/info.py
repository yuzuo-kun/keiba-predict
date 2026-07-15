from pydantic import BaseModel

from models.horse import Horse


class Info(BaseModel):
    place: str  # 場所
    race_no: str  # レース番号
    race_name: str  # レース名
    horses: list[Horse]  # 馬一覧