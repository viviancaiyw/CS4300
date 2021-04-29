from app import db
from app.irsystem.models.movie import Movie
from app.irsystem.models.game import Game
import numpy as np
import json
from nltk.corpus import wordnet as wn
from . import raw_token_list, dict_token_to_id, basis_eigenvector, game_vectors, game_id_list, dict_gameid_to_idx
from .metadata_match import filter_games


def searchWrapper(singleplayer, multiplayer, raw_genre_list, free_list, movie_id):
    game_id_pool = filter_games(singleplayer, multiplayer, raw_genre_list)
    selected_game_vectors, selected_game_id_list, selected_dict_gameid_to_idx = selected_games(game_id_pool)
    return ranking_by_cosine_similarity(selected_game_vectors, selected_game_id_list, free_list, movie_id)

def selected_games(game_id_pool):
    idx_list = [dict_gameid_to_idx[game_id] for game_id in game_id_pool]
    idx_list.sort()
    selected_game_vectors = game_vectors[idx_list]
    selected_game_id_list = game_id_list[idx_list]
    return selected_game_vectors, selected_game_id_list

# return a list of syns of given token
def return_syns(token) -> list:
    res = []
    syn_n = wn.synsets(token, pos=wn.NOUN)
    syn_adj = wn.synsets(token, pos=wn.ADJ)
    syns = syn_n + syn_adj
    for syn in syns:
        for lem in syn.lemmas():
            res.append(lem.name())
    return list(set(res))


#
def ranking_by_cosine_similarity(game_vectors, game_id_list, free_list, movie_id):
    """
    free_list is the list of free typing strs
    """
    qvec = 0
    mvec = 0
    if movie_id is not None:
        mvec = json.loads(Movie.query.filter_by(link_id=movie_id).vector_pca)
    if free_list is not None:
        qlist = [entry.lower() for entry in free_list]
        for entry in qlist:
            if ' ' in entry:
                qlist.extend(entry.split())
        for term in free_list:
            qlist.extend(return_syns(term))
        qlist = list(set(qlist))

        qvec = np.zeros(len(raw_token_list))
        for term in qlist:
            if term in raw_token_list:
                if term in free_list:
                    qvec[dict_token_to_id[term]] += 5
                else:
                    qvec[dict_token_to_id[term]] += 2
        qvec = np.matmul(qvec, basis_eigenvector)
    qvec += mvec

    game_norms = np.linalg.norm(game_vectors, axis=1)

    scores = np.dot(game_vectors, qvec) / game_norms
    rank_idx_15 = np.flip(np.argsort(scores))[:15]
    rank_gameid = game_id_list[rank_idx_15]

    ret_list = []
    for game_id in rank_gameid:
        gameObj = Game.query.filter_by(app_id=game_id)
        temp_dict = {game_id: {'name':gameObj.name,
                             'developer': gameObj.developer,
                             'publisher':gameObj.publisher,
                             'tags':gameObj.tags,
                             'genre':gameObj.genre,
                             'single_player':gameObj.single_player,
                             'multi_player':gameObj.multi_player,
                             'rating':gameObj.rating,
                             'mature_content':gameObj.mature_content,
                             'url':gameObj.url
                             }}
        ret_list.append(temp_dict)

    return ret_list




