from app.irsystem.controllers import MOVIE_TITLES, GAME_GENRES, dict_gamename_to_id

def get_movie_list():
  """
  Returns: list of movie titles in the form of (movie_name, movie_id)
  """
  return MOVIE_TITLES
  
def get_genre_list():
  """
  Returns: list of game genres
  """
  return GAME_GENRES

def get_game_dict():
  """
  Returns: [{name: id}...]
  """
  return dict_gamename_to_id