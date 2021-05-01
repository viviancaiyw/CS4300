import os

os.environ["APP_SETTINGS"] = "config.DevelopmentConfig"
os.environ["DATABASE_URL"] = "postgres://bivxusanexnbjp:12f8e000800ba66e4f98d0df4795edc962bdfd5318cbd9f19c7eaf16ef244f54@ec2-52-23-45-36.compute-1.amazonaws.com:5432/dd46p10a83f3m0"
# os.environ["DATABASE_URL"] = "postgresql://changwei:w45039w45039@localhost/app_trial"
import json
from app.irsystem.models.eigenvector import eigenvector
from app.irsystem.models.game import Game
from app.irsystem.models.movie import Movie
from app import db

DATA_DIR = os.path.abspath(os.path.join(__file__, "..", "..", "..", "data"))

# TODO
LOCAL_DATA_DIR = os.path.abspath(os.path.join(
    __file__, "..", "..", "..", "data", 'pca_svd'))

EIGENVECTORS_PCA_COLUMNS = "game_movie_eigenvectors_column.json"
EIGENVECTORS_PCA_COLUMNS_RESHAPED = "game_movie_eigenvectors_column_reshaped.json"
TOKEN_LST_BEFORE_PCA = "token_list_before_pca.json"
DICT_TOKEN_TO_IDX_BEFORE_PCA = "dict_token_to_id_before_pca.json"
MOVIE_VECTORS_PCA = "dict_movieid_to_vector_pca.json"
GAME_VECTORS_PCA = "dict_gameid_to_vector_pca.json"
GAME_INFO_FILENAME = 'game_info.json'
MOVIE_INFO_FILENAME = "movie_info.json"
GAME_INFO_FILENAME = "game_info.json"
TOP3000_MOVIE_GAME_TITLE_SIMILARITY_FILENAME = "top3000movie_game_title_similarity.json"
MOVIE_NAME_FILENAME = "movie_id_to_title.json"


def init_db():
    # Create tables
    print("Create db tables...")
    db.create_all()

    # Dump data

    with open(os.path.join(DATA_DIR, MOVIE_INFO_FILENAME), "r") as in_json_file:
        movie_info = json.load(in_json_file)
    with open(os.path.join(DATA_DIR, GAME_INFO_FILENAME), "r") as in_json_file:
        game_info = json.load(in_json_file)
    with open(os.path.join(LOCAL_DATA_DIR, EIGENVECTORS_PCA_COLUMNS),
              "r") as in_json_file:
        eigenvectors_pca = json.load(in_json_file)

    # eigenvectors_pca_reshaped reshapes eigenvectors_pca vector to fit into 1388 rows
    # Original vector dimension: 9716 x 2576
    # Reshaped dimension: 1388 x 7 x 2576
    # with open(os.path.join(LOCAL_DATA_DIR, EIGENVECTORS_PCA_COLUMNS_RESHAPED), "r") as in_json_file:
    #     eigenvectors_pca_reshaped = json.load(in_json_file)
    with open(os.path.join(LOCAL_DATA_DIR, MOVIE_VECTORS_PCA),
              "r") as in_json_file:
        movie_vectors = json.load(in_json_file)
    with open(os.path.join(LOCAL_DATA_DIR, GAME_VECTORS_PCA),
              "r") as in_json_file:
        game_vectors = json.load(in_json_file)
    with open(os.path.join(DATA_DIR, TOP3000_MOVIE_GAME_TITLE_SIMILARITY_FILENAME),
              "r") as in_json_file:
        movie_game_title_sim = json.load(in_json_file)
    with open(os.path.join(DATA_DIR, MOVIE_NAME_FILENAME), "r") as in_json_file:
        movie_titles = json.load(in_json_file)

    print("Dump movie data...")
    for (link, info) in movie_info.items():
        db.session.add(Movie(
            link_id=str(link),
            name=str(movie_titles[link]),
            games_review_match=json.dumps(info['games']),
            games_title_match=json.dumps(movie_game_title_sim.get(link, [])),
            genre=json.dumps(info['genre']),
            desc_keywords=json.dumps(info['desc_keywords']),
            vector_pca=json.dumps(movie_vectors[link])
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
            desc_keywords=json.dumps(info['desc_keywords']),
            vector_pca=json.dumps(game_vectors[appid])
        ))

    print("Dump basis eigenvectors...")
    # for row, vectors in eigenvectors_pca_reshaped.items():
    #     db.session.add(eigenvector(rn=row, vec=json.dumps(vectors)))
    db.session.add(eigenvector(rn="1", vec=json.dumps(eigenvectors_pca)))

    print("Dump basis eigenvectors complete...")

    db.session.commit()

    print("init_db done")


def drop_db():
    print("Drop all db tables...")
    db.session.remove()
    db.drop_all()


def modify_db():
    with open(os.path.join(DATA_DIR, MOVIE_INFO_FILENAME), "r") as in_json_file:
        movie_info = json.load(in_json_file)
    with open(os.path.join(DATA_DIR, GAME_INFO_FILENAME), "r") as in_json_file:
        game_info = json.load(in_json_file)
    with open(os.path.join(LOCAL_DATA_DIR, EIGENVECTORS_PCA_COLUMNS),
              "r") as in_json_file:
        eigenvectors_pca = json.load(in_json_file)
    with open(os.path.join(LOCAL_DATA_DIR, MOVIE_VECTORS_PCA),
              "r") as in_json_file:
        movie_vectors = json.load(in_json_file)
    with open(os.path.join(LOCAL_DATA_DIR, GAME_VECTORS_PCA),
              "r") as in_json_file:
        game_vectors = json.load(in_json_file)

    print("adding in movie vector...")
    for key in movie_info.keys():
        thisMovie = Movie.query.filter_by(link_id=key)
        thisMovie.vector_pca = json.dumps(movie_vectors[key])
    db.session.commit()
    print("adding in movie vector complete...")

    print("adding in game vector...")
    for key in game_info.keys():
        thisGame = Game.query.filter_by(app_id=key)
        thisGame.vector_pca = json.dumps(game_vectors[key])
    db.session.commit()
    print("adding in game vector complete...")

    print("adding in basis eigenvectors...")
    db.session.add(eigenvector(rn="1", vec=json.dumps(eigenvectors_pca)))
    db.session.commit()
    print("adding in movie vector complete...")


def modify_title_similarity():
    print("updating similarity scores ...")
    with open(os.path.join(DATA_DIR,
                           TOP3000_MOVIE_GAME_TITLE_SIMILARITY_FILENAME),
              "r") as in_json_file:
        movie_game_sim = json.load(in_json_file)

    for link_id in movie_game_sim.keys():
        movie_obj: Movie = Movie.query.filter_by(link_id=link_id).first()
        movie_obj.games_title_match = json.dumps(movie_game_sim[link_id])
    db.session.commit()
    print("finish updating similarity scores ...")


if __name__ == '__main__':
    # drop_db()
    # init_db()
    # modify_db()
    modify_title_similarity()
