from models.ranking import Ranking
from models.ranking_horse import RankingHorse


def analyze_ranking(distance_horses, max_horse_no):
    """
    距離別データから順位を計算する
    """
    result = []
    
    # race_placeとdistanceの組み合わせごとに順位を計算
    # まず全ての組み合わせを収集
    distance_keys = set()
    for dh in distance_horses:
        for dd in dh.distances:
            distance_keys.add((dd.race_place, dd.distance))
    
    for dh in distance_horses:
        rankings = []
        
        for race_place, distance in distance_keys:
            # このrace_placeとdistanceの全馬のデータを収集
            all_data = []
            for other_dh in distance_horses:
                for dd in other_dh.distances:
                    if dd.race_place == race_place and dd.distance == distance:
                        all_data.append({
                            "horse_no": other_dh.horse_no,
                            "avg_time": dd.avg_time,
                            "avg_last3f": dd.avg_last3f,
                            "best_last3f": dd.best_last3f,
                            "avg_first_corner_diff": dd.avg_first_corner_diff,
                            "avg_final_corner_diff": dd.avg_final_corner_diff
                        })
            
            # 現在の馬のデータを探す
            current_data = None
            for data in all_data:
                if data["horse_no"] == dh.horse_no:
                    current_data = data
                    break
            
            if current_data is None:
                continue
            
            # 各項目の順位を計算
            avg_time_rank = calculate_rank(all_data, "avg_time", max_horse_no, lower_is_better=True)
            avg_last3f_rank = calculate_rank(all_data, "avg_last3f", max_horse_no, lower_is_better=True)
            best_last3f_rank = calculate_rank(all_data, "best_last3f", max_horse_no, lower_is_better=True)
            avg_first_corner_diff_rank = calculate_rank(all_data, "avg_first_corner_diff", max_horse_no, lower_is_better=True)
            avg_final_corner_diff_rank = calculate_rank(all_data, "avg_final_corner_diff", max_horse_no, lower_is_better=True)
            
            # 現在の馬の順位を取得
            current_avg_time_rank = get_horse_rank(avg_time_rank, dh.horse_no)
            current_avg_last3f_rank = get_horse_rank(avg_last3f_rank, dh.horse_no)
            current_best_last3f_rank = get_horse_rank(best_last3f_rank, dh.horse_no)
            current_avg_first_corner_diff_rank = get_horse_rank(avg_first_corner_diff_rank, dh.horse_no)
            current_avg_final_corner_diff_rank = get_horse_rank(avg_final_corner_diff_rank, dh.horse_no)
            
            ranking = Ranking(
                race_place=race_place,
                distance=distance,
                avg_time_rank=current_avg_time_rank,
                avg_last3f_rank=current_avg_last3f_rank,
                best_last3f_rank=current_best_last3f_rank,
                avg_first_corner_diff_rank=current_avg_first_corner_diff_rank,
                avg_final_corner_diff_rank=current_avg_final_corner_diff_rank
            )
            rankings.append(ranking)
        
        result.append(
            RankingHorse(
                horse_no=dh.horse_no,
                rankings=rankings
            )
        )
    
    return result


def calculate_rank(all_data, field_name, max_horse_no, lower_is_better=True):
    """
    指定されたフィールドの順位を計算する
    Noneの値は最下位（max_horse_no）とする
    """
    # 値とhorse_noのペアを収集
    values = []
    for data in all_data:
        value = data[field_name]
        if value is not None:
            values.append((data["horse_no"], value))
        else:
            values.append((data["horse_no"], None))
    
    # 値でソート（Noneは最後に）
    if lower_is_better:
        values.sort(key=lambda x: (x[1] is None, x[1] if x[1] is not None else float('inf')))
    else:
        values.sort(key=lambda x: (x[1] is None, -(x[1] if x[1] is not None else float('inf'))))
    
    # 順位を割り当て（Noneはmax_horse_no）
    rankings = {}
    for rank, (horse_no, value) in enumerate(values, start=1):
        if value is None:
            rankings[horse_no] = max_horse_no
        else:
            rankings[horse_no] = rank
    
    return rankings


def get_horse_rank(rankings, horse_no):
    """
    指定された馬の順位を取得する
    """
    return rankings.get(horse_no, None)
