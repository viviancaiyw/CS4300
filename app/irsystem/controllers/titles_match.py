import json

from app.irsystem.controllers import MOVIE_GAME_TITLE_SIMILARITY, GAME_INFO


def get_top_games_from_title(mov_tmt_path: str, threshold=0.15) -> str:
    """
    Given a movie's rotten tomato's path `mov_tmt_path`, return a map of all
    top similar movies i.e. similar score between titles > `threshold`
    """
    ranking_info = MOVIE_GAME_TITLE_SIMILARITY[mov_tmt_path]
    res = []
    for app_id, score in ranking_info.items():
        if score >= threshold:
            res.append(GAME_INFO[app_id])
    return json.dumps(res)
