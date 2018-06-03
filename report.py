import psycopg2

# connect to PostgreSQL database
db = psycopg2.connect("dbname=news")

# create cursor to execute operations on the database
cursor = db.cursor()

# Query 1: What are the most popular three articles of all time?
cursor.execute("""
select title, count(path) as num
from log, articles
where path like '%' || articles.slug || '%' and status = '200 OK'
group by title
order by num desc
limit 3;
""")

results = cursor.fetchall()

with open('results.txt', 'w') as f:
    f.write('Query 1: What are the most popular three articles of all time?\n')
    for r in results:
        f.write('%s\n' % str(r))
    f.write('\n')

# Query 2: Who are the most popular article authors of all time?
cursor.execute("""
select name, count(path) as num
from articles, authors, log
where authors.id = articles.author and path like '%' || articles.slug || '%'
and status = '200 OK'
group by name
order by count(path) desc
limit 3;
""")

results = cursor.fetchall()

with open('results.txt', 'a') as f:
    f.write('Query 2: Who are the most popular article authors of all time?\n')
    for r in results:
        f.write('%s\n' % str(r))
    f.write('\n')

# Query 3: On which days did more than 1% of requests lead to errors?
cursor.execute("""
create view error_view as
select date(time) as f_date, sum(case when
    substring(status, 0, 4)::int >= 400
    then 1
    else 0
    end)::decimal / (count(log.status)) as f_per
from log
group by date(time);

select to_char(f_date, 'Month DD YYYY'), round(f_per * 100, 1) || '%'
from error_view
group by f_date, f_per
having f_per > 0.01
""")

results = cursor.fetchall()

with open('results.txt', 'a') as f:
    f.write('Query 3: On which days did more than 1% of requests lead to errors?\n')  # noqa
    for r in results:
        f.write('%s\n' % str(r))
    f.write('\n')

db.close()
