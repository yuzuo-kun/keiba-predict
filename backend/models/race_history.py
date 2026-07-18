from typing import Optional

from pydantic import BaseModel


class RaceHistory(BaseModel):
    race_place: Optional[str]     # 場所
    direction: Optional[str]      # 方向
    distance: Optional[int]      # 距離(m)
    race_horse_no: Optional[int]      # 馬番
    time: Optional[str]          # タイム
    last3f: Optional[float]      # 上がり
    first_corner: Optional[int] # 初回コーナー位置
    final_corner: Optional[int]  # 最終コーナー位置