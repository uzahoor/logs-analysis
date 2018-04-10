#!/usr/bin/env python2
# Database code for the DB Forum, full solution!

import psycopg2

DBNAME = "news"


def execute_query(query):
    """Execute a query and return the results as an array of tuples."""
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.Error as e:
        print "Database failed to connect" + str(e)
        return
    c = db.cursor()
    c.execute(query)
    posts = c.fetchall()
    db.close()
    return posts


def print_query_results(query_result):
    """Prints an array of tuples with some basic formatting"""
    for row in query_result:
        for column in row:
            if row[-1] == column:
                print str(column) + "\n",
            else:
                print str(column) + ' - ',


def main():
    print "Most popular articles of all time\n"
    print "Title - View Count"
    print_query_results(
        execute_query("SELECT title, views FROM top_articles LIMIT 3;")
      )
    print "\nMost popular article authors of all time\n"
    print "Author Name - View Count"
    print_query_results(execute_query("SELECT * from top_authors LIMIT 4;"))
    print "\nDays with more than 1% of request error\n"
    print "Date - Errors(%)"
    print_query_results(execute_query("SELECT * from error_days;"))


if __name__ == "__main__":
    main()
