from typing import List, Dict

import psycopg2

database_config = {
    "database": 'dd46p10a83f3m0', "user": 'bivxusanexnbjp',
    "password": '12f8e000800ba66e4f98d0df4795edc962bdfd5318cbd9f19c7eaf16ef244f54',
    "host": 'ec2-52-23-45-36.compute-1.amazonaws.com',
    "port": 5432}


def get_matched_game_ranking_info(movie_id: str) -> Dict[str, int]:
    """
    Query the corresponding match ranking from DB.
    """
    # setup connection
    conn = psycopg2.connect(**database_config)
    cursor = conn.cursor()

    # fetch result
    query = f"""
        SELECT
            games_title_match
        FROM
            "public"."movies"
        WHERE
            link_id = '{movie_id}';
        """
    cursor.execute(query)
    result = cursor.fetchall()

    # parse result
    if result:
        return eval(result[0][0])
    return dict()


def get_game_info(game_ids: List[str], cols: List[str]) -> Dict[str, Dict]:
    """
    Query game info of games specified in list `game_ids`. Wanted columns
    specified in list `cols`.
    """
    # setup connection
    conn = psycopg2.connect(**database_config)
    cursor = conn.cursor()

    query = f"""
        SELECT
            {', '.join(cols)}
        FROM
            "public"."games"
        WHERE
            app_id IN {str(tuple(game_ids))};"""

    cursor.execute(query)
    result = cursor.fetchall()

    result_in_dict = dict()
    if result:
        for info_tuple in result:
            app_id = info_tuple[0]
            result_in_dict[app_id] = dict()
            for i in range(len(cols)):
                result_in_dict[app_id][cols[i]] = info_tuple[i]
    return result_in_dict


def get_top_games_from_title(mov_tmt_path: str, threshold=0.5) -> List[Dict]:
    """
    Given a movie's rotten tomato's path `mov_tmt_path`, return a map of all
    top similar movies i.e. similar score between titles > `threshold`
    """
    if not mov_tmt_path:
        return []
    ranking_info = get_matched_game_ranking_info(movie_id=mov_tmt_path)
    res = []
    matched_games = list(ranking_info.keys())
    game_needed_cols = ["app_id", "name", "url"]
    games_info = get_game_info(matched_games, cols=game_needed_cols)
    for app_id, score in ranking_info.items():
        if score >= threshold:
            game_info = {'app_id': app_id,
                         'name': games_info[app_id]['name'],
                         'url': games_info[app_id]['url'],
                         'title_match_score': score}
            res.append(game_info)
    return res
