from collections import defaultdict

from models.distance_data import distance_data
from models.distance_horse import distance_horse


def analyze_distance(info) -> list[distance_horse]:
    """
    全馬の過去レースを
    ・同競馬場
    ・全競馬場
    の距離別に分類する
    """

    result = []

    for horse in info.horses:
        result.append(analyze_horse(horse, info.race_place))

    return result


def analyze_horse(horse, race_place) -> distance_horse:
    """
    1頭分の距離別データを作成
    """

    distance_list = []

    # 同競馬場
    same_course = group_same_course(horse.histories, race_place)
    distance_list.extend(same_course)

    # 全競馬場
    all_course = group_all_course(horse.histories)
    distance_list.extend(all_course)

    return distance_horse(
        horse_no=horse.horse_no,
        distances=distance_list
    )


def group_same_course(histories, race_place) -> list[distance_data]:
    """
    同競馬場・距離別
    """

    groups = defaultdict(list)

    for history in histories:
        if history.race_place != race_place:
            continue

        groups[history.distance].append(history)

    result = []

    for distance, history_list in groups.items():
        result.append(
            distance_data(
                race_place=race_place,
                distance=distance,
                histories=history_list
            )
        )

    return result


def group_all_course(histories) -> list[distance_data]:
    """
    全競馬場・距離別
    """

    groups = defaultdict(list)

    for history in histories:
        groups[history.distance].append(history)

    result = []

    for distance, history_list in groups.items():
        result.append(
            distance_data(
                race_place="",
                distance=distance,
                histories=history_list
            )
        )

    return result