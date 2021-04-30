# Import flask deps
from flask import request, render_template, \
    flash, g, session, redirect, url_for, jsonify, abort, Response

# For decorators around routes
from functools import wraps

# Import for pass / encryption
from werkzeug import check_password_hash, generate_password_hash

# Import the db object from main app module
from app import db

# Marshmallow
from marshmallow import ValidationError

# Import socketio for socket creation in this module
from app import socketio

# Import module models
# from app.irsystem import search

# IMPORT THE BLUEPRINT APP OBJECT
from app.irsystem import irsystem

# Import module models
# from app.accounts.models.user import *
# from app.accounts.models.session import *
import resource
import json
import os
import numpy as np
from app.irsystem.models.eigenvector import eigenvector
from app.irsystem.models.game import Game
from app.irsystem.models.movie import Movie
from app.irsystem.models import DATA_DIR

TOKEN_LIST_FILENAME = "token_list_before_pca.json"
DICT_TOKEN_TO_ID_FILENAME = "dict_token_to_id_before_pca.json"
EIGENVECTOR_COLUMN_FILENAME = "game_movie_eigenvectors_column.json"

with open(os.path.join(DATA_DIR, TOKEN_LIST_FILENAME), "r") as json_in:
    raw_token_list = json.load(json_in)
with open(os.path.join(DATA_DIR, DICT_TOKEN_TO_ID_FILENAME), "r") as json_in:
    dict_token_to_id = json.load(json_in)
with open(os.path.join(DATA_DIR, EIGENVECTOR_COLUMN_FILENAME), "r") as json_in:
    basis_eigenvector = json.load(json_in)
basis_eigenvector = np.array(basis_eigenvector)

# retrieve basis eigenvectors
# basis_eigenvector = json.loads(eigenvector.query.get("1").alleigenvector)
# basis_eigenvector = np.array(basis_eigenvector)

# handle reshaped basis_eigenvector
# retrieved_eigenvectors = db.session.query(eigenvector.alleigenvector).all()
# basis_eigenvector = []
# for vector in retrieved_eigenvectors:
#     basis_eigenvector.extend(eval(vector.alleigenvector))
# with open(os.path.join(DATA_DIR, 'basis_eigenvector.json'), 'w') as json_file:
#     json.dump(basis_eigenvector, json_file)
# basis_eigenvector = np.array(basis_eigenvector)


# retrieve vector of all games
game_vectors = dict()
allGameData = Game.query.with_entities(Game.app_id, Game.vector_pca).all()
for game in allGameData:
    game_vectors[game.app_id] = json.loads(game.vector_pca)

game_id_list = np.array(list(game_vectors.keys()))
dict_gameid_to_idx = {gid: i for i, gid in enumerate(game_id_list)}
game_vectors = np.array([game_vectors[key] for key in game_id_list])




# For now use movie_info2, which doesn't have desc_keywords
# MOVIE_INFO_FILENAME = 'movie_info.json'
# GAME_INFO_FILENAME = 'game_info.json'
#
# G_REV_COMMON_KEYWORDS_PHRASES_FILENAME = 'common_keywords_phrases.json'
# G_REV_INV_KEYWORDS_PHRASES_FILENAME = 'game_inv_rev_keyword_phrases.json'
# G_REV_KEYWORD_VEC_FILENAME = 'game_rev_keyword_vec.json'
# G_REV_WORD_TO_SYNPHRASES_FILENAME = 'game_rev_word_to_synphrase.json'

MOVIE_NAME_FILENAME = 'movie_titles.json'
G_GENRE_FILENAME = 'genre_list.json'
# MOVIE_GAME_TITLE_SIMILARITY_FILENAME = 'movie_game_title_similarity.json'

G_GENRE_KEY_FILENAME = 'genre_key.json'

with open(os.path.join(DATA_DIR, MOVIE_NAME_FILENAME), 'r', encoding='utf8') as in_json_file:
    MOVIE_TITLES = json.load(in_json_file)

with open(os.path.join(DATA_DIR, G_GENRE_KEY_FILENAME), 'r', encoding='utf8') as in_json_file:
    GENRE_KEY = json.load(in_json_file)

GAME_GENRES = list(sorted(GENRE_KEY.keys()))

# with open(os.path.join(DATA_DIR, G_REV_COMMON_KEYWORDS_PHRASES_FILENAME), 'r', encoding='utf8') as in_json_file:
#     G_REV_COMMON_KEYWORDS_PHRASES = json.load(in_json_file)
#
# with open(os.path.join(DATA_DIR, G_REV_INV_KEYWORDS_PHRASES_FILENAME), 'r', encoding='utf8') as in_json_file:
#     G_REV_INV_KEYWORDS_PHRASES = json.load(in_json_file)
#
# with open(os.path.join(DATA_DIR, G_REV_KEYWORD_VEC_FILENAME), 'r', encoding='utf8') as in_json_file:
#     G_REV_KEYWORD_VEC = json.load(in_json_file)
#
# # mac_memory_in_MB = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2**20)
# with open(os.path.join(DATA_DIR, G_REV_WORD_TO_SYNPHRASES_FILENAME), 'r', encoding='utf8') as in_json_file:
#     G_REV_WORD_TO_SYNPHRASES = json.load(in_json_file)
# # print(mac_memory_in_MB, flush=True)
#
# # mac_memory_in_MB = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2**20)
# with open(os.path.join(DATA_DIR, MOVIE_INFO_FILENAME), 'r', encoding='utf8') as in_json_file:
#     MOVIE_INFO = json.load(in_json_file)
# # print(mac_memory_in_MB, flush=True)
#
# # mac_memory_in_MB = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2**20)
# with open(os.path.join(DATA_DIR, GAME_INFO_FILENAME), 'r', encoding='utf8') as in_json_file:
#     GAME_INFO = json.load(in_json_file)
# # print(mac_memory_in_MB, flush=True)
#
# with open(os.path.join(DATA_DIR, G_GENRE_FILENAME), 'r', encoding='utf8') as in_json_file:
#     GAME_GENRES = json.load(in_json_file)

# with open(os.path.join(DATA_DIR, MOVIE_GAME_TITLE_SIMILARITY_FILENAME), 'r', encoding='utf8') as in_json_file:
#     MOVIE_GAME_TITLE_SIMILARITY = json.load(in_json_file)
#
mac_memory_in_MB = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2**20)
print(mac_memory_in_MB, flush=True)
