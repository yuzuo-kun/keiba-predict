import re

from bs4 import BeautifulSoup

from models.horse import Horse
from models.info import Info
from models.race_history import RaceHistory

def extract_info(soup: BeautifulSoup) -> Info:
    """BeautifulSoupオブジェクトからレース情報を抽出する"""
    # レース情報のテーブルを抽出
    race_info_table = soup.select_one('article.raceCard')
    
    place = ""
    race_no = ""
    race_name = ""
    race_distance = 0
    
    if race_info_table:
        place_elem = race_info_table.select_one('a.cNaviBtn.courseBtn.active')
        if place_elem:
            place = place_elem.text.strip()
        
        race_no_elem = race_info_table.select_one('a.cNaviBtn.raceNum.active')
        if race_no_elem:
            race_no = race_no_elem.text.strip()
        
        race_name_elem = race_info_table.select_one('section.raceTitle h3')
        if race_name_elem:
            race_name = race_name_elem.text.strip()
        
        race_distance_elem = race_info_table.select_one('section.raceTitle ul.dataArea li')
        if race_distance_elem:
            match = re.search(r'(\d+)ｍ', race_distance_elem.get_text(strip=True))
            if match:
                race_distance = int(match.group(1))
    
    horses = extract_horses(soup)
    
    return Info(
        place=place,
        race_no=race_no,
        race_name=race_name,
        race_distance=race_distance,
        horses=horses
    )

def extract_horses(soup: BeautifulSoup) -> list[Horse]:
    """BeautifulSoupオブジェクトから馬のリストを抽出する"""
    horses = []
    
    # 出馬表の馬情報を抽出
    horse_rows = soup.select('tr.tBorder')
    
    for row in horse_rows:
        horse_no = extract_horse_no(row)
        if horse_no == 0:
            continue
            
        history = extract_race_history(row)
        
        horse = Horse(
            horse_no=horse_no,
            history=history
        )
        horses.append(horse)
    
    return horses


def extract_horse_no(row) -> int:
    """馬番を抽出する"""
    horse_no_elem = row.select_one('td.horseNum')
    if horse_no_elem:
        try:
            return int(horse_no_elem.text.strip())
        except ValueError:
            return 0
    return 0


def extract_race_history(row) -> list[RaceHistory]:
    """過去成績を抽出する"""
    history = []
    
    # 過去5走のraceInfoを抽出
    race_infos = row.select('div.raceInfo')
    
    # タイム・コーナー通過順・上がり3Fの行を取得
    # 次のtrを探す必要がある
    time_corner_3f_row = row.find_next_siblings('tr')[2]
    if not time_corner_3f_row:
        return history
    
    time_corner_3f_cells = time_corner_3f_row.select('td')
    
    # 3〜7個目のtdに過去5走分のデータが入っている
    # インデックス2〜6を使用
    race_data_cells = time_corner_3f_cells[2:7]
    
    for i, race_info in enumerate(race_infos):
        if i >= len(race_data_cells):
            break
        
        # 場所、方向、距離、馬番を抽出
        race_place, direction, distance, race_horse_no = extract_race_info(race_info)
        
        # タイム・コーナー・上がりを抽出
        time, last3f, corners = extract_time_info(race_data_cells[i])
        
        first_corner, final_corner = extract_corners(corners)
        
        race_history = RaceHistory(
            race_place=race_place,
            direction=direction,
            distance=distance,
            race_horse_no=race_horse_no,
            time=time,
            last3f=last3f,
            first_corner=first_corner,
            final_corner=final_corner
        )
        history.append(race_history)
    
    return history


def extract_race_info(race_info):
    """raceInfoから場所・方向・距離・馬番を抽出する"""

    text = race_info.get_text(" ", strip=True)

    match = re.search(r'(\S+)\s*(左|右|直)(\d+)\s*(\d+)番', text)

    if match:
        return (
            match.group(1),          # place
            match.group(2),          # direction
            int(match.group(3)),     # distance
            int(match.group(4))      # horse_no
        )

    return "", "", 0, 0


def extract_time_info(time_cell) -> tuple[str, float | None, str]:
    """タイムセルからタイム、上がり、コーナー通過順を抽出する"""
    text = time_cell.get_text().strip()
    
    # 例: "1:18.0　7-7-5　39.0" のような形式
    parts = text.split()
    
    time = ""
    last3f = None
    corners = ""
    
    if len(parts) >= 1:
        time = parts[0]
    
    if len(parts) >= 2:
        corners = parts[1]
    
    if len(parts) >= 3:
        try:
            last3f = float(parts[2])
        except ValueError:
            pass
    
    return time, last3f, corners


def extract_corners(corners_str: str) -> tuple[int | None, int | None]:
    """コーナー通過順から初回と最終を抽出する"""
    if not corners_str:
        return None, None
    
    parts = corners_str.split('-')
    
    first_corner = None
    final_corner = None
    
    if len(parts) >= 1:
        try:
            first_corner = int(parts[0].strip())
        except ValueError:
            pass
    
    if len(parts) >= 2:
        try:
            final_corner = int(parts[-1].strip())
        except ValueError:
            pass
    
    return first_corner, final_corner