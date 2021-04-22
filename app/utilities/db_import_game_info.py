import json
import psycopg2

with open('../data/game_info.json') as f:
    game_info = json.load(f)
info_keys = list(game_info.keys())

print(type(game_info))
print(info_keys[:5])

# local postgres test
# conn = psycopg2.connect(database='app_trial',
#                         user='changwei',
#                         password='w45039w45039',
#                         host='localhost')

# postgres on heroku
conn = psycopg2.connect(database='d54e2cpo1gk8jf',
                        user='lfykwexqkamxmh',
                        password='fddd2b2526b3de064af5a3c471fe466da70ffa1b773bb43669fcd067590037b1',
                        host='ec2-3-211-37-117.compute-1.amazonaws.com',
                        port=5432)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE game_info (row_number      INT      PRIMARY KEY  NOT NULL,
                            app_id          TEXT,
                            name            TEXT,
                            developer       TEXT[],
                            publisher       TEXT[],
                            tags            TEXT[],
                            genres          TEXT[],
                            num_players     TEXT[],
                            rating          NUMERIC,
                            mature_content  BOOLEAN,
                            url             TEXT,
                            desc_keywords   TEXT[]
                            )                 
''')

for i, key in enumerate(info_keys):
    entry = game_info[info_keys[i]]
    cursor.execute("INSERT INTO game_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (i+1, key, entry['name'], entry['developer'], entry['publisher'], entry['tags'], entry['genre'],
                    entry['num_players'], entry['rating'], entry['mature_content'], entry['url'], entry['desc_keywords']))
conn.commit()

cursor.close()
conn.close()