import json
import os
import re
from typing import List, Dict, Tuple

import nltk
import pandas as pd


def _get_parent_folder(path: str, level_up: int) -> str:
    res = path
    for i in range(level_up):
        res = os.path.dirname(res)
    return res


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = _get_parent_folder(CUR_DIR, 3)
DATA_DIR = os.path.join(ROOT_DIR, 'data')


def _clean_input(input_str: str) -> str:
    stop_words_file = os.path.join(DATA_DIR, 'movie_data',
                                   'title_stopwords.json')
    with open(stop_words_file, 'r') as f:
        stop_words = json.load(f)['stop words']
    input_str = re.sub(r'\W+', ' ', input_str.lower())
    text_tokens = nltk.tokenize.word_tokenize(input_str)
    tokens_without_sw = [word for word in text_tokens if not word in stop_words]
    return " ".join(tokens_without_sw)


def get_similar_movie(filtered_input_str: str):
    return filtered_input_str  # TODO: autocorrect spelling


def get_top_match_games(typed_mov_name: str) -> List[Tuple]:
    # movie_file = os.path.join(DATA_DIR, 'movie_data',
    #                           'movie_title_filtered_df_3.csv')
    # movie_df: pd.DataFrame = pd.read_csv(movie_file)
    #
    sim_file = os.path.join(
        DATA_DIR, 'steamData', '80k_data',
        'movie_game_title_similarity_4_no_zeros_app_id.json')
    with open(sim_file, 'r') as f:
        sim_dict = json.load(f)
    top_match: Dict[str, float] = sim_dict.get(typed_mov_name)
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
            res.append((app_id, game_name))
    return res


def match_movie_titles_to_games(input_str: str) -> List[Tuple]:
    if not input_str:
        return []
    cleaned_input: str = _clean_input(input_str)
    movie_to_match: str = get_similar_movie(cleaned_input)
    return get_top_match_games(movie_to_match)


if __name__ == '__main__':
    print(match_movie_titles_to_games('LEGO'))
