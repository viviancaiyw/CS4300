from typing import List, Dict

from app.irsystem.models.game import Game
from app.irsystem.models.movie import Movie
import json


def get_matched_game_ranking_info(movie_id: str) -> Dict[str, int]:
    """
    Query the corresponding match ranking from DB.
    """
    query_res = Movie.query.filter_by(link_id=movie_id).all()
    if query_res:
        return eval(query_res[0].games_title_match)
    return dict()


def get_top_games_from_title(mov_tmt_path: str, candidate_games: List[str],
                             threshold=0.5) -> List[Dict]:
    """
    Given a movie's rotten tomato's path `mov_tmt_path`, return a map of all
    top similar movies i.e. similar score between titles > `threshold` who
    appears in `candidate_games`
    """
    if not mov_tmt_path or not candidate_games:
        return []
    ranking_info = get_matched_game_ranking_info(movie_id=mov_tmt_path)
    res = []
    for app_id, score in ranking_info.items():
        if score >= threshold and app_id in candidate_games:
            game_obj: Game = Game.query.filter_by(app_id=app_id).all()[0]
            game_info = {
                'app_id': app_id,
                'name': game_obj.name,
                'developer': ", ".join(json.loads(game_obj.developer)),
                'publisher': ", ".join(json.loads(game_obj.publisher)),
                'tags': json.loads(game_obj.tags),
                'genre': json.loads(game_obj.genre),
                'single_player': game_obj.single_player,
                'multi_player': game_obj.multi_player,
                'rating': game_obj.rating,
                'mature_content': game_obj.mature_content,
                'title_match_score': score}
            res.append(game_info)
    return res
