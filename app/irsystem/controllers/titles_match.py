from typing import List, Dict

from app.irsystem.controllers import MOVIE_GAME_TITLE_SIMILARITY, GAME_INFO


def get_top_games_from_title(mov_tmt_path: str, threshold=0.25) -> List[Dict]:
    """
    Given a movie's rotten tomato's path `mov_tmt_path`, return a map of all
    top similar movies i.e. similar score between titles > `threshold`
    """
    if not mov_tmt_path:
        return []
    ranking_info = MOVIE_GAME_TITLE_SIMILARITY.get(mov_tmt_path, [])
    res = []
    print("titles rankings: " + str(ranking_info))
    for app_id, score in ranking_info.items():
        if score >= threshold:
            game_info = {'app_id': app_id,
                         'name': GAME_INFO[app_id]['name'],
                         'developer': GAME_INFO[app_id]['developer'],
                         'publisher': GAME_INFO[app_id]['publisher'],
                         'num_players': GAME_INFO[app_id]['num_players'],
                         'rating': GAME_INFO[app_id]['rating'],
                         'url': GAME_INFO[app_id]['url'],
                         'title_match_score': score}
            res.append(game_info)
    return res
