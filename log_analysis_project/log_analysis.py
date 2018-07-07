#!/usr/bin/env python3

from tabulate import tabulate
import psycopg2

DBNAME = "news"


def getMostPopularArticles(numArticles):
    """returns a list of articles from the database
       with the most number of views"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select articles.title, top_paths.num
              from articles, top_paths
              where top_paths.path like '%' || articles.slug || '%' limit """ + str(numArticles) + ";")  # NOQA
    rows = c.fetchall()
    db.close()
    return rows


def getMostPopularAuthors():
    """returns a list of authors from the database
       with the most number of article views"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select authors.name, top_authors.num_views
            from top_authors, authors
            where top_authors.author = authors .id;""")
    rows = c.fetchall()
    db.close()
    return rows


def getErrorRatesForArticleRequests():
    """returns a list of days from the database
       where more than 1% of requests lead to errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select total_views.time::timestamp::date,
            failed_views.num * 100 / total_views.num::float as errors
            from failed_views, total_views
            where failed_views.time::timestamp::date =
                  total_views.time::timestamp::date
            and failed_views.num * 100 / total_views.num::float > 1;""")
    rows = c.fetchall()
    db.close()
    return rows


print("\nWhat are the most popular three articles of all time?")
print tabulate(getMostPopularArticles(3),
               headers=['Article', 'Views'],
               numalign="center",
               tablefmt="fancy_grid")

print("\nWho are the most popular article authors of all time?")
print tabulate(getMostPopularAuthors(),
               headers=['Author', 'Views'],
               tablefmt="fancy_grid",
               numalign="center",
               floatfmt=".0f")

print("\nOn which days did more than 1% of requests lead to errors?")
print tabulate(getErrorRatesForArticleRequests(),
               headers=['Date', 'Error(%)'],
               numalign="center",
               tablefmt="fancy_grid",
               floatfmt=".2f")
