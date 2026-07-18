from analyzer.distance import analyze_distance
from analyzer.ranking import analyze_ranking


def calculate_distance_stats(histories, horse_no):
    """
    履歴から統計情報を計算する
    """
    if not histories:
        return {
            "avg_time": None,
            "avg_last3f": None,
            "best_last3f": None,
            "avg_first_corner_diff": None,
            "avg_final_corner_diff": None
        }
    
    # タイムの計算（秒に変換して平均）
    times = []
    for h in histories:
        if h.time:
            try:
                # タイム形式 "1:23.4" を秒に変換
                parts = h.time.split(":")
                if len(parts) == 2:
                    minutes = int(parts[0])
                    seconds = float(parts[1])
                    times.append(minutes * 60 + seconds)
            except (ValueError, AttributeError):
                pass
    
    avg_time = None
    if times:
        avg_seconds = sum(times) / len(times)
        avg_minutes = int(avg_seconds // 60)
        avg_seconds_remainder = avg_seconds % 60
        avg_time = f"{avg_minutes}:{avg_seconds_remainder:.1f}"
    
    # last3fの計算
    last3f_values = [h.last3f for h in histories if h.last3f is not None]
    avg_last3f = sum(last3f_values) / len(last3f_values) if last3f_values else None
    best_last3f = min(last3f_values) if last3f_values else None
    
    # コーナー位置の差の計算（馬番との差）
    first_corner_diffs = []
    final_corner_diffs = []
    for h in histories:
        if h.first_corner is not None:
            first_corner_diffs.append(h.first_corner - horse_no)
        if h.final_corner is not None:
            final_corner_diffs.append(h.final_corner - horse_no)
    
    avg_first_corner_diff = sum(first_corner_diffs) / len(first_corner_diffs) if first_corner_diffs else None
    avg_final_corner_diff = sum(final_corner_diffs) / len(final_corner_diffs) if final_corner_diffs else None
    
    return {
        "avg_time": avg_time,
        "avg_last3f": avg_last3f,
        "best_last3f": best_last3f,
        "avg_first_corner_diff": avg_first_corner_diff,
        "avg_final_corner_diff": avg_final_corner_diff
    }


def calculate(info):
    """
    各Analyzerを実行する
    """

    distance = analyze_distance(info)
    
    # 統計情報を計算して埋める
    for distance_horse in distance:
        for distance_data in distance_horse.distances:
            stats = calculate_distance_stats(distance_data.histories, distance_horse.horse_no)
            distance_data.avg_time = stats["avg_time"]
            distance_data.avg_last3f = stats["avg_last3f"]
            distance_data.best_last3f = stats["best_last3f"]
            distance_data.avg_first_corner_diff = stats["avg_first_corner_diff"]
            distance_data.avg_final_corner_diff = stats["avg_final_corner_diff"]
    
    # 最大馬番を取得
    max_horse_no = max(horse.horse_no for horse in info.horses) if info.horses else 0
    
    # 順位を計算
    ranking = analyze_ranking(distance, max_horse_no)

    return distance, ranking