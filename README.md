# Logs Analysis

This is a simple Python script that outputs some interesting query results of the database 'news'. This program uses views for all the queries as this allows code reuse and to split up queries making them easier to read.

## Prerequisites

* Python 2.7.
* Postgresql version 9.5.11 or later 
* The 'news' database in Postgresql
* Linux flavors, OS X and Windows, packages are available at https://wiki.python.org/moin/BeginnersGuide/Download

## Setting up the 'news' database in Postgresql

These instructions will create the 'news' database that is required to run the python script

1. Download the following zip file [Download link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
2. Extract the zip file, A sql file named 'newsdata.sql' will now exist
3. Run the 'newsdata.sql' using the following command
```
$ psql -U <db_user> news < newsdata.sql
```
4. The 'news' database should be created
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Follow the instructions below.

1. Navigate to the folder containing 'newsdata.py' 
2. Ensure that all the required files are found in the same directory ('newsdata.py', 'newsdata_views.sql')
3. Run 'newsdata_views.sql' to create the necessary views in the database
```
$ psql news -f newsdata_views.sql
```
4. Run 'newsdata.py' to get the desired log analysis
```
$ python newsdata.py
```

## Views Used

View to get the top articles in the database which can later be filtered to show a limited number of articles

	CREATE OR REPLACE view top_articles AS
	SELECT articles.title, articles.author, COUNT(*) AS views
	FROM articles JOIN log 
	ON log.path = '/article/' || articles.slug
	GROUP BY articles.title, articles.author
	ORDER BY views DESC;

View to get the top authors in the database which can later be filtered to show a limited number of authors. This view relies on the 'top_articles' view to get the correct results.

	CREATE OR REPLACE view top_authors AS 
	SELECT authors.name, sum(top_articles.views) AS views 
	FROM top_articles JOIN authors 
	ON authors.id = top_articles.author
	GROUP BY authors.name
	ORDER BY views DESC;


View to get the requests that result in errors on a specific date.

	CREATE OR REPLACE view errors AS 
	SELECT date(time) AS date, COUNT(*) AS requests
	FROM log
	WHERE status LIKE '%404%'
	GROUP BY date;


View to get the number of requests on a specific date.

	CREATE OR REPLACE view total AS 
	SELECT date(time) AS date, COUNT(*) AS requests
	FROM log
	GROUP BY date;


View to calculate on what dates more than 1% of requests were errors. This view relies on the 'total' and 'error' views to help get the result.

	CREATE OR REPLACE view error_days AS 
	SELECT total.date, ROUND(((errors.requests * 1.0) / total.requests) * 100, 2) AS errors_percent
	FROM errors JOIN total
	ON total.date = errors.date
	WHERE ROUND(((errors.requests * 1.0) / total.requests) * 100, 2) > 1
	ORDER BY errors DESC;
