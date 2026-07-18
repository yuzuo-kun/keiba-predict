from models.distance_data import distance_data
from models.distance_horse import distance_horse


def analyze_distance(info) -> list[distance_horse]:
    """
    全馬の距離別データを作成する
    """

    same_course_distances = get_same_course_distances(info)
    all_course_distances = get_all_course_distances(info)

    result = []

    for horse in info.horses:
        result.append(
            analyze_horse(
                horse,
                info.race_place,
                same_course_distances,
                all_course_distances
            )
        )

    return result


def get_same_course_distances(info) -> list[int]:
    """
    同競馬場で使用されている距離一覧を取得
    """

    distances = set()

    for horse in info.horses:
        for history in horse.history:
            if history.race_place == info.race_place:
                distances.add(history.distance)

    return sorted(distances)


def get_all_course_distances(info) -> list[int]:
    """
    全競馬場で使用されている距離一覧を取得
    """

    distances = set()

    for horse in info.horses:
        for history in horse.history:
            distances.add(history.distance)

    return sorted(distances)


def analyze_horse(
    horse,
    race_place,
    same_course_distances,
    all_course_distances
) -> distance_horse:
    """
    1頭分の距離別データを作成
    """

    distances = []

    # 同競馬場
    for distance in same_course_distances:

        histories = [
            history
            for history in horse.histories
            if history.race_place == race_place
            and history.distance == distance
        ]

        distances.append(
            distance_data(
                race_place=race_place,
                distance=distance,
                histories=histories
            )
        )

    # 全競馬場
    for distance in all_course_distances:

        histories = [
            history
            for history in horse.histories
            if history.distance == distance
        ]

        distances.append(
            distance_data(
                race_place="",
                distance=distance,
                histories=histories
            )
        )

    return distance_horse(
        horse_no=horse.horse_no,
        distances=distances
    )