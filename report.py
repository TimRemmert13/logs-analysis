#!/usr/bin/env python3

import psycopg2
import sys


def connect(database):
    '''
    Connect to the PostgreSQL database and return a connection with
    a cursor. If an error occurs during the connection, a message is printed
    and the program is terminated.

    Returns:
        A database connection and a cursor for running operations on
        the database.

        Raises:
            psycopg2.Error: an error occured during the attempted connection
            to the database.
    '''
    try:
        db = psycopg2.connect(database)
        cursor = db.cursor()
        return db,  cursor
    except psycopg2.Error:
        print('Unable to connect to database')
        sys.exit(1)


def print_results(results, w_or_a, query, last):
    '''Function to pretty print query results and the original query to
    a text file called results.txt

    Args:
        results (list of tuples): results of the executed query.
        w_or_a (char): a char value of w or a to denote whether to write to
                the text file or append to the text file. Only the first query
                should use w or write.
        query (str): a string that denotes what the original query was.
        last (bool): boolean value to denote if this is the last query or not.
                    If it is the last query we need to print errors at the end
                    of each line and not views.
    '''
    if not last:
        with open('results.txt', w_or_a) as f:
            f.write(query + '\n')
            for r in results:
                f.write('%s - %s views\n' % (str(r[0]), str(r[1])))
            f.write('\n')
    else:
        with open('results.txt', w_or_a) as f:
                f.write(query + '\n')
                for r in results:
                    f.write('%s - %s errors\n' % (str(r[0]), str(r[1])))
                f.write('\n')


def get_top_articles():
    '''execute query to find and print the top 3 articles'''
    db, cursor = connect("dbname=news")

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
    query1 = 'Query 1: What are the most popular three articles of all time?'
    print_results(results, 'w', query1, False)
    db.close()


def get_top_authors():
    '''execute a query to find and print the top 3 authors'''
    db, cursor = connect("dbname=news")

    # Query 2: Who are the most popular article authors of all time?
    cursor.execute("""
    select name, count(path) as num
    from articles, authors, log
    where authors.id = articles.author and
    path like '%' || articles.slug || '%'
    and status = '200 OK'
    group by name
    order by count(path) desc
    limit 3;
    """)

    results = cursor.fetchall()
    query2 = 'Query 2: Who are the most popular article authors of all time?'
    print_results(results, 'a', query2, False)
    db.close()


def get_top_error_days():
    '''execute a query to find and print the days with more than 1% of request
    leading to errors'''
    db, cursor = connect("dbname=news")
  
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
    query3 = 'Query 3: On which days did more than 1% of requests lead to errors?'  # noqa
    print_results(results, 'a', query3, True)
    db.close()

# make sure the program is ran directly and not imported
if __name__ == '__main__':
    get_top_articles()
    get_top_authors()
    get_top_error_days()
