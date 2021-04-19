# from flask_login import login_required

from . import *

from app.irsystem.controllers.tags_movie_match import *
# from app.irsystem.models.database import init_db, drop_db

project_name = "Steamy Reviews: Game Recommendation Engine"
net_id = "Chang Wei: cw887, Qichen Hu: qh75, Yuwen Cai: yc687, Yitian Lin: yl698"


@irsystem.route('/', methods=['GET'])
def home():
    # drop_db()
    # init_db()
    return render_template('search.html')

@irsystem.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
    else:
        output_message = "Your search: " + query
        data = range(5)
    return render_template('search.html', name=project_name, netid=net_id,
                           output_message=output_message, data=data)

@irsystem.route('/tags_movie_match', methods=['GET', 'POST'])
def tags_match():
    tags = request.json.get('tags', '')
    movie = request.json.get('movie', '')
    if not tags:
        data = []
        output_message = ''
    else:
        output_message = "Your tags: " + str(tags) + " Your movie: " + str(movie)
        data = match_tags_and_movie(tags, movie)

        print(data, flush=True)
    return Response(json.dumps(data),  mimetype="application/json")
