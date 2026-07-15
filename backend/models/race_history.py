from pydantic import BaseModel


class RaceHistory(BaseModel):
    distance: int              # 距離(m)
    time: str                  # タイム
    last3f: float | None       # 上がり
    first_corner: int | None   # 初回コーナー位置
    final_corner: int | None   # 最終コーナー位置