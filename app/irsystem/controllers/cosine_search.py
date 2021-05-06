from app import db
from app.irsystem.models.movie import Movie
from app.irsystem.models.game import Game
import numpy as np
import json
from nltk.corpus import wordnet as wn
from . import raw_token_list, dict_token_to_id, basis_eigenvector, dict_gameid_to_idx
from .metadata_match import filter_games


def searchWrapper(singleplayer, multiplayer, raw_genre_list, free_list, movie_id, game_id, all_game_vectors, all_game_id_list):
    game_id_pool = filter_games(singleplayer, multiplayer, raw_genre_list)
    selected_game_vectors, selected_game_id_list = selected_games(game_id_pool, all_game_vectors, all_game_id_list)
    res = ranking_by_cosine_similarity(selected_game_vectors, selected_game_id_list, free_list, movie_id, game_id, all_game_vectors)
    if game_id != None:
        res = res[1:]
    return res


def selected_games(game_id_pool, game_vectors, game_id_list):
    if game_id_pool is not None:
        idx_list = [dict_gameid_to_idx[game_id] for game_id in game_id_pool]
        idx_list.sort()
        selected_game_vectors = game_vectors[idx_list]
        selected_game_id_list = game_id_list[idx_list]
        return selected_game_vectors, selected_game_id_list
    else:
        return game_vectors, game_id_list

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
def ranking_by_cosine_similarity(selected_game_vectors, selected_game_id_list, free_list, movie_id, game_id, all_game_vectors):
    """
    free_list is the list of free typing strs
    """
    if movie_id is not None:
        mvec = np.array(json.loads(Movie.query.filter_by(
            link_id=movie_id).first().vector_pca))
    else:
        mvec = 0

    if game_id is not None:
        g_idx = dict_gameid_to_idx[game_id]
        gvec = all_game_vectors[g_idx]
    else:
        gvec = 0

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
                    qvec[dict_token_to_id[term]] += 10
                else:
                    qvec[dict_token_to_id[term]] += 4
        qvec = np.matmul(qvec, basis_eigenvector)
    else:
        qvec = 0

    if type(mvec) == np.ndarray:
        qvec += mvec / np.linalg.norm(mvec)
    if type(gvec) == np.ndarray:
        qvec += gvec / np.linalg.norm(gvec)

    selected_game_norms = np.linalg.norm(selected_game_vectors, axis=1)

    scores = np.dot(selected_game_vectors, qvec) / selected_game_norms
    rank_idx_15 = np.flip(np.argsort(scores))[:15]
    rank_gameid = selected_game_id_list[rank_idx_15]

    ret_list = []
    for game_id in rank_gameid:
        core_token_list = retrieve_keywords_score(game_id, qvec, all_game_vectors)
        gameObj = Game.query.filter_by(app_id=game_id).first()
        tags = json.loads(gameObj.tags)
        tags.extend(free_list)
        new_core_token_list = []
        for word in core_token_list:
            if word in tags:
                new_core_token_list.append(word)
        core_token_list = set(core_token_list).intersection(set(tags))
        temp_dict = {
            'app_id': game_id,
            'name': gameObj.name,
            'developer': ", ".join(json.loads(gameObj.developer)),
            'publisher': ", ".join(json.loads(gameObj.publisher)),
            'tags': tags,
            'genre': json.loads(gameObj.genre),
            'single_player': gameObj.single_player,
            'multi_player': gameObj.multi_player,
            'rating': gameObj.rating,
            'mature_content': gameObj.mature_content,
            'matching_tokens': new_core_token_list[:10],
            'num_matching_tokens': len(core_token_list)
        }
        ret_list.append(temp_dict)

    ret_list = sorted(ret_list, key = lambda i: i['num_matching_tokens'], reverse=True)

    return ret_list


def retrieve_keywords_score(game_id, qvec, all_game_vectors):
    index = dict_gameid_to_idx[game_id]
    game_vec = all_game_vectors[index]
    key_index = np.flip(np.argsort(game_vec * qvec))[:50]
    token_score = np.zeros(len(raw_token_list))
    for idx in key_index:
        token_score += basis_eigenvector[:, idx]
    selected_token_idx = np.flip(np.argsort(token_score))[:50]
    selected_token = np.array(raw_token_list)[selected_token_idx]
    # svd_res_idx = np.nonzero(token_score)
    # svd_res_token = np.array(raw_token_list)[svd_res_idx]
    return selected_token
    # return svd_res_token