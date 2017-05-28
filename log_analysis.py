# -----------------------------------------------------------------------------
# Author: XPRMNTS
# Python Version 3
# Log Analysis - Reporting on Dummy Web Statistics
# 1) What are the most popular three articles of all time?
# 2) Who are the most popular authors of all time?
# 3) On which days did more than 1% of requests lead to errors?
# -----------------------------------------------------------------------------
import datetime
import psycopg2

# Indicate the program is running
print("-" * 30 + "Running Log Analysis" + "-" * 30)

# List of Queries
list_of_queries = [
    ["The most popular three articles of all time are:\n",
     """
    select articles.title, count(*) as Views
    from log
    inner join articles on log.path like concat('%',articles.slug)
    group by articles.title order by Views desc limit 3;
    """],
    ["The most popular authors of all time are:\n",
     """
    select authors.name, count(*) as Views
    from log
    inner join articles on log.path like concat('%',articles.slug)
    inner join authors on articles.author = authors.id
    group by authors.name order by Views desc;
    """],
    ["The days where more than 1% of requests lead to errors are:\n",
     """
    select E.errors, V.views, E.day,
    ((cast(E.errors as float) / cast(V.views as float))*100) as rate
    from (select count(*) as errors, date(time) as day
    from log
    where status != '200 OK'
    group by day order by day desc) as E
    inner join (select count(*) as views, date(time) as day
    from log
    group by day order by day desc) as V on E.day = V.day
    where ((cast(E.errors as float) / cast(V.views as float))*100) > 1;
    """]
]

# Co
def connect(db_name):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        print("Connecting to database...\n")
        db = psycopg2.connect("dbname={}".format(db_name))
        c = db.cursor()
        return db, c
    except:
        print("Unable to connect to database")


def get_query_results(query):
    """ Sub function that executes a query from parent method""" 
    c.execute(query)
    results = c.fetchall()
    return results


def print_top_articles(lead, query):
    # Printing Results for Question 1
    print("-" * 80)
    print(lead)
    top_3_articles = get_query_results(query)

    rank = 1
    for article in top_3_articles:
        print("%i. Title: %s | Total Views All Time: %i" %
              (rank, article[0], article[1]))
        rank += 1

    rank = 1
    print("-" * 80 + "\n\n")


def print_top_authors(lead, query):
    # Printing Results for Question 2
    print("-" * 80)
    print(lead)
    popular_authors = get_query_results(query)
    rank = 1

    for author in popular_authors:
        print("%i. Name: %s | Total Views All Time: %i" %
              (rank, author[0], author[1]))
        rank += 1

    print("-" * 80 + "\n\n")


def print_top_error(lead, query):
    # Printing Results for Question 3
    print("-" * 80)
    print(lead)
    high_error_days = get_query_results(query)
    rank = 1

    for day in high_error_days:
        print("Date: %s | Error Rate (%s): %.2f" %
              (day[2].strftime('%B, %d %Y'), '%', day[3]))
        rank += 1

    print("-" * 80 + "\n\n")


# Execute Program
if __name__ == '__main__':
    # Connect to DB
    db, c = connect("news")

    # Loop through queries
    for item in list_of_queries:
        lead = item[0]
        query = item[1]
        index = list_of_queries.index(item)
        if index == 0:
            print_top_articles(lead, query)
        if index == 1:
            print_top_authors(lead, query)
        if index == 2:
            print_top_error(lead, query)
    # Close
    db.close()
    print("Closing connection to database...")
    print("Bye!")
