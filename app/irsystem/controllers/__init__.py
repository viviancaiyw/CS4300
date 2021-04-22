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

import json
import os

from app.irsystem.models import DATA_DIR

# For now use movie_info2, which doesn't have desc_keywords
MOVIE_INFO_FILENAME = 'movie_info.json'
GAME_INFO_FILENAME = 'game_info.json'

G_REV_COMMON_KEYWORDS_PHRASES_FILENAME = 'common_keywords_phrases.json'
G_REV_INV_KEYWORDS_PHRASES_FILENAME = 'game_inv_rev_keyword_phrases.json'
G_REV_KEYWORD_VEC_FILENAME = 'game_rev_keyword_vec.json'
G_REV_WORD_TO_SYNPHRASES_FILENAME = 'game_rev_word_to_synphrase.json'

MOVIE_NAME_FILENAME = 'movie_titles.json'
G_GENRE_FILENAME = 'genre_list.json'
MOVIE_GAME_TITLE_SIMILARITY_FILENAME = 'movie_game_title_similarity.json'
MOVIE_FILTERED_TITLE_MAP_FILENAME = 'movie_filtered_title_map.json'


with open(os.path.join(DATA_DIR, G_REV_COMMON_KEYWORDS_PHRASES_FILENAME), 'r', encoding='utf8') as in_json_file:
	G_REV_COMMON_KEYWORDS_PHRASES = json.load(in_json_file)

with open(os.path.join(DATA_DIR, G_REV_INV_KEYWORDS_PHRASES_FILENAME), 'r', encoding='utf8') as in_json_file:
	G_REV_INV_KEYWORDS_PHRASES = json.load(in_json_file)

with open(os.path.join(DATA_DIR, G_REV_KEYWORD_VEC_FILENAME), 'r', encoding='utf8') as in_json_file:
	G_REV_KEYWORD_VEC = json.load(in_json_file)

with open(os.path.join(DATA_DIR, G_REV_WORD_TO_SYNPHRASES_FILENAME), 'r', encoding='utf8') as in_json_file:
	G_REV_WORD_TO_SYNPHRASES = json.load(in_json_file)

with open(os.path.join(DATA_DIR, MOVIE_INFO_FILENAME), 'r', encoding='utf8') as in_json_file:
	MOVIE_INFO = json.load(in_json_file)

with open(os.path.join(DATA_DIR, GAME_INFO_FILENAME), 'r', encoding='utf8') as in_json_file:
	GAME_INFO = json.load(in_json_file)

with open(os.path.join(DATA_DIR, MOVIE_NAME_FILENAME), 'r', encoding='utf8') as in_json_file:
	MOVIE_TITLES = json.load(in_json_file)

with open(os.path.join(DATA_DIR, G_GENRE_FILENAME), 'r', encoding='utf8') as in_json_file:
	GAME_GENRES = json.load(in_json_file)

with open(os.path.join(DATA_DIR, MOVIE_GAME_TITLE_SIMILARITY_FILENAME), 'r', encoding='utf8') as in_json_file:
	MOVIE_GAME_TITLE_SIMILARITY = json.load(in_json_file)

with open(os.path.join(DATA_DIR, MOVIE_FILTERED_TITLE_MAP_FILENAME), 'r', encoding='utf8') as in_json_file:
	MOVIE_FILTERED_TITLE_MAP = json.load(in_json_file)



