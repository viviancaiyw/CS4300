from app.irsystem.models import db, DATA_DIR
from app.irsystem.models.movie import Movie
from app.irsystem.models.game import Game
import json
import os


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
			name=info['name'],
			genre=json.dumps(info['genre']),
			content_rating=info['content_rating'],
			audience_count=int(info['audience_count']),
			desc_keywords=json.dumps(info['desc_keywords']),
			review_keywords=json.dumps(info['review_keywords']),
			review_keyphrases=json.dumps(info['review_keyphrases'])
		))

	print("Dump game data...")
	for (appid, info) in game_info.items():
		if info['mature_content']=='true':
			mature_content = True
		else:
			mature_content = False
		db.session.add(Game(
			app_id=str(appid),
			name=info['name'],
			developer=json.dumps(info['developer']),
			publisher=json.dumps(info['publisher']),
			tags=json.dumps(info['tags']),
			genre=json.dumps(info['genre']),
			num_players=json.dumps(info['num_players']),
			rating=int(info['rating']),
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

if __name__ == '__main__':
	drop_db()
	init_db()

