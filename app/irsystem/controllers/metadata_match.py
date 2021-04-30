# num of players filtering, genres weighting
from app.irsystem.controllers import GENRE_KEY
from app.irsystem.models.movie import Movie
from app.irsystem.models.game import Game


def _gen_sql_query(raw_genre_list):
    """
    raw_genre_list: list of raw user genre input from the UI
    Returns: The sqlalchemy query for a give genre list to filter the game by    
    """
    if raw_genre_list is not None:
        genre_list = []
        for genre in raw_genre_list:
            genre_list.append(GENRE_KEY[genre])
        print(genre_list)
        query = """Game.query.filter(Game.single_player == singleplayer, Game.multi_player == multiplayer,("""
        for genre in genre_list:
            query = query + "Game.genre.like('%{}%')|".format(genre)
        query = query[:-1] + ')).all()'
        return query
    else:
        return None


def filter_games(singleplayer: bool, multiplayer: bool, raw_genre_list):
    """
    Returns: list of game ids filtered by number of players and list of input genre
    """
    query = _gen_sql_query(raw_genre_list)
    if query is not None:
        res_games = eval(query)
        # res_games = Game.query.filter(
        #     Game.single_player == singleplayer, Game.multi_player == multiplayer,
        #     (Game.genre.like('%action%')|Game.genre.like('%adventure%'))).limit(10)
        res = [game.app_id for game in res_games]
        # for game in res_games:
        #     game_info = {
        #         'id': game.app_id,
        #         'name': game.name,
        #         'genre': game.genre
        #     }
        #     res.append(game_info)
        return res
    else:
        return None
