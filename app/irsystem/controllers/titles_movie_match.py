import json
import os
import re
from collections import Counter
from typing import List, Dict, Tuple, Optional

import nltk
import pandas as pd

from app.irsystem.controllers import MOVIE_INFO


def _get_parent_folder(path: str, level_up: int) -> str:
    res = path
    for i in range(level_up):
        res = os.path.dirname(res)
    return res


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = _get_parent_folder(CUR_DIR, 3)
DATA_DIR = os.path.join(ROOT_DIR, 'data')


def _clean_input(input_str: str) -> str:
    """
    Filter the typed string `input_str`
    """
    stop_words_file = os.path.join(DATA_DIR, 'movie_data',
                                   'title_stopwords.json')
    with open(stop_words_file, 'r') as f:
        stop_words = json.load(f)['stop words']
    input_str = re.sub(r'\W+', ' ', input_str.lower())
    text_tokens = nltk.tokenize.word_tokenize(input_str)
    tokens_without_sw = [word for word in text_tokens if not word in stop_words]
    return " ".join(tokens_without_sw)


def _get_mov_filtered_name_from_id(
        mov_df: pd.DataFrame, mov_id: int) -> Optional[str]:
    """
    Return the movie name corresponding with the movie id
    """
    print(type(mov_id))
    matched_rows = mov_df[mov_df['id'] == mov_id].filtered_name.values
    print(list(matched_rows))
    if len(matched_rows) > 0:
        return list(matched_rows)[0]
    return None


def get_similar_movie(typed_movie_str: str) -> List[str]:
    """
    Given a typed string, find all possible movies names that may mean by the
    typed string. Do in a similarity match approach.
    
    @param typed_movie_str: user's typed string for the movie field
    @returns a list of movies name that similar to `typed_movie_str`
    """

    # filter the input to clean stop words
    tokens = _clean_input(typed_movie_str).split(' ')

    # load data
    with open(os.path.join(DATA_DIR, 'movie_data',
                           'inv_filtered_name_map.json'), 'r') as f:
        matched_ids = json.load(f)
    mov_file = os.path.join(DATA_DIR, 'movie_data',
                            'movie_title_filtered_df_3.csv')
    mov_df: pd.DataFrame = pd.read_csv(mov_file)

    # count the number of matched tokens between the filtered strings
    # and all movies' filtered name
    count_list = []
    for token in tokens:
        if token in matched_ids.keys():
            count_list += matched_ids.get(token)
    counts = Counter(count_list)
    top_movies = []
    for mov_id, count in counts.items():
        if count == max(counts.values()):
            top_movies.append(_get_mov_filtered_name_from_id(mov_df, mov_id))

    return top_movies


def get_top_match_games(typed_mov_name: str, k=None) -> List[Tuple]:
    """
    Returns a list of ranked games that are similar to the typed movie name
    `typed_mov_name`. Each element in the returned result is in
    (score, app_id, game name) format
    """
    sim_movies_ids = get_similar_movie(typed_mov_name)
    all_matched_games = []
    for sim_mov in sim_movies_ids:
        all_matched_games += _get_top_match_games_for_a_movie(str(sim_mov))
    ranked_mov = sorted(all_matched_games, key=lambda x: -x[0])
    print(ranked_mov)
    if not k or k > ranked_mov:
        return ranked_mov
    return ranked_mov[:k]


def _get_top_match_games_for_a_movie(filtered_mov_name: str) -> List[Tuple]:
    """
    Helper method for `get_top_match_games`. This returns a list of ranked
    games for a given filtered movie's name `filtered_mov_name`
    """
    sim_file = os.path.join(
        DATA_DIR, 'steamData', '80k_data',
        'movie_game_title_similarity_4_no_zeros_app_id.json')
    with open(sim_file, 'r') as f:
        sim_dict = json.load(f)
    top_match: Dict[str, float] = sim_dict.get(filtered_mov_name)
    if not top_match:
        return []

    game_file = os.path.join(DATA_DIR, 'steamData', 'available_games',
                             'available_game_filtered_title.csv')
    game_df: pd.DataFrame = pd.read_csv(game_file)
    res = []
    for app_id, score in top_match.items():
        if score > 0:
            matched_rows = game_df[game_df['app_id'] == int(app_id)]
            game_name = list(set(matched_rows.name.values))
            if len(game_name) > 0:
                game_name = game_name[0]
            res.append((score, app_id, game_name))
    return res


def get_top_games_from_title(movielink):
    # load data
    movie_name = MOVIE_INFO[movielink]['name']
    mov_4_col_path = os.path.join(DATA_DIR, 'movie_data',
                                  'movie_title_filtered_df_3.csv')
    with open(mov_4_col_path, 'r') as f:
        movie_filtered_df = pd.read_csv(f)
    movie_filtered_name = list(
        movie_filtered_df[
            movie_filtered_df['original_title'] == movie_name
        ].filtered_name.values)[0]
    return _get_top_match_games_for_a_movie(movie_filtered_name)


# TODO: delete this helper
# def inv_title_map():
#     movie_file = os.path.join(DATA_DIR, 'movie_data',
#                               'movie_title_filtered_df_3.csv')
#     movie_df: pd.DataFrame = pd.read_csv(movie_file)
#     inv_map = dict()
#     for _, row in movie_df.iterrows():
#         name = row.original_title
#         if type(name) is str:
#             # print(filtered_name)
#             name = name.lower()
#             tokens = nltk.tokenize.word_tokenize(name)
#             for token in tokens:
#                 if inv_map.get(token) is None:
#                     inv_map[token] = []
#                 inv_map[token].append(row.id)
#     with open(os.path.join(DATA_DIR, 'movie_data',
#                            'inv_filtered_name_map.json'), 'w+') as f:
#         json.dump(inv_map, f, indent=4)
#     return inv_map


if __name__ == '__main__':
    print(get_top_games_from_title('max_payne'))
    # get_top_match_games('Max Payne')
    # print(match_movie_titles_to_games('LEGO'))
