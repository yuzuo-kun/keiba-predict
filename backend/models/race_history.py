from pydantic import BaseModel


class RaceHistory(BaseModel):
    race_place str | None     # 場所
    direction str | None      # 方向
    distance: int | None      # 距離(m)
    race_horce_no | None      # 馬番
    time: str | None          # タイム
    last3f: float | None      # 上がり
    first_corner: int | None # 初回コーナー位置
    final_corner: int | None  # 最終コーナー位置