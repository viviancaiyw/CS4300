import psycopg2

# local test
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
                SELECT app_id, name, url, desc_keywords FROM game_info
                where 'engage' = ANY(desc_keywords) and 'girl' = ANY(desc_keywords);
               ''')

rows = cursor.fetchall()

res = {}

for row in rows:
    res[row[0]] = {'name':row[1], 'url':row[2], 'keywords':row[3]}

print(res)
print(type(res))

conn.close()