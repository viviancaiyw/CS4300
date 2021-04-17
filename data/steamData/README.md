## Steam Data Documentation

### 80k_data
- **movie_steam_same_titles.json** <br>
  ```
  {"same_titles": [
     game/movie_name_1, 
     game/movie_name_2, 
     ...
     ]
  }
  ```
  which contains a list of names which exists in both movies and games. This means the movies are based from games or vice versa. 
- **movie_game_title_similarity.csv.zip**
  You need to unzip the file to get the JSON to use, which is in format:
  ```
  {"movie id 1": [
    [app_id_1, similarity score], 
    [app_id_2, similarity score],
    ...
    [app_id_100, similarity score]], 
    ...
  }
  ```



### web_crawl_data
- **app_ids.json** <br>
  This stores all app ids crawled from the Steam Web API. It's in JSON format 
  ```
  {"app_ids": [
     app_id_1, 
     app_id_2, 
     ...
     ]
  }
  ```
It might be useful if we want to expand our Steam Game database to more recent than Kaggle dataset. 
