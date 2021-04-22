import json
import psycopg2

with open("../data/game_rev_keyword_vec.json", 'r', encoding='UTF8') as f:
    game_rev_keyword_vec = json.load(f)

keys = list(game_rev_keyword_vec.keys())
print(len(keys))

conn = psycopg2.connect(database='app_trial',
                        user='changwei',
                        password='w45039w45039',
                        host='localhost')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE inv_idx (row_number    INT     PRIMARY KEY     NOT NULL,
                          app_id        TEXT,
                          norm          NUMERIC,
                          vector        JSON
                          )
''')

for i, key in enumerate(keys):
    entry = game_rev_keyword_vec[key]
    cursor.execute("INSERT INTO inv_idx VALUES(%s, %s, %s, %s)", (i+1, key, entry['norm'], json.dumps(entry['vector'])))
conn.commit()

conn.close()