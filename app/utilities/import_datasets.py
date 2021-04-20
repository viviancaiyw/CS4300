import json

game_genres = sorted(['action','indie','mmo','strategy','sports','party-game','open-world','simulation','role-playing','adventure',
 'boardgame', 'survival', 'fps', 'puzzle', 'casual', 'wargame', 'tower defense'])


# Import json datasets
path = "app/data/"
with open(path + "movie_info.json", 'r', encoding='utf8') as mv_info:
  movie_info = json.load(mv_info)

movie_names = [movie_info[x]['name'] for x in movie_info] # all original movie names

