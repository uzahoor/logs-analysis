# !/usr/bin/env python3
# Database code for the DB Forum, full solution!

import psycopg2

DBNAME = "news"


def get_top_three_articles():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT title, views FROM top_articles LIMIT 3;")
    posts = c.fetchall()
    db.close()
    return posts


def get_top_five_authors():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * from top_authors LIMIT 4;")
    posts = c.fetchall()
    db.close()
    return posts


def get_error_days():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * from error_days;")
    posts = c.fetchall()
    db.close()
    return posts


def print_query_results(query_result):
    """Add a post to the 'database' with the current timestamp."""
    for row in query_result:
        for column in row:
            if row[-1] == column:
                print str(column) + "\n",
            else:
                print str(column) + ' - ',


def main():
    print "Most popular articles of all time\n"
    print "Title - View Count"
    print_query_results(get_top_three_articles())
    print "\nMost popular article authors of all time\n"
    print "Author Name - View Count"
    print_query_results(get_top_five_authors())
    print "\nDays with more than 1% of request error\n"
    print "Date - Errors(%)"
    print_query_results(get_error_days())


if __name__ == "__main__":
	main()
