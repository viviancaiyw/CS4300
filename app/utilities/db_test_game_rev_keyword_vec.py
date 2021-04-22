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
    SELECT row_number, app_id, vector FROM inv_idx ORDER BY norm DESC LIMIT 10;
''')

row = cursor.fetchone()

rn = row[0]
app_id = row[1]
vec = row[2]
print(rn, app_id, vec)
print(type(rn), type(app_id), type(vec))