import psycopg2

db = psycopg2.connect("dbname=news")

cursor = db.cursor()

cursor.execute("select path, count(path) as num from log where path like '/article/%' group by path order by num desc limit 3;")

results = cursor.fetchall()

print (results)

db.close()
