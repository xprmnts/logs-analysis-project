# -----------------------------------------------------------------------------
# Author: Abhinay Reddy
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

# Connect to "news" database
print("Connecting to database...\n")
db = psycopg2.connect("dbname=news")
c = db.cursor()

# Start Question 1) -----------------------------------------------------------
query = """
select articles.title, count(*) as Views
from log
inner join articles on log.path like concat('%',articles.slug)
group by articles.title order by Views desc limit 3;
"""
c.execute(query)
top_3_articles = c.fetchall()

# Printing Results
print("-" * 80)
print("The most popular three articles of all time are:\n")

rank = 1

for article in top_3_articles:
    print("%i. Title: %s | Total Views All Time: %i" %
          (rank, article[0], article[1]))
    rank += 1

print("-" * 80 + "\n\n")
# Finish Question 1) ----------------------------------------------------------
# Start Question 2) -----------------------------------------------------------
query = """
select authors.name, count(*) as Views
from log
inner join articles on log.path like concat('%',articles.slug)
inner join authors on articles.author = authors.id
group by authors.name order by Views desc;
"""
c.execute(query)
popular_authors = c.fetchall()

# Printing Results
print("-" * 80)
print("The most popular authors of all time are:\n")
rank = 1
for author in popular_authors:
    print("%i. Name: %s | Total Views All Time: %i" %
          (rank, author[0], author[1]))
    rank += 1
print("-" * 80 + "\n\n")
# Finish Question 2) ----------------------------------------------------------
# Start Question 3) -----------------------------------------------------------
query = """
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
"""

c.execute(query)
high_error_days = c.fetchall()

# Printing Results
print("-" * 80)
print("The days where more than 1% of requests lead to errors are:\n")
rank = 1
for day in high_error_days:
    print("Date: %s | Error Rate (%s): %.2f" %
          (day[2].strftime('%B, %d %Y'), '%', day[3]))
    rank += 1
print("-" * 80 + "\n\n")
# Finish Question 3) ----------------------------------------------------------

db.close()
print("Closing connection to database...")
print("Bye!")
