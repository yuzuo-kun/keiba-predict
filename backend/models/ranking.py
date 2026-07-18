from typing import Optional

from pydantic import BaseModel


class Ranking(BaseModel):
    race_place: str
    distance: int
    avg_time_rank: Optional[int] = None
    avg_last3f_rank: Optional[int] = None
    best_last3f_rank: Optional[int] = None
    avg_first_corner_diff_rank: Optional[int] = None
    avg_final_corner_diff_rank: Optional[int] = None
