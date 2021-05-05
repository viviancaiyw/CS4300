# from flask_login import login_required

from app.irsystem.controllers.cosine_search import searchWrapper
from app.irsystem.controllers.get_info import *
from app.irsystem.controllers.metadata_match import filter_games
# from app.irsystem.controllers.reviews_match import *
from app.irsystem.controllers.titles_match import *
from . import *

# import resource

project_name = "Steamy Reviews: Game Recommendation Engine"
net_id = "Chang Wei: cw887, Qichen Hu: qh75, Yuwen Cai: yc687, Yitian Lin: yl698"


@irsystem.route('/', methods=['GET'])
def home():
    return render_template('search.html',
                           genresData=json.dumps(get_genre_list()),
                           moviesData=json.dumps(get_movie_list()),
                           gamesData=json.dumps(get_game_dict()))


@irsystem.route('/search', methods=['GET'])
def search():
    return redirect(url_for('irsystem.home'))


@irsystem.route('/search-run', methods=['POST'])
def search_action():
    # mac_memory_in_MB = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (2**20)
    # print(mac_memory_in_MB, flush=True)
    playerSingle = True if request.form.get('playerTypeSingle') else False
    playerMulti = True if request.form.get('playerTypeMulti') else False
    tags = json.loads(request.form.get('gameTags')) if request.form.get(
        'gameTags') else []
    movie = request.form.get('movieEnjoy') if request.form.get(
        'movieEnjoy') else None
    if movie:
        tags.extend(movie.split('_'))
    game = request.form.get('gameEnjoy') if request.form.get(
        'gameEnjoy') else None
    genres = json.loads(request.form.get('gameGenre')) if request.form.get(
        'gameGenre') else None

    # response_body = searchWrapper(playerSingle, playerMulti, genres, tags, movie, game_vectors, game_id_list)
    metadata_candidates = filter_games(singleplayer=playerSingle,
                                       multiplayer=playerMulti,
                                       raw_genre_list=genres)
    response_body = {
        "based on svd": searchWrapper(
            playerSingle, playerMulti, genres, tags, movie, game, game_vectors, game_id_list),
        "based on titles": get_top_games_from_title_for_movie(
            mov_tmt_path=movie, candidate_games=metadata_candidates,
            threshold=0.3) if movie else get_top_games_from_title_for_game(
            app_id=game, candidate_games=metadata_candidates,
            threshold=0.3)
    }
    return render_template('result.html', data=response_body)
