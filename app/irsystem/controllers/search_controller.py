# from flask_login import login_required

from . import *
import json
from app.utilities.search_form import search_form
from app.irsystem.controllers.tags_movie_match import *
from flask import render_template, flash, redirect, url_for, request

from app.utilities.import_datasets import movie_names, game_genres

project_name = "Steamy Reviews: Game Recommendation Engine"
net_id = "Chang Wei: cw887, Qichen Hu: qh75, Yuwen Cai: yc687, Yitian Lin: yl698"



@irsystem.route('/', methods=['GET', 'POST'])
def home():
    form = search_form()
    if request.method == 'POST':
        if form.validate_on_submit():

            # TODO

            return render_template('result.html', form=form)
    return render_template('search.html', form=form, genres=game_genres, mv_names=movie_names)

# @irsystem.route('/result', methods=['GET', 'POST'])
# def result(form):
#     return render_template('result.html', form=form)
# @irsystem.route('/search', methods=['GET', 'POST'])
# def search():
#     form = search_form()
#     if form.validate_on_submit():
#
#
#         pass
#     render_template(url_for('home'), form=form)
    # query = request.args.get('search')
    # if not query:
    #     data = []
    #     output_message = ''
    # else:
    #     output_message = "Your search: " + query
    #     data = range(5)
    # return render_template('search.html', name=project_name, netid=net_id,
    #                        output_message=output_message, data=data)

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
