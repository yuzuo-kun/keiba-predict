from analyzer.distance import analyze_distance


def calculate(info):
    """
    各Analyzerを実行する
    """

    distance = analyze_distance(info)

    return distance