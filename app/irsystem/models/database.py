from app.irsystem.models import db
from app.irsystem.models.movie import Movie
from app.irsystem.models.game import Game
import json
import os

DATA_DIR = os.path.abspath(os.path.join(__file__, "..", "..", "..", "data"))


def init_db():
    MOVIE_INFO_FILENAME = "movie_info.json"
    GAME_INFO_FILENAME = "game_info.json"

    # Create tables
    print("Create db tables...")
    db.create_all()

    # Dump data
    with open(os.path.join(DATA_DIR, MOVIE_INFO_FILENAME), "r") as in_json_file:
        movie_info = json.load(in_json_file)
    with open(os.path.join(DATA_DIR, GAME_INFO_FILENAME), "r") as in_json_file:
        game_info = json.load(in_json_file)

    print("Dump movie data...")
    for (link, info) in movie_info.items():
        db.session.add(Movie(
            link_id=str(link),
            games=json.dumps(info['games']),
            genre=json.dumps(info['genre']),
            desc_keywords=json.dumps(info['desc_keywords'])
        ))

    print("Dump game data...")
    for (appid, info) in game_info.items():
        if info['mature_content'] == 'true':
            mature_content = True
        else:
            mature_content = False
        single_player = False
        multi_player = False
        if 'single-player' in info['num_players']:
            single_player = True
        if 'multi-player' in info['num_players']:
            multi_player = True
        db.session.add(Game(
            app_id=str(appid),
            name=info['name'],
            developer=json.dumps(info['developer']),
            publisher=json.dumps(info['publisher']),
            tags=json.dumps(info['tags']),
            genre=json.dumps(info['genre']),
            single_player=single_player,
            multi_player=multi_player,
            rating=str(info['rating']),
            mature_content=mature_content,
            url=str(info['url']),
            desc_keywords=json.dumps(info['desc_keywords'])
        ))

    db.session.commit()

    print("init_db done")


def drop_db():
    print("Drop all db tables...")
    db.session.remove()
    db.drop_all()

# if __name__ == '__main__':
# 	drop_db()
# 	init_db()
